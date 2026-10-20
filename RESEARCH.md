# Research —20 October2026

Demand is **inferred**, not a verified request for this tool. A list of durations hides which predecessor sets the finish and which tasks can move without delaying the project.

## Observed comparables

Query `critical path`, GitHub repository search sorted by Most stars: [exact search](https://github.com/search?q=critical+path&type=repositories&s=stars&o=desc). The highest-star relevant comparable found in this research pool is `networkx/networkx`; this is not an exhaustive global ranking.

| Repository | Stars observed | Last push | License metadata | Workflow / scope |
| --- | ---: | --- | --- | --- |
| [networkx/networkx](https://github.com/networkx/networkx) | 17341 | 2026-10-16T22:01:28Z | NOASSERTION | General Python graph algorithms, including DAG longest paths. |
| [taskjuggler/TaskJuggler](https://github.com/taskjuggler/TaskJuggler) | 817 | 2025-07-28T18:41:08Z | GPL-2.0 | Ruby project scheduler with resource and planning capabilities. |
| [chrisspen/criticalpath](https://github.com/chrisspen/criticalpath) | 27 | 2018-07-01T10:57:55Z | unknown | Python critical-path library with nested task nodes and example network; last push2018. |

## Workflow choice and tradeoffs

Release coordinators reviewing a small dependency schedule before setting a deadline. Compute earliest/latest task times, total/free slack, binding predecessor evidence and one longest-chain witness with explicit finish-to-start lags.

capacity-cut-report allocates pool capacity by max flow, task-queue runs asynchronous work, and systemd-order-audit checks ordering. This computes time and deadline slack, with no execution or resource assignment.

This is a bounded dedicated report with an invented fixture and zero runtime dependencies. The established tools are broader; choose them when their ecosystem, formats or capabilities match the job. Our own installed example proves only our documented behavior. Competitor clean installs, time to first useful result, support response times, reliability and equivalent-workload performance were not measured. Current docs offer install/usage guidance; sampled issue activity is preserved as evidence, not a support-quality score. No feature absence or superiority is claimed.

## Coverage and evidence

The keyword search includes irrelevant results (SQL knowledge graphs, CSS critical paths, routing deployment projects and regex engines). Relevant comparables were also found directly; filtering was based on current README scope. [Exact dated metadata and issue samples](RESEARCH_PROVENANCE.json). Own acceptance and distinction: [brief](BRIEF.json). No implementation, branding or prose was copied.
