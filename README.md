README.md
# MCP Demo Project: AI Tools & Skills Workshop

This project is a **teaching demo for Model Context Protocol (MCP)**.

It demonstrates how an AI system can interact with a software project by calling **Tools** and executing **Skills** to complete tasks such as fixing bugs or adding new features.

The repository contains a small Todo application and a simulated MCP server.  
Students will implement their own **Tools** and **Skills** on top of this framework.

---

# Project Goals

This project helps students understand three key concepts:

### Prompt
A prompt describes **what the AI should do**.

### Tool
A tool performs **a single concrete action**, such as:

- reading a file
- writing code
- running tests

### Skill
A skill defines **a workflow of multiple steps**, for example:

1. Read an issue
2. Inspect code
3. Modify the implementation
4. Update tests
5. Run tests again

Skills are implemented using multiple tool calls.

---

# Repository Structure


FakeMcp/
├── server.py
├── interactive_client.py
├── demo_project/
│ ├── app/
│ │ ├── main.py
│ │ ├── task_model.py
│ │ └── todo_service.py
│ ├── tests/
│ │ └── test_todo_service.py
│ ├── issues/
│ │ ├── 1.json
│ │ └── 2.json
│ └── skills/
│ ├── bugfix_skill/
│ │ ├── SKILL.md
│ │ └── REFERENCE.md
│ └── add_feature_skill/
│ └── SKILL.md
└── demo_project_backup/


### server.py

Simulated MCP server.

It exposes project capabilities as **Tools**.

Examples of built-in tools:

- `read_file`
- `write_file`
- `run_tests`
- `load_skill`
- `list_files`

Students will implement new tools here.

---

### interactive_client.py

A simple interactive MCP client.

It simulates how an AI agent interacts with the MCP server.

You can type commands to trigger tool calls and workflows.

---

### demo_project

A small Todo application used for experiments.

It contains:

- application code
- unit tests
- issues
- skill definitions

---

### demo_project_backup

Backup copy of the project.

Used to reset the project state during demonstrations.

---

# How MCP Works in This Project

The interaction flow is:


User
↓
Client (simulated AI agent)
↓
MCP Request
↓
MCP Server
↓
Tool Execution
↓
Project Files / Tests / Skills


Example workflow:


Read issue
→ Read source code
→ Modify implementation
→ Run tests
→ Verify results


---

# Running the Demo

Make sure Python is installed.

Then run:

```bash
python interactive_client.py

You should see:

Project MCP Server started.
Example Commands
List available tools
tools
Show issue description
issue
Read source code
show app/todo_service.py
Run tests
test
Run automatic bug fix workflow
auto_fix
Reset the project state
reset
Assignment: Implement Your Own Tool

Students must implement a new MCP Tool:

add_function(path, function_name, function_code)

Goal:

Insert a new Python function into the specified file.

The implementation should:

Read the target file

Check whether the function already exists

Append the function definition

Save the updated file

TODO locations are provided in:

server.py
Assignment: Implement a Skill

Students must create a new skill:

add_feature_skill

Goal:

Add a new feature to the Todo application.

Feature:

count_completed_tasks(tasks)

The skill should perform the following workflow:

Read the issue description

Inspect the source code

Use add_function to insert the new function

Add or update test cases

Run tests

Verify the result

Skill instructions should be written in:

demo_project/skills/add_feature_skill/SKILL.md
Learning Objectives

After completing this project, students should understand:

What MCP is

How AI systems call external tools

How tools expose structured capabilities

How skills organize complex workflows

How AI-assisted development works in practice

Suggested Extensions

Students can extend this system by implementing additional tools:

Examples:

search_issue
apply_patch
create_file
list_skills
summarize_issue

Or create new skills such as:

test_writer_skill
code_review_skill
refactor_skill
Notes

This project simulates an AI development workflow.

The MCP server is simplified for educational purposes.

In real systems, MCP servers may connect to:

GitHub repositories

databases

cloud services

CI pipelines