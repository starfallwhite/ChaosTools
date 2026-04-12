"""
FastAPI API 模块

提供 HTTP API 接口，供前端调用 MCP Server。
"""

from .routes import app, run_api_server

__all__ = [
    "app",
    "run_api_server"
]