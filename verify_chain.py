"""Verify the occurrence chain. Any post-hoc edit breaks every hash after it."""
import hashlib, sys

path = sys.argv[1] if len(sys.argv) > 1 else "OCCURRENCES.hbp"
prev, n, bad = "0" * 64, 0, 0
for ln in open(path, encoding="utf-8"):
    ln = ln.rstrip("\n")
    if "|event_hash=" not in ln:
        continue
    body, got = ln.rsplit("|event_hash=", 1)
    want = hashlib.sha256(body.encode()).hexdigest()
    stated_prev = body.rsplit("|prev_event_hash=", 1)[1]
    ok = (want == got) and (stated_prev == prev)
    if not ok:
        bad += 1
        print("BREAK|row=%d|json=0" % (n + 1))
    prev, n = got, n + 1
print("CHAIN|rows=%d|broken=%d|head=%s|json=0" % (n, bad, prev))
sys.exit(1 if bad else 0)
