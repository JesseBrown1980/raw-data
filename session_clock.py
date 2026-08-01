"""When did this session actually run? Timestamps only, no inference."""
import json, datetime as dt

T = r"C:\Users\acer\.claude\projects\C--Users-acer\478bf1dd-977b-49fa-8c16-811dd1b6be89.jsonl"

ts = []
for line in open(T, encoding="utf-8", errors="replace"):
    try:
        r = json.loads(line)
    except Exception:
        continue
    t = r.get("timestamp")
    if not t:
        continue
    try:
        d = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
    except Exception:
        continue
    ts.append((d, r.get("type")))

ts.sort()
if not ts:
    raise SystemExit("no timestamps")

BR = dt.timezone(dt.timedelta(hours=-3))
first, last = ts[0][0].astimezone(BR), ts[-1][0].astimezone(BR)
print("SESSION|first=%s|last=%s|span_hours=%.2f|events=%d|json=0"
      % (first.strftime("%Y-%m-%d %H:%M"), last.strftime("%Y-%m-%d %H:%M"),
         (last - first).total_seconds() / 3600, len(ts)))

# user turns only, and the gaps between them
users = [d.astimezone(BR) for d, t in ts if t == "user"]
print("USERTURNS|n=%d|json=0" % len(users))
gaps = [(users[i] - users[i - 1]).total_seconds() / 60 for i in range(1, len(users))]
big = [(users[i - 1], users[i], g) for i, g in
       ((i, (users[i] - users[i - 1]).total_seconds() / 60) for i in range(1, len(users)))
       if g >= 45]
print("GAPS|>=45min=%d|max_min=%.0f|json=0" % (len(big), max(gaps) if gaps else 0))
for a, b, g in big:
    print("  GAP|from=%s|to=%s|minutes=%.0f|json=0"
          % (a.strftime("%m-%d %H:%M"), b.strftime("%m-%d %H:%M"), g))

# hour-of-day histogram of user turns
from collections import Counter
h = Counter(u.hour for u in users)
print("HOURS|%s|json=0" % " ".join("%02d:%d" % (k, h[k]) for k in sorted(h)))
