# Goal
Write a prompt to implement the proposal.

# Input
- docs/v1-02_feedback/proposal.md
- docs/v1-02_feedback/tasks

# Output
- docs/v1-02_feedback/prompt.md: prompt to kick off implementation.

# Step
Understand the project and write docs/v1-02_feedback/prompt.md for the staring prompt for implementing the tool.

The main agent is the supervisor, which spin up subagents to implement tasks the defined in docs/v1-02_feedback/tasks. The subagent should make sure the test passes before finishing. The main agent need to assemble the relevent context for the subagents, so that the subagent do not waste time and token on understanding the context. After completion, the main agent need to tick off the checkbox in the docs/v1-02_feedback/progress.md and corresponding task files.

The main agent needs to complete V1 implementation without User interruption, So if you have any questions, ASK NOW.

All the python code have to pass pytest unit tests, and mypy and ruff tests. The frontend have to pass their corresponding tests as well.