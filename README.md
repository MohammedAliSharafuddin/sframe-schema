# sframe-schema

**Status: `v0.1-draft`, not stable. Do not treat as a frozen standard.**

## Conformance profiles (added 2026-08-22)

The schema defines two profiles. A file is valid if it conforms to either.

| Profile | Schema | What it is | Status |
|---|---|---|---|
| `instrument` | `schema/sframe-instrument.schema.json` | Layer 1 plus the verification hash, serialised flat. What surveyframe's `write_sframe()` emits. | **implemented, CRAN 0.4.0** |
| `full` | `schema/sframe.schema.json` | The complete five-layer provenance chain. | target, layers 3 to 5 land with surveyframe 0.6 |

The validator detects the profile from the object's own shape and reports
which one it checked.

This split exists because the two were previously out of step: the reference
validator passed this repository's hand-written examples and **rejected every
real file the reference implementation produced**, on `sframe_schema_version`,
`layers` and `meta.author`. The five-layer model is the target and is not
being abandoned. The instrument profile records what is actually shipping, so
a consumer can implement against something real today.

Files carry `sframe_format` to say which shape they are. Files written before
2026-08-22 have no such field and conform to neither profile; they are
readable by surveyframe but predate format versioning.

A standalone, independently versioned JSON Schema for the `.sframe` object
defined by the [surveyframe](https://CRAN.R-project.org/package=surveyframe) R
package, plus the Derivative Citation Model that gives `.sframe` instruments a
citable, hash-based identity without issuing them individual DOIs.

This repository is decoupled from surveyframe's own release cycle on purpose:
the schema should be usable by tooling in any language, not only R, and its
version number should track schema stability, not package features.

## Why hash-based identity, not DOIs

An `.sframe` instrument is never assigned its own DOI. Its identity is a
chained SHA-256 manifest hash covering five lifecycle layers (instrument,
version/pre-registration, response, analysis and reporting, and a verification
manifest). The manifest hash is a Merkle-style chain — each layer's hash
depends on the content and hash of the layer before it — so it proves not just
that all five layers exist and are unmodified, but that they occurred in the
declared order. Citations generated from an `.sframe` object carry that hash,
not a DOI; the only DOI in any generated citation belongs to the parent
surveyframe package. See `spec.Rmd` for the full field-by-field specification
and the chain algorithm.

## Repository contents

| Path | Purpose |
|---|---|
| `schema/sframe.schema.json` | The JSON Schema, `full` profile, `v0.1-draft` |
| `schema/sframe-instrument.schema.json` | The JSON Schema, `instrument` profile, matches surveyframe 0.4.0 |
| `spec.Rmd` | Formal specification: fields, validation rules, chain algorithm, DDI/CodeMeta/PROV-O mappings |
| `validator/validate_sframe.py` | Reference validator in Python (no R dependency) |
| `examples/` | Example `.sframe`-shaped JSON at each lifecycle stage |
| `CITATION.cff` | This repository's own citation metadata |

## Relationship to surveyframe

surveyframe validates instruments against this schema; this schema does not
depend on surveyframe. The schema will not be declared stable (1.0) until
surveyframe v0.9 ships the chained Layer 5 manifest hash this schema
documents, and has been validated against real v0.9 output.

## Related work

The five-layer chained provenance framework this schema documents is
described in Sharafuddin (2026), *Social Science Research 6.0: A
Proof-of-Integrity Framework for Tamper-Evident Survey Instruments Using an
Open-Source R Package*, SocArXiv preprint:
[10.31235/osf.io/jmbv8_v1](https://doi.org/10.31235/osf.io/jmbv8_v1).

## Licence

CC BY 4.0 for the specification and schema. See `LICENSE`.
