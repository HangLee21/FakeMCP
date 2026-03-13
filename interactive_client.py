import json
import subprocess
from typing import Any, Dict


class MCPClient:
    def __init__(self, server_cmd):
        self.proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        self.request_id = 1
        startup = self.proc.stdout.readline().strip()
        print(f"[server] {startup}")

    def call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        req = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        self.request_id += 1

        print("\n--- MCP Request ---")
        print(json.dumps(req, indent=2, ensure_ascii=False))

        self.proc.stdin.write(json.dumps(req, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

        line = self.proc.stdout.readline().strip()
        resp = json.loads(line)

        print("--- MCP Response ---")
        print(json.dumps(resp, indent=2, ensure_ascii=False))
        return resp

    def list_tools(self):
        return self.call("tools/list", {})

    def tool(self, name: str, arguments: Dict[str, Any]):
        return self.call("tools/call", {"name": name, "arguments": arguments})

    def close(self):
        self.proc.terminate()


def extract_content(resp):
    if "result" not in resp:
        return None
    content = resp["result"].get("content", [])
    if not content:
        return None
    item = content[0]
    if item["type"] == "json":
        return item["json"]
    if item["type"] == "text":
        return item["text"]
    return item


def print_llm(msg: str):
    print(f"\n[Mock LLM] {msg}")


def auto_fix(client: MCPClient):
    print_llm("Loading bugfix skill first.")
    skill_resp = client.tool("load_skill", {"name": "bugfix_skill"})
    skill_text = extract_content(skill_resp)
    print_llm(skill_text)

    issue_resp = client.tool("show_issue", {"issue_id": 1})
    issue = extract_content(issue_resp)
    print_llm(f"Issue: {issue['title']}")

    related = issue.get("related_files", [])
    print_llm(f"Related files: {related}")

    for path in related:
        resp = client.tool("read_file", {"path": path})
        text = extract_content(resp)
        print(f"\n[Read: {path}]\n{text}")

    test_before = extract_content(client.tool("run_tests", {}))
    print_llm(f"Initial test summary: {test_before['summary']}")

    fixed_code = """from app.task_model import Task


def get_todos():
    tasks = []
    return [task.to_dict() for task in tasks]


def count_todos():
    return len(get_todos())
"""

    client.tool("write_file", {
        "path": "app/todo_service.py",
        "content": fixed_code
    })

    test_after = extract_content(client.tool("run_tests", {}))
    print_llm(f"Final test summary: {test_after['summary']}")

    if test_after["summary"]["failed"] == 0:
        print_llm("Bug fixed successfully.")
    else:
        print_llm("Patch incomplete.")

def auto_add_feature(client):
    """
    TODO(student):
    Implement a workflow for adding a new feature.

    Suggested workflow:
    1. Read the skill instructions
    2. Read related source files
    3. Use add_function to add a new function
    4. Update or create tests
    5. Run tests
    6. Summarize the changes
    """
    raise NotImplementedError("Student TODO: implement auto_add_feature")

def main():
    client = MCPClient(["python", "server.py"])

    print("\nCommands:")
    print("  tools")
    print("  issue")
    print("  ls app")
    print("  show app/todo_service.py")
    print("  search tasks = None")
    print("  skill bugfix_skill")
    print("  test")
    print("  auto_fix")
    print("  reset")
    print("  exit\n")

    try:
        while True:
            q = input("User > ").strip()
            if not q:
                continue
            if q in {"exit", "quit"}:
                break

            if q == "tools":
                client.list_tools()

            elif q == "issue":
                print(json.dumps(extract_content(client.tool("show_issue", {"issue_id": 1})), indent=2, ensure_ascii=False))

            elif q.startswith("ls "):
                directory = q[3:].strip()
                print(json.dumps(extract_content(client.tool("list_files", {"directory": directory})), indent=2, ensure_ascii=False))

            elif q.startswith("show "):
                path = q[5:].strip()
                print(extract_content(client.tool("read_file", {"path": path})))

            elif q.startswith("search "):
                keyword = q[7:].strip()
                print(json.dumps(extract_content(client.tool("search_files", {"keyword": keyword})), indent=2, ensure_ascii=False))

            elif q.startswith("skill "):
                name = q[6:].strip()
                print(extract_content(client.tool("load_skill", {"name": name})))

            elif q == "test":
                print(json.dumps(extract_content(client.tool("run_tests", {})), indent=2, ensure_ascii=False))

            elif q == "reset":
                print(extract_content(client.tool("reset_project", {})))

            elif q == "auto_fix":
                auto_fix(client)

            elif q.startswith("add_function "):
                # TODO(student):
                # Parse command arguments and call the MCP tool
                pass
            else:
                print("Unknown command.")

    finally:
        client.close()


if __name__ == "__main__":
    main()