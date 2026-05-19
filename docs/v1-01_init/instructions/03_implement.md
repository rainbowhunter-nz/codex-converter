# Goal
Write a prompt to implement the tool.

# Input
- docs/proposal.md: implementation plan.

# Output
- docs/prompt.md: prompt to kick off implementation.

# Step
Understand the project and write docs/prompt.md for the staring prompt for implementing the tool.

The main agent is the supervisor, which spin up subagents to implement tasks the defined in docs/tasks. The subagent should make sure the test passes before finishing. The main agent need to assemble the relevent context for the subagents, so that the subagent do not waste time and token on understanding the context. After completion, the main agent need to tick off the checkbox in the docs/progress.md and corresponding task files.

The main agent needs to complete V1 implementation without User interruption, So if you have any questions, ASK NOW.

All the python code have to pass pytest unit tests, and mypy and ruff tests. The frontend have to pass their corresponding tests as well.