"""
MCP Session 管理

关键模块：管理 LLM 调用之间的状态。

LLM 是无状态的，但混沌分析需要连续性：
- 用户 → simulate → 保存结果
- 下一步 → fft（使用上一步结果）

Session 用于存储：
- last_result: 最近一次工具返回的数据
- context: 用户上下文信息
"""


import uuid
from typing import Dict, Any


class SessionManager:
    """
    Session 管理器

    管理会话状态，支持跨工具调用数据共享。
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self) -> str:
        """
        创建新会话

        Returns:
            str: 会话ID
        """
        sid = str(uuid.uuid4())
        self.sessions[sid] = {
            "created_at": None,  # 可扩展
            "last_result": None,
            "context": {}
        }
        return sid

    def get(self, sid: str) -> Dict[str, Any]:
        """
        获取会话数据

        Args:
            sid: 会话ID

        Returns:
            Dict: 会话数据（若不存在返回空字典）
        """
        return self.sessions.get(sid, {})

    def set(self, sid: str, key: str, value: Any) -> None:
        """
        设置会话数据

        Args:
            sid: 会话ID
            key: 数据键
            value: 数据值
        """
        if sid not in self.sessions:
            self.sessions[sid] = {}
        self.sessions[sid][key] = value

    def get_last_result(self, sid: str) -> Dict[str, Any]:
        """
        获取最近一次工具返回结果

        关键方法：用于 fft/lyapunov 等分析工具获取上一步的仿真数据。

        Args:
            sid: 会话ID

        Returns:
            Dict: 最近结果数据
        """
        return self.get(sid).get("last_result", {})

    def set_last_result(self, sid: str, result: Dict[str, Any]) -> None:
        """
        设置最近结果

        Args:
            sid: 会话ID
            result: 结果数据
        """
        self.set(sid, "last_result", result)

    def exists(self, sid: str) -> bool:
        """
        检查会话是否存在

        Args:
            sid: 会话ID

        Returns:
            bool: 是否存在
        """
        return sid in self.sessions

    def clear(self, sid: str) -> None:
        """
        清除会话

        Args:
            sid: 会话ID
        """
        if sid in self.sessions:
            del self.sessions[sid]

    def clear_all(self) -> None:
        """清除所有会话"""
        self.sessions.clear()


# 创建全局实例
session_manager = SessionManager()