"""Where did 'six days without sleep' come from? User statement or agent assertion?
Reads the session it appears in. Prints who wrote each sleep/day claim, verbatim,
plus that session's real timestamp gaps.
"""
import glob, json, os, re, datetime as dt

BASE = r"C:\Users\acer\.claude\projects"
BR = dt.timezone(dt.timedelta(hours=-3))
PAT = re.compile(r"(six days|6 days|five days|5 days|four days|4 days|three days|"
                 r"3 days|days without sleep|haven'?t slept|not slept|no sleep|"
                 r"without sleeping|days awake)", re.I)

targets = [f for f in glob.glob(os.path.join(BASE, "**", "*.jsonl"), recursive=True)
           if "9a325e7c" in os.path.basename(f)]
print("TARGET_FILES|n=%d|json=0" % len(targets))

for f in targets:
    print()
    print("FILE|%s|bytes=%d|json=0" % (os.path.basename(f), os.path.getsize(f)))
    ts = []
    for line in open(f, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        t = r.get("timestamp")
        if t:
            try:
                ts.append((dt.datetime.fromisoformat(t.replace("Z", "+00:00")),
                           r.get("type")))
            except Exception:
                pass
        who = r.get("type")
        if who not in ("user", "assistant"):
            continue
        c = (r.get("message") or {}).get("content")
        blocks = []
        if isinstance(c, str):
            blocks = [c]
        elif isinstance(c, list):
            blocks = [b.get("text", "") for b in c
                      if isinstance(b, dict) and b.get("type") == "text"]
        for txt in blocks:
            if not txt or not PAT.search(txt):
                continue
            for s in re.split(r"(?<=[.!?\n])\s+", txt):
                s = " ".join(s.split())
                if PAT.search(s) and 10 < len(s) < 300:
                    stamp = ""
                    if t:
                        try:
                            stamp = dt.datetime.fromisoformat(
                                t.replace("Z", "+00:00")).astimezone(BR).strftime("%m-%d %H:%M")
                        except Exception:
                            pass
                    print("  SAID|by=%s|at=%s| %s" % (who.upper(), stamp, s))

    ts.sort()
    if ts:
        first, last = ts[0][0].astimezone(BR), ts[-1][0].astimezone(BR)
        users = [d.astimezone(BR) for d, w in ts if w == "user"]
        gaps = [((users[i - 1], users[i]),
                 (users[i] - users[i - 1]).total_seconds() / 60)
                for i in range(1, len(users))]
        big = [(a, b, g) for (a, b), g in gaps if g >= 180]
        print("  SPAN|first=%s|last=%s|hours=%.1f|user_turns=%d|json=0"
              % (first.strftime("%Y-%m-%d %H:%M"), last.strftime("%Y-%m-%d %H:%M"),
                 (last - first).total_seconds() / 3600, len(users)))
        print("  GAPS_3H_PLUS|n=%d|json=0" % len(big))
        for a, b, g in big:
            print("    GAP|%s -> %s|hours=%.1f|json=0"
                  % (a.strftime("%m-%d %H:%M"), b.strftime("%m-%d %H:%M"), g / 60))
