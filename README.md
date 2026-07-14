# sframe-schema

**Status: `v0.1-draft` — not stable. Do not treat as a frozen standard.**

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
| `schema/sframe.schema.json` | The JSON Schema, `v0.1-draft` |
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
