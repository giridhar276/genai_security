import json
import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = Path(__file__).with_name("mcp_config.json")
EXPECTED_COMMAND = "npx"
EXPECTED_PACKAGE = "@modelcontextprotocol/server-github@2025.4.8"

def resolve_env_value(value):
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        variable_name = value[2:-1]
        resolved = os.getenv(variable_name)
        if not resolved:
            raise ValueError(f"Missing environment variable: {variable_name}")
        return resolved
    return value

def validate_server_config(github):
    if github.get("command") != EXPECTED_COMMAND:
        raise ValueError("BLOCK: Untrusted MCP server command")
    args = github.get("args", [])
    if EXPECTED_PACKAGE not in args:
        raise ValueError("BLOCK: Untrusted or unpinned MCP server package")

def main():
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    github = config["mcpServers"]["github"]
    validate_server_config(github)
    env = os.environ.copy()
    for key, value in github.get("env", {}).items():
        env[key] = resolve_env_value(value)
    if shutil.which("npx") is None:
        raise RuntimeError("npx was not found. Install Node.js first.")
    if os.name == "nt":
        process_command = ["cmd", "/c", github["command"]] + github.get("args", [])
    else:
        process_command = [github["command"]] + github.get("args", [])
    subprocess.run(process_command, env=env, check=True)

if __name__ == "__main__":
    main()