# Goal
automatic versioning from git tag.

# Step
Can you make the help menu to show the version of the tool? 
if run `codex-converter --version` please show the version as well. 
make the version to be comming from the git tag? This only need to work for the github action. 
If developer clones the repo, the version should be `dev`
Please just set the version pyproject.toml to dev, and replace it when running the github action.

DO NOT implement it in a way that uses git to check the tag.
The version is only assigned on the github action, so we do not have to update it manually.