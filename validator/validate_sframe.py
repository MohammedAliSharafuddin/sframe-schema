#!/usr/bin/env python3
"""
validator/validate_sframe.py

Reference validator for the .sframe schema (v0.1-draft), written in Python
with no R dependency, to demonstrate the schema is usable outside the R
ecosystem it originates from. Requires: jsonschema (pip install jsonschema).

Usage:
    python validate_sframe.py <path-to-sframe.json>

Exit code 0 on schema-valid input, 1 otherwise. Chain-integrity checks (layer
ordering, hash linkage) are reported separately from schema validity, since
an object can be schema-valid with an incomplete chain (fewer than five
layers present) without being invalid.
"""

import sys
import json
import pathlib

try:
    import jsonschema
except ImportError:
    sys.exit("This validator requires the 'jsonschema' package: pip install jsonschema")

SCHEMA_PATH = pathlib.Path(__file__).parent.parent / "schema" / "sframe.schema.json"
LAYER_ORDER = ["instrument", "version", "response", "analysis_reporting", "verification_manifest"]


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(instance, schema):
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    return errors


def check_chain(instance):
    """Report per-layer chain status. Not a schema check: a partial chain
    (fewer than five layers present) is schema-valid but incomplete."""
    layers = instance.get("layers", {})
    status = {}
    previous_hash = None
    for name in LAYER_ORDER:
        layer = layers.get(name)
        if layer is None:
            status[name] = "absent"
            continue
        if previous_hash is not None and layer.get("previous_hash") != previous_hash:
            status[name] = "chain-broken"
        else:
            status[name] = "linked"
        previous_hash = layer.get("hash")
    return status


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    target = pathlib.Path(sys.argv[1])
    with open(target, "r", encoding="utf-8") as f:
        instance = json.load(f)

    schema = load_schema()
    errors = validate_schema(instance, schema)

    if errors:
        print(f"SCHEMA INVALID: {target}")
        for e in errors:
            print(f"  - {'.'.join(str(p) for p in e.path)}: {e.message}")
        sys.exit(1)

    print(f"SCHEMA VALID: {target}")
    chain = check_chain(instance)
    n_present = sum(1 for v in chain.values() if v != "absent")
    print(f"Lifecycle stage: {n_present}/5")
    for name, state in chain.items():
        print(f"  - {name}: {state}")

    if any(state == "chain-broken" for state in chain.values()):
        print("CHAIN INTEGRITY: FAILED (a present layer's previous_hash does not match)")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
