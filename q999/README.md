# Q999

Quantum-certified 1-in-6 random draw across six labeled nodes (Gambia,
Nigeria, South Africa, Norway, Sweden, Denmark) — the companion tool
for the Q999 track concept ("spin, measure, verify").

This is a provably-fair random picker, not a harm simulator. The six
"nodes" are just labeled outcomes, comparable to rolling a die or
drawing a raffle ticket — there are no real-world stakes attached to
any result.

## How it works
1. `spin` requests one random byte from the [ANU Quantum Random
   Numbers Server](https://qrng.anu.edu.au/) (a real physical quantum
   RNG). If the network call fails, times out, or `--offline` is
   passed, it falls back to Python's `secrets` CSPRNG.
2. The byte is reduced mod 6 to select a node.
3. Every draw is written to `certificates/<run-id>.json` along with a
   SHA-256 hash computed over its fields.
4. `verify <file>` recomputes the hash and confirms the certificate
   has not been altered since it was generated.

## Usage
```
python q999.py spin              # try the quantum source, fall back to CSPRNG
python q999.py spin --offline    # skip the network call entirely
python q999.py verify certificates/<run-id>.json
```

## Notes
- Pure Python 3 standard library — no dependencies to install.
- The ANU QRNG endpoint is a free public API and may rate-limit or be
  unreachable; the CSPRNG fallback (`secrets` module, CSPRNG-grade) is
  always cryptographically sound regardless of network state.
- `source` in each certificate records which generator produced that
  draw (`QUANTUM_ANU` or `CSPRNG_FALLBACK`) for transparency.
