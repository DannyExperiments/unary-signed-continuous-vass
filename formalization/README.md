# Lean certificate

`SignedGrid.shares` is checked using Lean 4.30.0 and its standard library.

For any positive integer capacity D and m occurrences, every integer mass between m and mD admits exactly m positive shares bounded by D. Lean proves existence by constructing the shares recursively. In the signed-VASS paper this supplies the allocation after multiplying by a common denominator. Obtaining a short supported walk, bounding that denominator, and proving the complexity classification are separate steps.

[Source](Q1568Grid.lean) · [Verification workflow](../.github/workflows/lean.yml)

To replay from the repository root with Lean 4.30.0 installed, run

```sh
lean -DwarningAsError=true formalization/Q1568Grid.lean
```

The source requests an axiom report. The GitHub Actions workflow downloads the pinned compiler, verifies its SHA-256 and checks the source with warnings treated as errors.
