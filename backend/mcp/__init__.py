"""
MCP 模块

Model Context Protocol - LLM Tool Interface Layer

职责：
1. 向 LLM 暴露工具（tool schema）
2. 接收 LLM 的 tool call
3. 调度对应 skill
4. 返回结构化结果
"""

from .types import ToolRequest, ToolResponse
from .registry import tool_registry, ToolRegistry
from .session import session_manager, SessionManager
from .executor import execute_tool
from .schema import get_all_schemas, register_schema
from .server import mcp_server, MCPServer, call_tool

__all__ = [
    "ToolRequest",
    "ToolResponse",
    "tool_registry",
    "ToolRegistry",
    "session_manager",
    "SessionManager",
    "execute_tool",
    "get_all_schemas",
    "register_schema",
    "mcp_server",
    "MCPServer",
    "call_tool"
]