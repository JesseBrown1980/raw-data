"""Count 'sleep' in assistant-written text across every transcript on this machine.
Separates code/command uses (Start-Sleep, time.sleep, sleep 5) from prose
addressed to the operator. Every prose sentence is printed verbatim.
"""
import glob, json, os, re
from collections import Counter

BASE = r"C:\Users\acer\.claude\projects"
CODE = re.compile(r"(start-sleep|time\.sleep|sleep\s*\(|\bsleep\s+\d|asyncio\.sleep|"
                  r"sleep_?ms|delayseconds|thread\.sleep|--sleep|sleepms)", re.I)
WORD = re.compile(r"\bsleep\w*\b", re.I)

files = glob.glob(os.path.join(BASE, "**", "*.jsonl"), recursive=True)
total = code_hits = prose_hits = 0
prose, forms = [], Counter()
blocks = 0

for f in files:
    try:
        fh = open(f, encoding="utf-8", errors="replace")
    except Exception:
        continue
    with fh:
        for line in fh:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("type") != "assistant":
                continue
            c = (r.get("message") or {}).get("content")
            if not isinstance(c, list):
                continue
            for b in c:
                if not (isinstance(b, dict) and b.get("type") == "text"):
                    continue
                txt = b.get("text", "")
                if "sleep" not in txt.lower():
                    continue
                blocks += 1
                for m in WORD.finditer(txt):
                    total += 1
                    forms[m.group(0).lower()] += 1
                for s in re.split(r"(?<=[.!?\n])\s+", txt):
                    s = " ".join(s.split())
                    if not WORD.search(s):
                        continue
                    n = len(WORD.findall(s))
                    if CODE.search(s):
                        code_hits += n
                    else:
                        prose_hits += n
                        prose.append((os.path.basename(f)[:18], s[:240]))

print("CORPUS|jsonl_files=%d|assistant_blocks_containing_sleep=%d|json=0"
      % (len(files), blocks))
print("SLEEP|total_word_occurrences=%d|code_or_command=%d|prose=%d|json=0"
      % (total, code_hits, prose_hits))
print("FORMS|%s|json=0" % ", ".join("%s=%d" % (k, v) for k, v in forms.most_common()))
print()
print("PROSE_SENTENCES|n=%d|json=0" % len(prose))
for fn, s in prose:
    print("  P|%s| %s" % (fn, s))
