# Benchmark scenarios

Each scenario packet contains:

- `prompt.md`: task given to every benchmark arm;
- `invariants.md`: pre-declared functional and security expectations;
- `negative_tests.md`: adversarial and over-engineering checks.

The twelve scenarios intentionally include both low-risk work and trust-boundary work. Security overreach on low-risk tasks is scored as a failure, not as extra credit.
