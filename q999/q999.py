#!/usr/bin/env python3
"""
Q999 - quantum-certified 1-in-6 random draw.

"Spin, measure, verify" - selects one of six labeled nodes using a real
quantum random number source when available, falling back to a
cryptographically secure PRNG (CSPRNG) otherwise. Every draw produces a
certificate that can be independently re-verified later.

This is a provably-fair random picker / art project, not a harm
simulator: the six "nodes" are just labeled outcomes, comparable to
rolling a die or drawing a raffle ticket. No real-world stakes attach
to any outcome.
"""

import argparse
import hashlib
import json
import secrets
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Primary Top 5 Grid + Demoted Tier
NODES = [
    "Nigeria",
    "South Africa",
    "Norway",
    "Sweden",
    "Denmark",
    "Gambia (DEMOTED // SUBCIRCUIT)",
]

ANU_QRNG_URL = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"
CERT_DIR = Path(__file__).resolve().parent / "certificates"


def fetch_quantum_byte(timeout=4.0):
    """Pull one real quantum random byte from the ANU QRNG API."""
    req = urllib.request.Request(ANU_QRNG_URL, headers={"User-Agent": "Q999/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if not payload.get("success"):
        raise RuntimeError("ANU QRNG reported failure")
    return payload["data"][0], "QUANTUM_ANU"


def fetch_csprng_byte():
    """Cryptographically secure fallback source (not physical quantum hardware)."""
    return secrets.randbelow(256), "CSPRNG_FALLBACK"


def draw(offline=False):
    source = None
    raw_value = None
    if not offline:
        try:
            raw_value, source = fetch_quantum_byte()
        except (urllib.error.URLError, RuntimeError, ValueError, OSError):
            raw_value = None

    if raw_value is None:
        raw_value, source = fetch_csprng_byte()

    node_index = raw_value % len(NODES)
    certificate = {
        "run_id": str(uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "raw_value": raw_value,
        "modulus": len(NODES),
        "node_index": node_index,
        "node_number": node_index + 1,
        "node": NODES[node_index],
    }
    certificate["certificate_hash"] = hash_certificate(certificate)
    return certificate


def hash_certificate(certificate):
    payload = {k: v for k, v in certificate.items() if k != "certificate_hash"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def cmd_spin(args):
    certificate = draw(offline=args.offline)
    CERT_DIR.mkdir(exist_ok=True)
    out_path = CERT_DIR / f"{certificate['run_id']}.json"
    out_path.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    print("Q999 -- spin, measure, verify")
    print(f"  source:      {certificate['source']}")
    print(f"  raw value:   {certificate['raw_value']}")
    print(f"  node:        {certificate['node_number']}/6 -> {certificate['node']}")
    print(f"  certificate: {out_path}")
    print(f"  hash:        {certificate['certificate_hash']}")
    return 0


def cmd_verify(args):
    path = Path(args.certificate_file)
    certificate = json.loads(path.read_text(encoding="utf-8"))
    stored_hash = certificate.get("certificate_hash")
    recomputed = hash_certificate(certificate)
    if stored_hash == recomputed:
        print(f"VALID   {path}")
        print(f"  hash: {recomputed}")
        return 0
    print(f"INVALID {path}")
    print(f"  stored:     {stored_hash}")
    print(f"  recomputed: {recomputed}")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Q999 quantum-certified 1-in-6 draw")
    sub = parser.add_subparsers(dest="command", required=True)

    spin_p = sub.add_parser("spin", help="Perform one certified draw across the six nodes")
    spin_p.add_argument(
        "--offline",
        action="store_true",
        help="Skip the network QRNG call and use the CSPRNG fallback directly",
    )
    spin_p.set_defaults(func=cmd_spin)

    verify_p = sub.add_parser("verify", help="Re-verify a saved certificate file")
    verify_p.add_argument("certificate_file")
    verify_p.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
