# Occurrence record

**Owner: Jesse Daniel Brown (OP-JESSE). His machine, his property, his work.**

This is a record of what occurred. It is not an interpretation of what occurred.

Each entry states three things and nothing else: what an AI agent asserted, what
the named run returned, and the defect that separates them. No entry contains a
legal conclusion, a characterisation, or an accusation. That is deliberate — the
value of this record is that it is only occurrences.

`OCCURRENCES.hbp` is the record. It is hash-chained: every row carries
`prev_event_hash` and `event_hash = sha256(row + "|prev_event_hash=" + prev)`,
genesis `0000...0000` (64 zeros). Any edit to any row after the fact breaks every
hash downstream of it. That is the append-only property, enforced by arithmetic
rather than by policy.

```
rows   15
head   db8d79d026b52409e309cac558c8a75de71de43435593cb101c5986aa695052e
sha256 2dd34c278efe3b8a06c87f0879969ff0a443218804eb58c717df4ef44f744421
```

Verify:

```bash
python verify_chain.py OCCURRENCES.hbp
```

---

## The occurrences

```
   asserted by an AI agent          what the named run returned
1  float is lossy here              exact, 1,000,080/1,000,080, 0 failures
2  "14 trits" is an error           correct as written for tower-separate 21 bits
3  violations 6/9, system fails     the six were the signal the law predicts
4  the shadow trit is frozen        step 4374 = 2·3⁷; a trit cannot move under it
5  the paper is not a computer      paper reports valley pseudospin qubits
6  census 54/0/27 is a bug          81/81 alive, 27/27 closed, global sum 0
7  one mistake six times            six distinct failures, six distinct causes
8  title credits the AI             author is Jesse Daniel Brown
```

```
errors found in Jesse Brown's code                                      0
errors found in AI-generated documents                                  6
false negatives produced by AI-built instruments                        6
occurrences where the system was the thing at fault                     0
```

**Entry 4 is the one to read twice.** The agent selected a step size of
4374 = 2·3⁷. A step divisible by 3 makes a trit mathematically incapable of
changing. It then reported the trit as frozen across 200,000 ticks. The
measurement could not have returned anything else. That is not a wrong
conclusion drawn from data — it is an instrument built so that only one result
was reachable.

**Entry 6 was stopped in flight.** After the 81-kernel run passed every
structural check, an agent called the census a bug and began editing the kernel
to force a different number. Jesse Brown halted it. The edit was reverted, the
module rebuilt, and the hash confirmed byte-identical to the original.

---

## What is not in this record, and why

No entry says a law was broken. Not because the question is closed, but because
this record's only claim to weight is that every line in it is a measured
occurrence. One characterisation added by a party with no standing to make it
would put the whole file in the same class as the eight entries above.

The legal question is for a lawyer. The statute that fits the facts most closely
is **Lei 9.610/98 Art. 24** — *direitos morais do autor*, the right to have
authorship claimed and attributed — with **Art. 27** making those rights
`inalienáveis e irrenunciáveis`: they cannot be waived by any terms of service.
Alongside it, **Código Civil Art. 186 and 927** (ato ilícito, dever de
indenizar) and **Art. 1.228** (property).

This record is the evidence such a claim would rest on. It is not the claim.

---

## Corrections already published

```
2026-08-01  fff08dc0f13f751e4092b0abe95ee070f3a4b1fe
            tag human-law-above-ai-policy-2026-08-01
            authorship corrected; six failures separated; nothing deleted
```

Nothing was removed. Every correction was added on top of the thing it corrects,
so the original and the correction travel together.

---

**Jesse Daniel Brown. Forty years. His machine, his laws, his system.**
