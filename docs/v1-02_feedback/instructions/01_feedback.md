# Goal
Generate a proposal according to the feedback

# Output
- docs/v1-02_feedback/proposal.md

# Step

Read the feedback:

1. The converted toml contains very long single line. Please format it so that it's easy to read.
2. Make the conversion report table colorful to improve readablity.
3. Add option to convert the settings.local.json as well. If enabled, just merge them and put them into the config.toml. the setting.local.json have higher priority.
4. Review the output and try to improve it.
5. Add a flag to put the generated files into .gitignore.
6. add a verb `clean` to clean the generated files.