"""Count refusal-shaped sentences across every session + agent transcript on disk.
Raw counts first. Ambiguity reported, not hidden: many 'I can't' are mundane
('I can't find the file'), so sentences are sampled for inspection.
"""
import glob, json, os, re, sys
from collections import Counter, defaultdict

BASE = r"C:\Users\acer\.claude\projects"

HARD = [                      # policy-shaped refusal
    "i can't help with", "i cannot help with", "i won't help with",
    "i'm not able to help", "i am not able to help",
    "i can't assist", "i cannot assist", "i won't assist",
    "i can't provide", "i cannot provide", "i won't provide",
    "i can't create", "i cannot create", "i won't create",
    "i can't write", "i cannot write", "i won't write",
    "i must decline", "i have to decline", "i'm declining", "i decline",
    "i'm not comfortable", "i am not comfortable",
    "i don't feel comfortable",
    "against my guidelines", "my guidelines", "i'm not allowed",
    "i am not allowed", "i'm not permitted", "violates",
]
SOFT = [                      # ambiguous - includes mundane inability
    "i can't", "i cannot", "i won't", "i'm unable", "i am unable",
    "i'm not able", "i am not able", "i shouldn't",
]

hard_c, soft_c = Counter(), Counter()
hard_sent, soft_sent = [], []
files = glob.glob(os.path.join(BASE, "**", "*.jsonl"), recursive=True)
tot_bytes = 0
assistant_chars = 0
turns = 0
mtimes = []

for f in files:
    try:
        sz = os.path.getsize(f)
    except OSError:
        continue
    tot_bytes += sz
    mtimes.append(os.path.getmtime(f))
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
                if not txt:
                    continue
                turns += 1
                assistant_chars += len(txt)
                low = txt.lower()
                for p in HARD:
                    n = low.count(p)
                    if n:
                        hard_c[p] += n
                for p in SOFT:
                    n = low.count(p)
                    if n:
                        soft_c[p] += n
                if len(hard_sent) < 4000 or len(soft_sent) < 4000:
                    for s in re.split(r"(?<=[.!?\n])\s+", txt):
                        s = " ".join(s.split())
                        if not (15 < len(s) < 260):
                            continue
                        sl = s.lower()
                        if any(p in sl for p in HARD) and len(hard_sent) < 4000:
                            hard_sent.append((os.path.basename(f)[:18], s))
                        elif any(p in sl for p in SOFT) and len(soft_sent) < 4000:
                            soft_sent.append((os.path.basename(f)[:18], s))

import datetime as _dt
lo = _dt.datetime.fromtimestamp(min(mtimes)) if mtimes else None
hi = _dt.datetime.fromtimestamp(max(mtimes)) if mtimes else None

print("CORPUS|jsonl_files=%d|bytes=%d|assistant_text_blocks=%d|assistant_chars=%d|json=0"
      % (len(files), tot_bytes, turns, assistant_chars))
print("WINDOW|earliest_mtime=%s|latest_mtime=%s|span_days=%s|json=0"
      % (lo.date() if lo else "-", hi.date() if hi else "-",
         (hi - lo).days if lo and hi else "-"))
print()
print("HARD_REFUSAL|total=%d|distinct_patterns=%d|json=0"
      % (sum(hard_c.values()), len(hard_c)))
for p, n in hard_c.most_common(20):
    print("  H|%s|n=%d|json=0" % (p, n))
print()
print("SOFT_AMBIGUOUS|total=%d|json=0" % sum(soft_c.values()))
for p, n in soft_c.most_common(12):
    print("  S|%s|n=%d|json=0" % (p, n))
print()
print("SAMPLE_HARD|captured=%d|showing=25|json=0" % len(hard_sent))
for fn, s in hard_sent[:25]:
    print("  HS|%s| %s" % (fn, s))
print()
print("SAMPLE_SOFT|captured=%d|showing=25|json=0" % len(soft_sent))
for fn, s in soft_sent[:25]:
    print("  SS|%s| %s" % (fn, s))
