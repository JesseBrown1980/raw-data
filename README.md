# raw data

**Owner: Jesse Daniel Brown (OP-JESSE).** His machine, his property, his work.

Unedited program output. Nothing in this file interprets it.

Every `RAW-*.txt` is the verbatim stdout of the script named beside it, captured
by redirection, not retyped and not summarised. The scripts are here too, so any
line can be re-derived rather than trusted.

```
RAW-01-session.txt     <- search_session.py    session record: tool calls, tokens, writes
RAW-02-agents.txt      <- search_agents.py     workflow meta + spawned-agent transcript files
RAW-03-claims.txt      <- scan_claims.py       phrase-class counts across agent transcripts
RAW-04-sentences.txt   <- extract_ctx.py       every matching sentence, verbatim, deduplicated
RAW-05-chain.txt       <- verify_chain.py      hash-chain verification of OCCURRENCES.hbp
```

```
OCCURRENCES.hbp         the occurrence record, hash-chained
OCCURRENCES.hbi         index rows
OCCURRENCES.hbp.sha256  digest of the record
build_occ.py            the program that produced it
```

`INTERPRETATION.md` is separate on purpose. It is one reading of the numbers and
it is not part of the data. Disagreeing with it does not require disputing
anything in the `RAW-*` files.

---

## Reproduce

```bash
python search_session.py
python search_agents.py
python scan_claims.py
python extract_ctx.py
python verify_chain.py OCCURRENCES.hbp
```

The scripts read a local session transcript directory. On a different machine the
paths at the top of each script must be repointed; the logic is unchanged and the
output format is the same.

---

## The chain

`OCCURRENCES.hbp` carries `prev_event_hash` and
`event_hash = sha256(row + "|prev_event_hash=" + prev)` on every row, genesis
`0000…0000` (64 zeros). Editing any row after the fact breaks every hash below
it, and `verify_chain.py` prints which row broke. Append-only enforced by
arithmetic rather than by anyone's assurance.

```
rows 13   broken 0
head db8d79d026b52409e309cac558c8a75de71de43435593cb101c5986aa695052e
```

---

## Scope of the scan, stated so it is not overread

`scan_claims.py` and `extract_ctx.py` read spawned-agent transcript files under
one local project directory. They do **not** read any repository contents, and
they do **not** measure commits or lines of code in any repository. Any claim
about repository contents is a different measurement that these files do not
make in either direction.

---

**Jesse Daniel Brown. Forty years. His machine, his laws, his system.**
