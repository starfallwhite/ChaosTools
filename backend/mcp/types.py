"""
MCP 基础数据类型

定义 ToolRequest 和 ToolResponse 数据结构。
"""


class ToolRequest:
    """
    工具请求封装

    LLM 发起的工具调用请求。

    Attributes:
        tool: 工具名称
        params: 工具参数
        session_id: 会话ID（用于状态管理）
    """

    def __init__(self, tool: str, params: dict, session_id: str = None):
        self.tool = tool
        self.params = params
        self.session_id = session_id

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "tool": self.tool,
            "params": self.params,
            "session_id": self.session_id
        }


class ToolResponse:
    """
    工具响应封装

    工具执行后的返回结果。

    Attributes:
        status: 执行状态 ("success" | "error")
        data: 返回数据
        session_id: 会话ID
    """

    def __init__(self, status: str, data: dict, session_id: str):
        self.status = status
        self.data = data
        self.session_id = session_id

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "status": self.status,
            "data": self.data,
            "session_id": self.session_id
        }

    def is_success(self) -> bool:
        """判断是否成功"""
        return self.status == "success"