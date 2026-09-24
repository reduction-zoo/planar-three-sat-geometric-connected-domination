# Manuscript completion evidence

Date: 2026-09-24. Reviewed implementation freeze: `72e1365`; independent advance review committed at `42ecaab`. Writing introduced no new construction or proof mechanism and did not edit the maps, prepared corpus or independent checks. Completed after the round allocation under research-session's current-result completion rule.

Applied research-write and sci-brain:how-to-technical-writing before drafting, including its Notation/Figure Rulebooks, and reapplied the language checklist in the final pass. Preserved quantifiers, arbitrary-output recovery and reconstruction-only novelty scope. The first compile exposed a Typst multi-letter math token; compilation repaired it. Visual inspection then caught an attachment-scope error in the valid-output formula; explicit subscript grouping repaired it. Figure labels were moved clear of edges, the counting equation split across aligned lines, and reproduction commands kept together with their setup. The final manuscript uses native Typst math, three checked SVG figures, cited interfaces, complete F/G composition and a reproduction appendix.

Commands are given in the manuscript. `typst compile work/manuscript.typ work/manuscript.pdf` (with the full campaign prefix from repository root) completed without diagnostics using Typst 0.15.1. `figures/draw.py` passed its graph-interface assertions; `figures.txt` records the result. The native macOS PDFKit renderer in `render.swift` produced eight page images; `render.txt` records their dimensions and `sha256.txt` identifies the final PDF and inspected pages. Raster previews are reproducible and ignored; the PDF and SVG assets are retained.

## Page-by-page visual inspection

| Page | Checked content and outcome |
|---|---|
| 1 | Title, abstract, main theorem, native valid-output equation and source definitions; formula attachment correct, no clipping. |
| 2 | Cover budget, full clause gadget, labels and caption; exact three ports and five-vertex cover visible. |
| 3 | Face augmentation, labeled subdivision, degree categories, caption and connected-cover proof; labels clear of edges. |
| 4 | Core premise, visibility coordinates, finite-template parameters and bounds; notation legible and no overflow. |
| 5 | Grid route, connector/middle/side distinctions, target budget and normalization setup; figure and caption agree. |
| 6 | Two-line connector count, full recovery, complexity, deterministic reconstruction and conclusion; equation remains with setup. |
| 7 | Four complete references and verification scope; no unsupported novelty, negative-target or formalization claim. |
| 8 | Prerequisites/reproduction commands and both public map modes; blocks legible, no clipped paths or separated command continuations. |

All eight pages were inspected. After the final editorial revision, unchanged pages 1–3 retained their prior inspection; pages 4–8 were re-rendered and re-inspected. No layout defect remains identified. This is document inspection, not an additional mathematical or formal certificate.

## Added negative-case evidence (2026-09-24)

The reviewed F/G maps and general proof were unchanged. The verification appendix now records two target-only structural negative certificates outside the original Prepare corpus and gives their reproduction command. Typst compiled the revised source without diagnostics. PDFKit rendered eight pages at 595 × 841 pt; the updated hashes are in `sha256.txt`. Pages 7–8 were visually re-inspected: the new certificate paragraph, native math inequality, reference, command block and final reproduction text are legible, with no clipping or separated setup. Pages 1–6 are unaffected by this appendix edit. The new certificate itself has not received an independent reviewer assessment; the prior advance verdict applies to the unchanged maps and general proof.

## Final experience audit

Three distinct entries created in rounds 021–040: backend contract, separator connected-domination oracle, finite port-template stretching. Two pre-existing entries updated: connected-domination oracle scale and tsmpy face recursion. Further updates within the new entries include the independently found hash-order counterexample. Nine local entries total; zero pending extraction; zero board promotions. Remaining limits and unsuccessful runs are preserved rather than converted into solver answers.
