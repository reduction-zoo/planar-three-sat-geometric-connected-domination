# Fixed question

```json
{
  "source": "Planar 3-SAT",
  "target": "Geometric connected domination",
  "category": "Construction open",
  "summary": "A faithful geometric construction supplies a concrete hardness route for connected coverage and communication backbones.",
  "source_definition": "Given a three-literal CNF formula together with a planar embedding of its variable-clause incidence graph, return a satisfying assignment. Return NO-SOLUTION exactly when no such witness exists. Graphs, families and strings are explicit; numerical parameters use binary encodings.",
  "target_definition": "Given explicitly represented rational points in the plane and K, return at most K points forming a connected dominating set in the graph joining points at Euclidean distance at most one. A valid output is a witness satisfying these conditions, or NO-SOLUTION exactly when none exists.",
  "required_result": "Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.",
  "acceptance": "Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.",
  "importance": "A faithful geometric construction supplies a concrete hardness route for connected coverage and communication backbones.",
  "difficulty": "Difficulty is not yet established by a construction attempt. Coordinates must connect the intended gadgets while avoiding unintended adjacencies. A drawing that leaves the whole unit-disk graph disconnected cannot encode satisfiable instances.",
  "openness": "This is a rule-completion task from the imported catalog. The requested contribution is a complete, reproducible construction, proof and implementation; the existing hardness attribution is not presented as an unsolved complexity classification. The references are leads to check, not a verified solution.",
  "literature_checked": "2026-09-18",
  "coverage": "Import inventory review of the cited sources. Primary proofs have not been independently re-audited; availability of a complete reconstruction elsewhere remains unassessed.",
  "references": [
    {
      "title": "Problem-Reductions: Planar 3-SAT \u2192 Geometric connected domination",
      "url": "https://github.com/CodingThrust/problem-reductions/issues/377",
      "note": "Upstream task and discussion checked on 2026-09-18. Reported reference: Lichtenstein, D. (1982). *Planar formulae and their uses.* SIAM J. Comput. 11(2), 329\u2013343 \u2014 specifically \u00a76 \"Geometric connected dominating set\", Theorem 5 (p. 336) together with Lemma 1 (p. 339). PDF at `docs/research/raw/lichtenstein1982.pdf`; BibTeX key `lichtenstein1982` in `docs/paper/references.bib`."
    }
  ],
  "solutions": [],
  "equation": ""
}
```
