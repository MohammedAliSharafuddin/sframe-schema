# CLAUDE.md -- sframe-schema

This repository holds the standalone `.sframe` JSON Schema and the Derivative
Citation Model it defines. It is independently versioned (SemVer, decoupled
from the surveyframe R package) so third-party tooling in any language can
depend on the schema without depending on R.

---

## Status: v0.1-draft (not stable)

Created 2026-07-14 as a dated placeholder to establish a public reference
point for the schema's identity and naming, ahead of the chained provenance
algorithm it documents being finalised in a future surveyframe release.
**Nothing in this repository is a frozen standard yet.** Fields, the chain
algorithm, and the citation model may all still change before 1.0.

1.0 is declared only when:
- The chained (not sorted-then-concatenated) manifest hash this schema
  documents has shipped in surveyframe and is stable.
- The schema in this repository has been validated against real package
  output, not synthetic placeholders.
- The examples in `examples/` have been regenerated from that real output.

Do not cite this repository's schema as authoritative before the 1.0 tag
exists. Do not register a FAIRsharing "Standard" record or a Zenodo DOI
version until 1.0.

---

## What this schema is not

- Not a CRAN dependency of surveyframe. surveyframe validates instruments
  against this schema; this schema does not import or require surveyframe.
- Not a source of instrument identity. Identity is the chained manifest root
  hash computed by surveyframe itself. This repository defines the *shape* of
  that hash's container, not the hash.
- Not a DOI-issuing mechanism for individual instruments. Individual `.sframe`
  instruments never get their own DOI (see the Derivative Citation Model
  section in `spec.Rmd`). Only this repository, as a whole, gets a DOI (once
  registered at 1.0), and only the parent software package gets a DOI in any
  citation generated from an instrument.

---

## Repository layout

- `schema/sframe.schema.json` — the JSON Schema itself. `v0.1-draft`.
- `spec.Rmd` — the formal, language-agnostic specification document: field
  definitions, validation rules, the five-layer chain algorithm, and mappings
  to DDI, CodeMeta, and PROV-O.
- `validator/validate_sframe.py` — a non-R reference validator (Python,
  `jsonschema`), so the schema is demonstrably usable outside the R ecosystem.
- `examples/` — example `.sframe`-shaped JSON at different lifecycle stages,
  for the validator and the spec to exercise. Currently synthetic; see
  `examples/README.md`.
- `CITATION.cff` — this repository's own citation metadata, separate from the
  parent package's `CITATION.cff`. Carries this repository's own DOI once
  registered; never an instrument-level hash.

---

## Conventions

- No em-dashes, en-dashes, semicolons, or ellipses in any prose. No "not X but
  Y" constructions. UK spellings.
- Do not invent or cite unverified references. Every DOI, hash, and example
  value in this repository is either real or explicitly marked as a
  placeholder (`<PLACEHOLDER>`) — never a fabricated-but-plausible-looking
  value.
- Commit or push only when asked. Never add a Co-Authored-By trailer or any
  AI-attribution line to commit messages.

---

## Related work

The five-layer chained provenance framework this schema documents is
described in: Sharafuddin, M.A. (2026). *Social Science Research 6.0: A
Proof-of-Integrity Framework for Tamper-Evident Survey Instruments Using an
Open-Source R Package.* SocArXiv preprint.
https://doi.org/10.31235/osf.io/jmbv8_v1
