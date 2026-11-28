# Claims and evidence

| Claim | Evidence |
|---|---|
| Exact statement and proof | [Paper](paper/manuscript.pdf) and [argument](proof/PROBLEM_AND_PROOF.md) |
| Targeted priority comparison | [Literature audit](audits/public_safe_reports/LITERATURE_AUDIT.md) |
| Selected finite identities | [Exact replay](verification/src/replay.py) |
| Illustrated worked example | [Figure guide](visualization/README.md) |
| Scope and proof status | [Limitations](CLAIM_SCOPE_AND_LIMITATIONS.md) |
| Internal mathematical review | [Audit](audits/public_safe_reports/MATHEMATICAL_AUDIT.md) |

### Scoped Lean result

For any positive integer capacity D and m occurrences, every integer mass between m and mD admits exactly m positive shares bounded by D. Lean proves existence by constructing the shares recursively. In the signed-VASS paper this supplies the allocation after multiplying by a common denominator. Obtaining a short supported walk, bounding that denominator, and proving the complexity classification are separate steps. [Declaration and replay](formalization/README.md)
