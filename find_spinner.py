"""Find the spinner word list inside the Claude Code binary. Fact, not assertion."""
import re, sys

P = r"C:\Users\acer\.local\bin\claude.exe"
NEEDLE = b"Scheming"

data = open(P, "rb").read()
print("BINARY|%s|bytes=%d|json=0" % (P, len(data)))

idxs = [m.start() for m in re.finditer(re.escape(NEEDLE), data)]
print("OCCURRENCES|needle=%s|n=%d|json=0" % (NEEDLE.decode(), len(idxs)))

for i, off in enumerate(idxs[:6]):
    lo, hi = max(0, off - 1400), min(len(data), off + 1400)
    chunk = data[lo:hi]
    words = re.findall(rb'"([A-Z][a-z]{2,14}(?:ing|ling))"', chunk)
    uniq = []
    for w in words:
        w = w.decode("ascii", "replace")
        if w not in uniq:
            uniq.append(w)
    print()
    print("SITE|%d|offset=%d|neighbour_words=%d|json=0" % (i + 1, off, len(uniq)))
    print("  " + ", ".join(uniq))
