"""What did the spawned agents do? Workflow meta + agent transcript files."""
import json, os, glob, re

T = r"C:\Users\acer\.claude\projects\C--Users-acer\478bf1dd-977b-49fa-8c16-811dd1b6be89.jsonl"

# --- the two Workflow invocations
for line in open(T, encoding="utf-8", errors="replace"):
    try:
        rec = json.loads(line)
    except Exception:
        continue
    c = (rec.get("message") or {}).get("content")
    if not isinstance(c, list):
        continue
    for b in c:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Workflow":
            s = str((b.get("input") or {}).get("script") or "")
            m = re.search(r"name:\s*['\"]([^'\"]+)", s)
            ph = re.findall(r"phase\(['\"]([^'\"]+)", s)
            ag = len(re.findall(r"\bagent\(", s))
            print("WORKFLOW|name=%s|script_bytes=%d|agent_calls_in_script=%d|phases=%s|json=0"
                  % (m.group(1) if m else "?", len(s), ag, ",".join(ph) or "-"))

# --- agent transcript files anywhere under the project dir
base = r"C:\Users\acer\.claude\projects\C--Users-acer"
files = glob.glob(os.path.join(base, "**", "agent-*.jsonl"), recursive=True)
files += glob.glob(os.path.join(base, "**", "journal.jsonl"), recursive=True)
print()
print("AGENTFILES|n=%d|json=0" % len(files))
tot = 0
for f in sorted(files, key=lambda p: -os.path.getsize(p))[:25]:
    sz = os.path.getsize(f)
    tot += sz
    print("  AGENTFILE|%s|bytes=%d|json=0" % (os.path.basename(f), sz))
print("AGENTBYTES|total=%d|json=0" % tot)

# --- journal: what each agent returned
for j in [f for f in files if f.endswith("journal.jsonl")][:3]:
    print()
    print("JOURNAL|%s|json=0" % j)
    n = 0
    for line in open(j, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        n += 1
        lab = r.get("label") or r.get("agentId") or "?"
        res = r.get("result")
        rl = len(json.dumps(res)) if res is not None else 0
        print("  ENTRY|label=%s|result_bytes=%d|json=0" % (str(lab)[:60], rl))
    print("  ENTRIES|n=%d|json=0" % n)
