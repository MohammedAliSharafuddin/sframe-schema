# Example .sframe objects

Both files here are **synthetic**: the layer content strings (e.g.
`"instrument-content-example"`) are placeholder literals, not real instrument
payloads, and the hashes are genuinely computed SHA-256 chains over those
placeholder strings (not fabricated hex). They exist to exercise the schema
and the reference validator, not to represent a real study.

- `aic_rsam_stage_5_complete.json` — all five layers present and chained,
  `lifecycle_stage: "5/5"`. Validates cleanly and reports full chain linkage.
- `aic_rsam_stage_2_draft.json` — only `instrument` and `version` present,
  no `bibliographic` block. Still schema-valid (a partial chain is not an
  invalid object), lifecycle stage `2/5`, not citable yet.

Regenerate or extend these with `python3 -c` / any SHA-256 tool following the
chain algorithm in `spec.Rmd` Section 2: `hash = SHA256(content + previous_hash)`.

Before the MethodsX submission, these placeholders must be replaced with
hashes from a real run against the shipped surveyframe v0.9, the same
discipline the SSR 6.0 preprint followed (see
`ssr60-integrity-framework/CLAUDE.md`: "SHA-256 hash values in the manuscript
must come from the actual demo script output, not invented").

## Instrument profile (added 2026-08-22)

| File | What it is |
|---|---|
| `instrument_profile_surveyframe_040.sframe` | Real output from surveyframe 0.4.0's `write_sframe()`. Validates against the `instrument` profile. Not synthetic. |
| `instrument_profile_surveyframe_040_responses.csv` | The matching response data, 80 rows. |

A `.sframe` carries the instrument only, never the responses. The two files
join on column id: every `items[].id` in the instrument is a column in the
CSV. This pairing is the shape a consuming application reads.

The other examples in this directory are hand-written illustrations of the
`full` five-layer profile, which no implementation emits yet.
