"""
MCP 执行器

核心执行逻辑：接收请求 -> 调用工具 -> 返回响应。
"""

from .registry import tool_registry
from .session import session_manager
from .types import ToolRequest, ToolResponse


def execute_tool(request: ToolRequest) -> ToolResponse:
    """
    执行工具调用

    Args:
        request: 工具请求对象

    Returns:
        ToolResponse: 工具响应对象
    """
    # 检查工具是否存在
    tool_func = tool_registry.get(request.tool)

    if tool_func is None:
        return ToolResponse(
            status="error",
            data={"message": f"工具 '{request.tool}' 未注册"},
            session_id=request.session_id
        )

    # 执行工具
    try:
        result = tool_func(request.params, request.session_id)

        return ToolResponse(
            status="success",
            data=result,
            session_id=request.session_id
        )

    except Exception as e:
        return ToolResponse(
            status="error",
            data={"message": f"执行错误: {str(e)}"},
            session_id=request.session_id
        )


def execute_tool_simple(tool: str, params: dict, session_id: str = None) -> dict:
    """
    简化执行接口

    直接返回字典格式，适合快速调用。

    Args:
        tool: 工具名称
        params: 工具参数
        session_id: 会话ID（可选）

    Returns:
        dict: 执行结果
    """
    request = ToolRequest(tool, params, session_id)
    response = execute_tool(request)
    return response.to_dict()