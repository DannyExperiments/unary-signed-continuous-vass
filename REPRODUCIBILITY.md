# Reproducibility

From the repository root with Python 3.11 or later, run:

```sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
```

The exact replay checks 43,680 grid allocation fixtures, the worked reachability example, signed coverability, and a zero-length run. The expected stdout is in [the replay log](verification/logs/replay.txt). The replay is finite and supports particular proof steps. See [PDF build instructions](paper/BUILD.md) for a clean rebuild. The diagram is an illustration of the worked example in the README. Its explorer needs only a browser and runs offline.
