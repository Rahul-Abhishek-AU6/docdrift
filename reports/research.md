# Research: documentation drift after AI-assisted changes

Researched: 2026-11-03.

AI code use is routine, but validation remains expensive. Stack Overflow's
2025 survey reports more developers distrust AI accuracy (46%) than trust it
(33%), and 66% cite "almost right" output as a frustration.
[Source](https://survey.stackoverflow.co/2025/ai). In the 2026 survey,
documentation remains one of the trusted places developers look for answers
(60%), while 75% say quality/safety validation is a larger responsibility with
AI-generated output. [Source](https://d3bdzitctqoj2j.cloudfront.net/teams/software-development/state-of-developer-experience-2026)

## Selected problem: DocDrift

AI-assisted changes can add/remove CLI flags, environment variables, and
configuration keys without updating the README, examples, or docs. Reviewers
need a cheap, local reminder of which public-facing tokens changed and where
they are (or are not) documented.

DocDrift will read a local Git diff or explicit unified patch, extract changed
`--flags`, `UPPER_CASE_ENV` variables, and JSON/YAML-like configuration keys,
then search README/docs/examples for each token. It creates an auditable
Markdown/JSON receipt. It does not prove documentation correctness, execute
code, call a model, or send data anywhere.

This is distinct from the factory's prior outputs: it checks documentation
parity rather than test impact, agent-instruction files, or API consumers.
