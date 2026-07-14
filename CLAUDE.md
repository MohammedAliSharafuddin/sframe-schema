# CLAUDE.md -- sframe-schema

This repository holds the standalone `.sframe` JSON Schema and the Derivative
Citation Model it defines. It is independently versioned (SemVer, decoupled
from the surveyframe R package) so third-party tooling in any language can
depend on the schema without depending on R.

Read `portfolio-planner/CLAUDE.md` and
`portfolio-planner/development_instructions/07_v08_v09_implementation.md`
first — this repository implements the schema side of the provenance work
planned there. `portfolio-planner/decisions.md` (2026-07-14 entry) records why
this repository exists and what it deliberately does not do.

---

## Status: v0.1-draft (not stable)

Created 2026-07-14 as a dated placeholder to establish public precedence for
the schema's identity and naming, ahead of the chained Layer 5 algorithm it
documents being finalised in surveyframe v0.9. **Nothing in this repository is
a frozen standard yet.** Fields, the chain algorithm, and the citation model
may all still change before 1.0.

1.0 is declared only when:
- surveyframe v0.9 ships with the chained (not sorted-then-concatenated)
  Layer 5 manifest hash described in
  `portfolio-planner/development_instructions/07_v08_v09_implementation.md`.
- The schema in this repository has been validated against real v0.9 output,
  not synthetic placeholders.
- The MethodsX submission is ready to reference it as stable.

Do not cite this repository's schema as authoritative before the 1.0 tag
exists. Do not register the FAIRsharing "Standard" record or a Zenodo DOI
version until 1.0.

---

## What this schema is not

- Not a CRAN dependency of surveyframe. surveyframe validates instruments
  against this schema; this schema does not import or require surveyframe.
- Not a source of instrument identity. Identity is the chained Layer 5
  manifest root hash computed by surveyframe itself. This repository defines
  the *shape* of that hash's container, not the hash.
- Not a DOI-issuing mechanism for individual instruments. Individual `.sframe`
  instruments never get their own DOI (see the Derivative Citation Model
  section below). Only this repository, as a whole, gets a DOI (once
  registered at 1.0), and only the parent surveyframe package gets a DOI in
  any generated citation.

---

## Repository layout

- `schema/sframe.schema.json` — the JSON Schema itself. `v0.1-draft`.
- `spec.Rmd` — the formal, language-agnostic specification document: field
  definitions, validation rules, the five-layer chain algorithm, and mappings
  to DDI, CodeMeta, and PROV-O. Renders to a citable spec document independent
  of the R package's own vignettes.
- `validator/validate_sframe.py` — a non-R reference validator (Python,
  `jsonschema`), so the schema is demonstrably usable outside the R ecosystem.
  This is also the validator the MethodsX paper's "Validation" section
  references.
- `examples/` — example `.sframe`-shaped JSON at each of the five lifecycle
  stages (draft through fully verified), for the validator and the spec to
  exercise.
- `CITATION.cff` — this repository's own citation metadata, separate from
  `surveyframe`'s `CITATION.cff`. Carries this repository's own DOI once
  registered; never the instrument-level hash.

---

## Conventions (inherited from the ecosystem)

- No em-dashes, en-dashes, semicolons, or ellipses in any prose. No "not X but
  Y" constructions. UK spellings.
- Do not invent or cite unverified references. Every DOI, hash, and example
  value in this repository is either real or explicitly marked as a
  placeholder (`<PLACEHOLDER>`) — never a fabricated-but-plausible-looking
  value.
- Commit or push only when asked. Never add a Co-Authored-By trailer or any
  AI-attribution line to commit messages.
- When this repository and `portfolio-planner` disagree, the planner is
  authoritative. Update the planner first, then this file.

---

## Relationship to the three publication tracks

- **SSR 6.0** (`ssr60-integrity-framework`, unchanged, DOI
  10.31235/osf.io/jmbv8_v1): describes the five-layer application. This
  repository does not restate that paper's content.
- **MethodsX**: the schema-standard paper this repository directly supports.
  Submits once this repository reaches 1.0.
- **JOI**: cites both of the above plus this repository, framing the
  Derivative Citation Model as informetric infrastructure. Submits after
  MethodsX.

Full detail: `portfolio-planner/development_instructions/12_publications_citations.md`.
