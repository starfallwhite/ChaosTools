"""
MCP Tool Schema 定义

定义工具的 Schema，用于向 LLM 暴露工具接口。

根据 Prompt/4.mcp 规范实现。
"""

from typing import Dict, List, Any


# 全局 Schema 存储
TOOL_SCHEMAS: List[Dict[str, Any]] = []


def register_schema(schema: dict) -> None:
    """
    注册工具 Schema

    Args:
        schema: Schema 定义
    """
    # 检查必要字段
    if "name" not in schema:
        raise ValueError("Schema must contain 'name' field")

    # 避免重复注册
    name = schema["name"]
    for existing in TOOL_SCHEMAS:
        if existing["name"] == name:
            return

    TOOL_SCHEMAS.append(schema)


def get_all_schemas() -> List[Dict[str, Any]]:
    """
    获取所有已注册的 Schema

    Returns:
        List[Dict]: Schema 列表
    """
    return TOOL_SCHEMAS


def get_schema(name: str) -> Dict[str, Any]:
    """
    获取特定工具的 Schema

    Args:
        name: 工具名称

    Returns:
        Dict: Schema 定义

    Raises:
        KeyError: Schema 不存在
    """
    for schema in TOOL_SCHEMAS:
        if schema["name"] == name:
            return schema
    raise KeyError(f"Schema '{name}' not registered")


def clear_schemas() -> None:
    """清除所有 Schema"""
    TOOL_SCHEMAS.clear()


# ==================== 预定义 Schema（符合 Prompt 规范）====================

CHAOS_SIMULATE_SCHEMA = {
    "name": "chaos_simulate",
    "description": "Simulate a chaotic system",
    "parameters": {
        "type": "object",
        "properties": {
            "model": {"type": "string"},
            "model_params": {"type": "object"}
        },
        "required": ["model", "model_params"]
    }
}

FFT_ANALYSIS_SCHEMA = {
    "name": "fft_analysis",
    "description": "Perform FFT on time series",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

LYAPUNOV_CALCULATE_SCHEMA = {
    "name": "lyapunov_calculate",
    "description": "Compute Lyapunov exponent",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

PHASE_RECONSTRUCT_SCHEMA = {
    "name": "phase_reconstruct",
    "description": "Reconstruct phase space",
    "parameters": {
        "type": "object",
        "properties": {
            "tau": {"type": "integer"},
            "dim": {"type": "integer"}
        },
        "required": []
    }
}

# prompt6-8 新增 Schema
LIST_MODELS_SCHEMA = {
    "name": "list_models",
    "description": "List all available chaos models",
    "parameters": {
        "type": "object",
        "properties": {
            "detailed": {
                "type": "boolean",
                "description": "Whether to return detailed parameter schemas"
            }
        },
        "required": []
    }
}

GET_MODEL_PARAMS_SCHEMA = {
    "name": "get_model_params",
    "description": "Get parameter schema for a specific model",
    "parameters": {
        "type": "object",
        "properties": {
            "model": {
                "type": "string",
                "description": "Model name"
            }
        },
        "required": ["model"]
    }
}


# 自动注册预定义 Schema
register_schema(CHAOS_SIMULATE_SCHEMA)
register_schema(FFT_ANALYSIS_SCHEMA)
register_schema(LYAPUNOV_CALCULATE_SCHEMA)
register_schema(PHASE_RECONSTRUCT_SCHEMA)
register_schema(LIST_MODELS_SCHEMA)
register_schema(GET_MODEL_PARAMS_SCHEMA)