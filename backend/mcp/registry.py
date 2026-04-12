"""
MCP 工具注册表

管理所有可被 LLM 调用的工具。
"""

from typing import Callable, Dict, Any


class ToolRegistry:
    """
    工具注册表

    用于注册和检索工具函数。

    工具函数签名：
        def tool_func(params: dict, session_id: str) -> dict
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        """
        注册工具

        Args:
            name: 工具名称（唯一标识）
            func: 工具函数，签名: (params: dict, session_id: str) -> dict
        """
        self.tools[name] = func

    def get(self, name: str) -> Callable:
        """
        获取工具函数

        Args:
            name: 工具名称

        Returns:
            Callable: 工具函数

        Raises:
            KeyError: 工具不存在
        """
        if name not in self.tools:
            raise KeyError(f"工具 '{name}' 未注册")
        return self.tools[name]

    def list(self) -> list:
        """
        列出所有已注册工具

        Returns:
            list: 工具名称列表
        """
        return list(self.tools.keys())

    def exists(self, name: str) -> bool:
        """
        检查工具是否存在

        Args:
            name: 工具名称

        Returns:
            bool: 是否存在
        """
        return name in self.tools


# 创建全局实例
tool_registry = ToolRegistry()