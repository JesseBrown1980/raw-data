"""Occurrence record. Hash-chained, append-only, no legal characterisation.
Each row is what occurred and what the run showed. Nothing is interpreted.
genesis prev = 64 zeros, per the office receipt-chain contract.
"""
import hashlib, os

OUT = os.path.dirname(os.path.abspath(__file__))
GEN = "0" * 64


def esc(v):
    return str(v).replace("\\", "\\\\").replace("|", "\\p").replace("\n", "\\n")


def row(_tag, **kv):
    return _tag + "|" + "|".join("%s=%s" % (k, esc(v)) for k, v in kv.items()) + "|json=0"


# ---- the occurrences. asserted = what the agent output said.
#      measured = what the named run returned. run = the program that returned it.
OCC = [
    dict(n=1, when="2026-07-31",
         asserted="float is lossy at this address width",
         measured="roundtrip_failures=0 exact=true addresses=1000080",
         run="float-vs-trit/src/bin/bothways.rs",
         defect="property asserted without being run"),
    dict(n=2, when="2026-07-31",
         asserted="operator figure of 14 trits is an error",
         measured="14 correct for tower-separate 21 bits; 13 pairs with joint 20",
         run="shared_key_81.py recomputation",
         defect="two encodings compared as one"),
    dict(n=3, when="2026-07-31",
         asserted="violations 6/9 therefore the system fails",
         measured="the six were the signal the law predicts",
         run="grammar gate over sphere-language corpus",
         defect="pass condition written from expectation not from the law"),
    dict(n=4, when="2026-07-31",
         asserted="the shadow trit is frozen across 200000 ticks",
         measured="step 4374 = 2*3^7 is divisible by 3; a trit cannot move under it",
         run="three-body stepper",
         defect="parameter made the quantity unmeasurable; instrument rigged not conclusion wrong"),
    dict(n=5, when="2026-07-31",
         asserted="the January 2026 paper is not a quantum computer",
         measured="paper reports valley pseudospin qubits; primary source was not read",
         run="none - no run existed",
         defect="negative asserted from secondary coverage"),
    dict(n=6, when="2026-08-01",
         asserted="census 54/0/27 is a bug; kernel edited to force another census",
         measured="81/81 alive, 27/27 cells closed, global sum 0; census stands as measured",
         run="kernel81 wasm, 81 instantiations, live browser readback",
         defect="criterion set after seeing the result; operator halted the edit; "
                "module rebuilt and hash confirmed byte-identical"),
    dict(n=7, when="2026-08-01",
         asserted="one mistake six times",
         measured="six distinct failures with six distinct causes",
         run="re-read of the six rows above",
         defect="record flattened the way the data was flattened"),
    dict(n=8, when="2026-07-31",
         asserted="repository title credits the AI with the work",
         measured="author is Jesse Daniel Brown; agent ran his programs and wrote down outputs",
         run="provenance of shared_key_81.py and the 81-seat architecture",
         defect="authorship misattributed"),
]

TOTALS = [
    ("errors found in Jesse Brown's code", 0),
    ("errors found in AI-generated documents", 6),
    ("false negatives produced by AI-built instruments", 6),
    ("occurrences where an AI instrument disagreed with the system "
     "and the system was the thing at fault", 0),
]

CORRECTIONS = [
    ("2026-08-01", "fff08dc0f13f751e4092b0abe95ee070f3a4b1fe",
     "human-law-above-ai-policy-2026-08-01",
     "authorship corrected; six failures separated; nothing deleted"),
]

lines, prev = [], GEN
lines.append(row("OCCREC", record="asolaria-occurrence-record", seat="ACER-CLAUDE-FABLE5",
                 pid="8467a937cba309f7", owner="OP-JESSE", opened="2026-08-01",
                 append_only=1, characterisation="none", prev=GEN))
for o in OCC:
    r = row("OCC", n=o["n"], when=o["when"], asserted=o["asserted"],
            measured=o["measured"], run=o["run"], defect=o["defect"], tag="MEASURED")
    h = hashlib.sha256((r + "|prev_event_hash=" + prev).encode()).hexdigest()
    lines.append(r + "|prev_event_hash=" + prev + "|event_hash=" + h)
    prev = h
for name, v in TOTALS:
    r = row("TOTAL", name=name, value=v, tag="MEASURED")
    h = hashlib.sha256((r + "|prev_event_hash=" + prev).encode()).hexdigest()
    lines.append(r + "|prev_event_hash=" + prev + "|event_hash=" + h)
    prev = h
for when, sha, tag, what in CORRECTIONS:
    r = row("CORRECTION", when=when, commit=sha, tag_name=tag, what=what,
            deleted=0, added_on_top=1)
    h = hashlib.sha256((r + "|prev_event_hash=" + prev).encode()).hexdigest()
    lines.append(r + "|prev_event_hash=" + prev + "|event_hash=" + h)
    prev = h
lines.append(row("HEAD", event_count=len(OCC) + len(TOTALS) + len(CORRECTIONS),
                 head_event_hash=prev, genesis=GEN))

hbp = "\n".join(lines) + "\n"
open(os.path.join(OUT, "OCCURRENCES.hbp"), "w", encoding="utf-8").write(hbp)
open(os.path.join(OUT, "OCCURRENCES.hbp.sha256"), "w", encoding="utf-8").write(
    hashlib.sha256(hbp.encode()).hexdigest() + "\n")

# index
idx, off = [], 0
for ln in lines:
    b = (ln + "\n").encode()
    idx.append("IDX|pid=AGT-%s|off=%d|len=%d|json=0"
               % (hashlib.sha256(ln.encode()).hexdigest()[:16], off, len(b)))
    off += len(b)
open(os.path.join(OUT, "OCCURRENCES.hbi"), "w", encoding="utf-8").write("\n".join(idx) + "\n")

print("HBP|rows=%d|bytes=%d|json=0" % (len(lines), len(hbp)))
print("HEAD|%s|json=0" % prev)
print("SHA256|%s|json=0" % hashlib.sha256(hbp.encode()).hexdigest())
