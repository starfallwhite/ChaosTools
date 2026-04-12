"""
模型 API 接口

提供模型参数 schema 查询接口，用于前端动态生成参数 UI。

根据 Prompt/4.mcp/prompt6.txt 规范实现。
"""

from typing import Dict, Any

from .registry import MODEL_REGISTRY


def get_all_model_schemas() -> Dict[str, Dict[str, Any]]:
    """
    获取所有模型的参数 schema

    用于前端动态生成参数 UI。

    Returns:
        Dict: 模型名称 -> 参数 schema
            {
                "electrooptic_feedback": {
                    "T1": {"type": "float", "default": 1.0, "description": "..."},
                    "xin": {"type": "array", "default": [0.1, 0.1], "description": "..."},
                    ...
                },
                ...
            }
    """
    result = {}

    for name in MODEL_REGISTRY.list():
        model = MODEL_REGISTRY.get(name)
        result[name] = model.param_schema

    return result


def get_model_schema(name: str) -> Dict[str, Any]:
    """
    获取特定模型的参数 schema

    Args:
        name: 模型名称

    Returns:
        Dict: 参数 schema

    Raises:
        KeyError: 模型不存在
    """
    model = MODEL_REGISTRY.get(name)
    return model.param_schema


def get_model_info(name: str) -> Dict[str, Any]:
    """
    获取模型完整信息（名称 + 描述 + schema）

    Args:
        name: 模型名称

    Returns:
        Dict: 模型信息
    """
    model = MODEL_REGISTRY.get(name)
    return model.get_param_info()


def get_all_models_info() -> list:
    """
    获取所有模型的完整信息列表

    Returns:
        list: 模型信息列表
    """
    return MODEL_REGISTRY.get_all_info()