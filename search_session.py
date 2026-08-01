"""Search the session record for what agents did. Index tool-call records, not prose."""
import json, os, sys
from collections import Counter, defaultdict

T = r"C:\Users\acer\.claude\projects\C--Users-acer\478bf1dd-977b-49fa-8c16-811dd1b6be89.jsonl"

spawns = []          # Agent / Task / Workflow invocations
tool_use = Counter()
writes = []          # files written
pushes = []          # gh api mutations
usage = defaultdict(int)
n = 0

for line in open(T, encoding="utf-8", errors="replace"):
    line = line.strip()
    if not line:
        continue
    try:
        rec = json.loads(line)
    except Exception:
        continue
    n += 1
    msg = rec.get("message") or {}
    u = msg.get("usage") or {}
    for k in ("input_tokens", "output_tokens",
              "cache_creation_input_tokens", "cache_read_input_tokens"):
        if isinstance(u.get(k), int):
            usage[k] += u[k]
    content = msg.get("content")
    if not isinstance(content, list):
        continue
    for blk in content:
        if not isinstance(blk, dict) or blk.get("type") != "tool_use":
            continue
        name = blk.get("name", "?")
        tool_use[name] += 1
        inp = blk.get("input") or {}
        if name in ("Agent", "Task", "Workflow"):
            spawns.append(dict(
                tool=name,
                subagent=inp.get("subagent_type") or inp.get("name") or "",
                desc=(inp.get("description") or inp.get("title") or "")[:90],
                prompt_len=len(str(inp.get("prompt") or inp.get("script") or "")),
            ))
        elif name in ("Write", "Edit", "NotebookEdit"):
            p = str(inp.get("file_path", ""))
            writes.append(p)
        elif name in ("Bash", "PowerShell"):
            c = str(inp.get("command", ""))
            low = c.lower()
            if "gh api" in low and ("-x post" in low or "-x patch" in low or
                                    "-x put" in low or "-x delete" in low):
                pushes.append(c[:160].replace("\n", " "))

print("RECORDS|n=%d|json=0" % n)
print("TOKENS|out=%d|in=%d|cache_create=%d|cache_read=%d|json=0"
      % (usage["output_tokens"], usage["input_tokens"],
         usage["cache_creation_input_tokens"], usage["cache_read_input_tokens"]))
print()
print("SPAWNS|total=%d|json=0" % len(spawns))
by = Counter((s["tool"], s["subagent"]) for s in spawns)
for (t, sa), c in by.most_common():
    print("  SPAWN|tool=%s|subagent=%s|count=%d|json=0" % (t, sa or "-", c))
print()
print("TOOLUSE|distinct=%d|json=0" % len(tool_use))
for k, v in tool_use.most_common(18):
    print("  TOOL|%s|n=%d|json=0" % (k, v))
print()
print("MUTATIONS|gh_api_writes=%d|json=0" % len(pushes))
print("WRITES|n=%d|json=0" % len(writes))
ext = Counter(os.path.splitext(w)[1].lower() or "(none)" for w in writes)
for k, v in ext.most_common(12):
    print("  EXT|%s|n=%d|json=0" % (k, v))
