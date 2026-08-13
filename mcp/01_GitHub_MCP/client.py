
import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
SERVER_FILE = Path(__file__).with_name("server.py").resolve()
openai_client = OpenAI()

def mcp_tools_to_openai(mcp_tools):
    tools = []
    for tool in mcp_tools:
        schema = tool.inputSchema if isinstance(tool.inputSchema, dict) else tool.inputSchema.model_dump()
        tools.append({"type": "function", "function": {"name": tool.name, "description": tool.description or f"GitHub MCP tool: {tool.name}", "parameters": schema}})
    return tools

def tool_result_to_text(result):
    parts = []
    for item in result.content:
        if hasattr(item, "text"):
            parts.append(item.text)
        else:
            parts.append(str(item))
    return "\n".join(parts)

def validate_arguments(tool_name, arguments):
    if tool_name == "search_repositories" and not str(arguments.get("query", "")).strip():
        return False, "Search query cannot be empty"
    if tool_name == "search_code" and not str(arguments.get("q", arguments.get("query", ""))).strip():
        return False, "Code search query cannot be empty"
    if tool_name == "create_repository" and not str(arguments.get("name", "")).strip():
        return False, "Repository name is required"
    return True, "OK"

async def run():
    server_params = StdioServerParameters(command=sys.executable, args=[str(SERVER_FILE)], env=os.environ.copy())
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            openai_tools = mcp_tools_to_openai(mcp_tools)
            print("\nGitHub MCP connected.")
            print("Tools discovered:", len(mcp_tools))
            for tool in mcp_tools:
                print("-", tool.name)
            print("\nGive GitHub instructions in normal English.")
            print('Example: Create a private repository named mcp-demo and initialize it with a README.')
            print("Type exit to stop.\n")
            messages = [{"role": "system", "content": "You are a GitHub assistant. Use the available GitHub MCP tools to complete the user's request. Choose tools automatically from the user's natural-language instruction. When a tool is needed, call it instead of only describing what to do. Never call search_repositories with an empty query. Extract the search term from the user's instruction. Use create_repository when the user asks to create a repository. Use search_repositories only when the user asks to search for repositories. Always provide all required tool arguments."}]
            while True:
                instruction = input("You: ").strip()
                if instruction.lower() in {"exit", "quit"}:
                    break
                if not instruction:
                    continue
                messages.append({"role": "user", "content": instruction})
                for _ in range(8):
                    response = openai_client.chat.completions.create(model=MODEL, messages=messages, tools=openai_tools, tool_choice="auto")
                    message = response.choices[0].message
                    messages.append(message.model_dump(exclude_none=True))
                    if not message.tool_calls:
                        print("\nAssistant:", message.content or "Task completed.", "\n")
                        break
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments or "{}")
                        print(f"\nMCP tool: {tool_name}")
                        print("Arguments:", arguments)
                        valid, reason = validate_arguments(tool_name, arguments)
                        if not valid:
                            print("Tool validation failed:", reason)
                            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": f"VALIDATION_ERROR: {reason}. Choose the correct tool and provide all required arguments."})
                            continue
                        try:
                            result = await session.call_tool(tool_name, arguments)
                        except Exception as error:
                            error_text = str(error)
                            print("MCP tool error:", error_text)
                            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": f"MCP_TOOL_ERROR: {error_text}. Correct the arguments or choose another GitHub tool."})
                            continue
                        tool_text = tool_result_to_text(result)
                        print("Tool result:", tool_text[:2000])
                        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": tool_text})
                else:
                    print("\nStopped because the maximum agent steps were reached.\n")

if __name__ == "__main__":
    asyncio.run(run())