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

SCHEMA_DIR = pathlib.Path(__file__).parent.parent / "schema"
SCHEMA_PATH = SCHEMA_DIR / "sframe.schema.json"
INSTRUMENT_SCHEMA_PATH = SCHEMA_DIR / "sframe-instrument.schema.json"

# Two conformance profiles, checked in order. "instrument" is what
# surveyframe's write_sframe() emits today; "full" is the complete five-layer
# provenance chain, whose later layers arrive with surveyframe 0.6. A file is
# valid if it conforms to either. Reporting a flat pass/fail against the full
# profile alone rejected every real file the reference implementation writes.
PROFILES = [("instrument", INSTRUMENT_SCHEMA_PATH), ("full", SCHEMA_PATH)]
LAYER_ORDER = ["instrument", "version", "response", "analysis_reporting", "verification_manifest"]


def load_schema(path=SCHEMA_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_profile(instance):
    """Pick the profile to validate against from the object's own shape,
    so the error messages name real problems instead of profile mismatch."""
    if "layers" in instance or "sframe_schema_version" in instance:
        return "full"
    return "instrument"


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

    profile = detect_profile(instance)
    path = dict(PROFILES)[profile]
    errors = validate_schema(instance, load_schema(path))

    if errors:
        print(f"SCHEMA INVALID ({profile} profile): {target}")
        for e in errors:
            print(f"  - {'.'.join(str(p) for p in e.path)}: {e.message}")
        sys.exit(1)

    print(f"SCHEMA VALID ({profile} profile): {target}")
    if profile == "instrument":
        fmt = instance.get("sframe_format", "unset")
        n_items = len(instance.get("items", []))
        n_scales = len(instance.get("scales", []))
        n_plan = len(instance.get("analysis_plan", []))
        print(f"Format version: {fmt}")
        print(f"  - items: {n_items}, scales: {n_scales}, declared analyses: {n_plan}")
        print("Lifecycle stage: 1/5 (instrument declared; response, "
              "analysis/reporting and manifest layers not present)")
        sys.exit(0)

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
