import json
import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = Path(__file__).with_name("mcp_config.json")

def resolve_env_value(value):
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        variable_name = value[2:-1]
        resolved = os.getenv(variable_name)
        if not resolved:
            raise ValueError(f"Missing environment variable: {variable_name}")
        return resolved
    return value

def main():
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    github = config["mcpServers"]["github"]
    command = github["command"]
    args = github.get("args", [])
    env = os.environ.copy()
    for key, value in github.get("env", {}).items():
        env[key] = resolve_env_value(value)
    if shutil.which("npx") is None:
        raise RuntimeError("npx was not found. Install Node.js first.")
    if os.name == "nt":
        process_command = ["cmd", "/c", command] + args
    else:
        process_command = [command] + args
    subprocess.run(process_command, env=env, check=True)

if __name__ == "__main__":
    main()