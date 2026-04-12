"""
MCP Server 主入口

实现 MCP Server，接收 LLM 的工具调用请求。
"""

from typing import Dict, Any

from .types import ToolRequest
from .executor import execute_tool
from .session import session_manager
from .schema import get_all_schemas

# Import skills to register tools
from backend.skills import (
    chaos_simulate,
    fft_analysis,
    lyapunov_calculate,
    phase_reconstruct,
    list_models_tool,
    get_model_params_tool
)


class MCPServer:
    """
    MCP Server

    职责：
    1. 接收 LLM 的工具调用请求
    2. 管理 session
    3. 调度工具执行
    4. 返回结构化结果
    """

    def __init__(self):
        """初始化 Server"""
        pass

    def handle_request(self, req_json: dict) -> Dict[str, Any]:
        """
        处理工具调用请求

        Args:
            req_json: 请求 JSON
                {
                    "tool": "chaos_simulate",
                    "params": {...},
                    "session_id": "xxx" (可选)
                }

        Returns:
            Dict: 响应
                {
                    "status": "success" | "error",
                    "data": {...},
                    "session_id": "xxx"
                }
        """
        tool = req_json.get("tool")
        params = req_json.get("params", {})
        session_id = req_json.get("session_id")

        # 自动创建 session（若未提供）
        if session_id is None:
            session_id = session_manager.create_session()

        # 构建请求
        request = ToolRequest(tool, params, session_id)

        # 执行工具
        response = execute_tool(request)

        return response.to_dict()

    def get_tools(self) -> list:
        """
        获取所有可用工具的 Schema

        用于向 LLM 暴露工具列表。

        Returns:
            list: Schema 列表
        """
        return get_all_schemas()

    def get_session_data(self, session_id: str) -> Dict[str, Any]:
        """
        获取 session 数据

        Args:
            session_id: 会话ID

        Returns:
            Dict: session 数据
        """
        return session_manager.get(session_id)


# 创建全局实例
mcp_server = MCPServer()


# ==================== 快捷接口 ====================

def call_tool(tool: str, params: dict, session_id: str = None) -> dict:
    """
    快捷调用工具

    Args:
        tool: 工具名称
        params: 工具参数
        session_id: 会话ID（可选，自动创建）

    Returns:
        dict: 执行结果
    """
    req = {
        "tool": tool,
        "params": params,
        "session_id": session_id
    }
    return mcp_server.handle_request(req)


def get_available_tools() -> list:
    """
    获取可用工具列表

    Returns:
        list: 工具 Schema
    """
    return mcp_server.get_tools()