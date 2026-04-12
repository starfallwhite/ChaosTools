"""
list_models MCP 工具实现

用于获取所有可用混沌模型列表。

根据 Prompt/4.mcp/prompt8.txt 规范实现。
"""

from typing import Dict, Any

from backend.models.registry import list_models
from backend.models.api import get_all_model_schemas


def list_models_tool(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    获取所有可用模型列表

    Args:
        params: 工具参数（可选）
            - detailed: bool - 是否返回详细信息（默认 False）
        session_id: 会话ID

    Returns:
        Dict: 模型列表
            {
                "type": "model_list",
                "data": {
                    "models": ["electrooptic_feedback", ...],
                    "schemas": {...}  # 可选，当 detailed=True
                }
            }
    """
    # 获取参数
    detailed = params.get("detailed", False)

    # 获取模型列表
    models = list_models()

    # 构建结果
    result = {
        "type": "model_list",
        "data": {
            "models": models
        }
    }

    # 如果需要详细信息，添加 schema
    if detailed:
        schemas = get_all_model_schemas()
        result["data"]["schemas"] = schemas

    return result


def get_model_params_tool(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    获取特定模型的参数 schema

    Args:
        params: 工具参数
            - model: str - 模型名称
        session_id: 会话ID

    Returns:
        Dict: 模型参数 schema
    """
    from backend.models.api import get_model_info

    model_name = params.get("model")

    if model_name is None:
        return {"error": "model parameter required"}

    try:
        info = get_model_info(model_name)
        return {
            "type": "model_params",
            "data": info
        }
    except KeyError:
        return {"error": f"model '{model_name}' not found"}


# 注册到 MCP registry
from backend.mcp.registry import tool_registry
tool_registry.register("list_models", list_models_tool)
tool_registry.register("get_model_params", get_model_params_tool)