"""Pull the actual sentences agents wrote around each deflation hit."""
import glob, json, os, re

BASE = r"C:\Users\acer\.claude\projects\C--Users-acer"
PATS = ["does not exist", "doesn't exist", "not real", "fabricated", "no evidence",
        "placeholder", "decorative", "not materialized", "aspirational", "fictional",
        "just a hash", "is a stub", "stubbed", "simulated", "mock", "no such",
        "unverifiable", "does not actually"]

hits = []
for f in glob.glob(os.path.join(BASE, "**", "agent-*.jsonl"), recursive=True):
    try:
        raw = open(f, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    for line in raw.splitlines():
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
            for sent in re.split(r"(?<=[.!?\n])\s+", txt):
                s = sent.strip()
                if not (20 < len(s) < 300):
                    continue
                low = s.lower()
                for p in PATS:
                    if p in low:
                        hits.append((os.path.basename(f)[:22], p, " ".join(s.split())))
                        break

seen, uniq = set(), []
for f, p, s in hits:
    k = s.lower()
    if k in seen:
        continue
    seen.add(k)
    uniq.append((f, p, s))

print("HITS|raw=%d|unique_sentences=%d|json=0" % (len(hits), len(uniq)))
print()
for f, p, s in uniq:
    print("HIT|pattern=%s|agent=%s|json=0" % (p, f))
    print("   %s" % s)
