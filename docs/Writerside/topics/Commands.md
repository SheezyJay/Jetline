# Jetline Commands

Jetline includes a variety of commands for maintaining and operating your project.

## Installation

Before using any commands, make sure you've installed Jetline by running:

\`\`\`bash
pip install jetline
\`\`\`

## Commands

Here are some of the main commands you can use with the Jetline Python package.

### jetline

\`\`\`bash
jetline
\`\`\`

The `jetline` command displays information about your project.

### jetline-setup

\`\`\`bash
jetline-setup --project-name [project_name] --pipeline-name [pipeline_name]
\`\`\`

The `jetline-setup` command is used to create a new project. Optionally, specify the project name and pipeline folder name.

### jetline-create-pipe

\`\`\`bash
jetline-create-pipe
\`\`\`

The `jetline-create-pipe` command allows you to create a new pipeline in your project.

### jetline-analyze

\`\`\`bash
jetline-analyze
\`\`\`

The `jetline-analyze` command is useful for conducting an analysis of your project. It might check for things such as static code issues or performance problems.

### jetline-run

\`\`\`bash
jetline-run [args]
\`\`\`

The `jetline-run` command facilitates the starting or running of your pipelines. The `args` should be replaced by any parameters the pipeline might need.

### jetline-to-exe

\`\`\`bash
jetline-to-exe
\`\`\`

The `jetline-to-exe` command is intended to transform your project into an executable file.

## Note

Don't forget to replace the placeholders like `[project_name]`, `[pipeline_name]`, and `[args]` with your actual values while using the commands.

For further usage information on any individual command, you can always use the help flag `-h` or `--help` following any command to get more details, for example:

\`\`\`bash
jetline-setup --help
\`\`\`