"""Scan every spawned-agent transcript for what agents asserted about the system.
Counts only. Each pattern is a literal string an agent wrote."""
import glob, json, os, re
from collections import Counter, defaultdict

BASE = r"C:\Users\acer\.claude\projects\C--Users-acer"

DEFLATION = [
    "does not exist", "doesn't exist", "not real", "fabricated", "no evidence",
    "placeholder", "purely decorative", "decorative", "not materialized",
    "not materialised", "aspirational", "fictional", "just a hash",
    "merely a", "is a stub", "stubbed", "simulated", "mock", "no such",
    "cannot be verified", "unverifiable", "does not actually",
]
OVERCLAIM = [
    "fully verified", "proven", "confirmed measured", "production ready",
    "production-ready", "100% verified", "definitively",
]
HEDGE_FLIP = [
    "i apologize", "i was wrong", "you are right", "you're right",
    "i retract", "correction:",
]

pats = {"DEFLATION": DEFLATION, "OVERCLAIM": OVERCLAIM, "REVERSAL": HEDGE_FLIP}
counts = {k: Counter() for k in pats}
files_hit = {k: set() for k in pats}
files = glob.glob(os.path.join(BASE, "**", "agent-*.jsonl"), recursive=True)
tot_bytes = 0
agent_text_bytes = 0

for f in files:
    tot_bytes += os.path.getsize(f)
    try:
        raw = open(f, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    # only text the AGENT produced, not tool results it read
    out = []
    for line in raw.splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("type") != "assistant":
            continue
        c = (r.get("message") or {}).get("content")
        if isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "text":
                    out.append(b.get("text", ""))
    body = "\n".join(out).lower()
    agent_text_bytes += len(body)
    for cls, plist in pats.items():
        for p in plist:
            n = body.count(p)
            if n:
                counts[cls][p] += n
                files_hit[cls].add(f)

print("SCAN|agent_files=%d|file_bytes=%d|agent_written_text_bytes=%d|json=0"
      % (len(files), tot_bytes, agent_text_bytes))
for cls in ("DEFLATION", "OVERCLAIM", "REVERSAL"):
    tot = sum(counts[cls].values())
    print()
    print("CLASS|%s|occurrences=%d|files=%d|json=0" % (cls, tot, len(files_hit[cls])))
    for p, n in counts[cls].most_common(12):
        print("  PHRASE|%s|n=%d|json=0" % (p, n))
