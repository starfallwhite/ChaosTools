"""
FastAPI 接口层

将 MCP Server 暴露为 HTTP API，供前端调用。

根据 Prompt/6.frontend/prompt13.txt 规范实现。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from backend.mcp.server import mcp_server
from backend.models.api import get_all_model_schemas, get_all_models_info

# 创建 FastAPI 应用
app = FastAPI(
    title="Chaos Analysis API",
    description="混沌系统仿真与分析 API",
    version="0.1.0"
)

# 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 基础接口 ====================

@app.get("/")
def root() -> Dict[str, Any]:
    """
    健康检查

    Returns:
        Dict: 服务状态
    """
    return {"status": "ok", "service": "Chaos Analysis API"}


@app.get("/health")
def health() -> Dict[str, Any]:
    """
    健康检查端点

    Returns:
        Dict: 服务状态
    """
    return {"status": "healthy"}


# ==================== MCP 调用接口 ====================

@app.post("/mcp")
def call_mcp(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP 工具调用接口

    Args:
        req: MCP 请求
            {
                "tool": "chaos_simulate",
                "params": {...},
                "session_id": "..."  // 可选
            }

    Returns:
        Dict: MCP 响应
            {
                "status": "success" | "error",
                "data": {...},
                "session_id": "..."
            }
    """
    return mcp_server.handle_request(req)


@app.get("/mcp/tools")
def get_tools() -> list:
    """
    获取所有可用 MCP 工具

    Returns:
        list: 工具 Schema 列表
    """
    return mcp_server.get_tools()


# ==================== 模型接口 ====================

@app.get("/models")
def get_models() -> Dict[str, Any]:
    """
    获取所有模型及其参数 schema

    用于前端动态生成参数 UI。

    Returns:
        Dict: 模型名称 -> 参数 schema
    """
    return get_all_model_schemas()


@app.get("/models/info")
def get_models_info() -> list:
    """
    获取所有模型的完整信息

    Returns:
        list: 模型信息列表
    """
    return get_all_models_info()


# ==================== 启动入口 ====================

def run_api_server():
    """
    启动 FastAPI 服务器

    使用 uvicorn 运行。
    """
    import uvicorn
    uvicorn.run(
        "backend.api.routes:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    run_api_server()