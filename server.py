import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path("demo_project")
BACKUP_ROOT = Path("demo_project_backup")


TOOLS = [
    {
        "name": "list_files",
        "description": "List files under a directory",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string"}
            },
            "required": ["directory"]
        }
    },
    {
        "name": "read_file",
        "description": "Read a file by relative path",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Overwrite a file by relative path",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "search_files",
        "description": "Search keyword in project files",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string"}
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "show_issue",
        "description": "Show a project issue by id",
        "inputSchema": {
            "type": "object",
            "properties": {
                "issue_id": {"type": "integer"}
            },
            "required": ["issue_id"]
        }
    },
    {
        "name": "load_skill",
        "description": "Load a skill instruction file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "run_tests",
        "description": "Run fake project tests and return structured results",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "reset_project",
        "description": "Reset project files from backup",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    # TODO(student): complete this tool schema
    # {
    #     "name": "add_function",
    #     "description": "...",
    #     "inputSchema": {
    #         "type": "object",
    #         "properties": {
    #             "path": {"type": "string"},
    #             "function_name": {"type": "string"},
    #             "function_code": {"type": "string"}
    #         },
    #         "required": ["path", "function_name", "function_code"]
    #     }
    # },
]


def safe_path(rel_path: str) -> Path:
    path = (PROJECT_ROOT / rel_path).resolve()
    if PROJECT_ROOT.resolve() not in path.parents and path != PROJECT_ROOT.resolve():
        raise ValueError("Path escapes project root")
    return path


def list_files(directory: str):
    root = safe_path(directory)
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if root.is_file():
        return [str(root.relative_to(PROJECT_ROOT))]
    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            files.append(str(p.relative_to(PROJECT_ROOT)))
    return files


def read_file(path: str):
    p = safe_path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return p.read_text(encoding="utf-8")


def write_file(path: str, content: str):
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return {"path": path, "bytes": len(content.encode('utf-8'))}


def search_files(keyword: str):
    matches = []
    for p in PROJECT_ROOT.rglob("*"):
        if p.is_file():
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            if keyword in text:
                matches.append(str(p.relative_to(PROJECT_ROOT)))
    return matches


def show_issue(issue_id: int):
    issue_path = PROJECT_ROOT / "issues" / f"{issue_id}.json"
    if not issue_path.exists():
        raise FileNotFoundError(f"Issue not found: {issue_id}")
    return json.loads(issue_path.read_text(encoding="utf-8"))


def load_skill(name: str):
    skill_path = PROJECT_ROOT / "skills" / name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill not found: {name}")
    return skill_path.read_text(encoding="utf-8")


def reset_project():
    if PROJECT_ROOT.exists():
        shutil.rmtree(PROJECT_ROOT)
    shutil.copytree(BACKUP_ROOT, PROJECT_ROOT)
    return "Project reset from backup."


# NOTE:
# This tool only adds a function to a file.
# It should NOT decide business logic, write tests, or run workflows.
# Those responsibilities belong to a Skill.
def add_function(path: str, function_name: str, function_code: str):
    """
    TODO(student):
    Implement this tool.

    Requirements:
    1. Read the target file
    2. Check whether the function already exists
    3. If not, append the new function definition
    4. Save the updated file
    5. Return structured metadata
    """
    raise NotImplementedError("Student TODO: implement add_function")

def run_tests():
    """
    Controlled fake test runner.
    We inspect the source and decide pass/fail deterministically.
    """
    code = read_file("app/todo_service.py")
    results = []

    if "tasks = None" in code:
        results = [
            {
                "name": "test_get_todos_returns_list",
                "status": "failed",
                "message": "TypeError: 'NoneType' object is not iterable"
            },
            {
                "name": "test_get_todos_default_empty",
                "status": "failed",
                "message": "TypeError: 'NoneType' object is not iterable"
            },
            {
                "name": "test_count_todos_default_zero",
                "status": "failed",
                "message": "TypeError: 'NoneType' object is not iterable"
            }
        ]
    elif "tasks = []" in code:
        results = [
            {"name": "test_get_todos_returns_list", "status": "passed", "message": ""},
            {"name": "test_get_todos_default_empty", "status": "passed", "message": ""},
            {"name": "test_count_todos_default_zero", "status": "passed", "message": ""}
        ]
    else:
        results = [
            {
                "name": "test_get_todos_returns_list",
                "status": "failed",
                "message": "Unexpected implementation"
            },
            {
                "name": "test_get_todos_default_empty",
                "status": "failed",
                "message": "Unexpected implementation"
            },
            {
                "name": "test_count_todos_default_zero",
                "status": "failed",
                "message": "Unexpected implementation"
            }
        ]

    passed = sum(1 for x in results if x["status"] == "passed")
    failed = sum(1 for x in results if x["status"] == "failed")
    return {
        "summary": {"passed": passed, "failed": failed, "total": len(results)},
        "results": results
    }


def ok(req_id, result):
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def err(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def handle_request(req: dict):
    method = req.get("method")
    req_id = req.get("id")

    try:
        if method == "tools/list":
            return ok(req_id, {"tools": TOOLS})

        if method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})

            if name == "list_files":
                return ok(req_id, {"content": [{"type": "json", "json": list_files(arguments["directory"])}]})

            if name == "read_file":
                return ok(req_id, {"content": [{"type": "text", "text": read_file(arguments["path"])}]})

            if name == "write_file":
                meta = write_file(arguments["path"], arguments["content"])
                return ok(req_id, {"content": [{"type": "json", "json": meta}]})

            if name == "search_files":
                matches = search_files(arguments["keyword"])
                return ok(req_id, {"content": [{"type": "json", "json": matches}]})

            if name == "show_issue":
                issue = show_issue(arguments["issue_id"])
                return ok(req_id, {"content": [{"type": "json", "json": issue}]})

            if name == "load_skill":
                skill_text = load_skill(arguments["name"])
                return ok(req_id, {"content": [{"type": "text", "text": skill_text}]})

            if name == "run_tests":
                result = run_tests()
                return ok(req_id, {"content": [{"type": "json", "json": result}]})

            if name == "reset_project":
                result = reset_project()
                return ok(req_id, {"content": [{"type": "text", "text": result}]})

            # TODO(student):
            # Register your custom tool here.
            # Example:
            # elif name == "add_function":
            #     result = add_function(
            #         arguments["path"],
            #         arguments["function_name"],
            #         arguments["function_code"]
            #     )
            #     return ok(req_id, {"content": [{"type": "json", "json": result}]})

            return err(req_id, -32601, f"Unknown tool: {name}")

        return err(req_id, -32601, f"Unknown method: {method}")

    except KeyError as e:
        return err(req_id, -32602, f"Missing argument: {e}")
    except Exception as e:
        return err(req_id, -32000, str(e))


def main():
    print("Project MCP Server started.", flush=True)
    while True:
        try:
            line = input()
            if not line.strip():
                continue
            req = json.loads(line)
            resp = handle_request(req)
            print(json.dumps(resp, ensure_ascii=False), flush=True)
        except EOFError:
            break
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32000, "message": str(e)}
            }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()