"""
chaos_simulate 工具实现

MCP Tool: 运行混沌系统数值仿真。

调用流程：
1. 从 params 获取模型名称和参数
2. 调用 Model 进行仿真
3. 结果存入 session（关键）
4. 返回 LLM友好的数据格式
"""

import numpy as np
from typing import Dict, Any

from backend.models.registry import MODEL_REGISTRY
from backend.mcp.session import session_manager


def chaos_simulate(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    执行混沌系统仿真

    Args:
        params: 工具参数
            {
                "model": "electrooptic_feedback",
                "model_params": {
                    "h": 0.01,
                    "N": 10000,
                    "T1": 1.0,
                    "beta": 2.0,
                    ...
                }
            }
        session_id: 会话ID

    Returns:
        Dict: 仿真结果（LLM友好格式）
            {
                "type": "timeseries",
                "data": {"t": [...], "x": [...]},
                "summary": {"mean": ..., "std": ..., "length": ...},
                "data_preview": [...100个点...],
                "full_data_ref": "session_id"
            }
    """
    # 获取模型名称
    model_name = params.get("model", "electrooptic_feedback")
    model_params = params.get("model_params", {})

    # 获取模型
    try:
        model = MODEL_REGISTRY.get(model_name)
    except KeyError:
        return {"error": f"model '{model_name}' not registered"}

    # 执行仿真
    result = model.simulate(model_params)

    # 存入 session（关键）
    # 保存原始数据供后续分析工具使用
    session_manager.set(session_id, "last_result", result)
    session_manager.set(session_id, "original_timeseries", result)  # 保留原始时序
    # 保存仿真参数供相空间重构等工具使用
    session_manager.set(session_id, "simulation_params", model_params)

    # 转换为 LLM友好格式
    llm_friendly_result = make_llm_friendly(result)

    return llm_friendly_result


def make_llm_friendly(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将数据转换为 LLM友好格式

    LLM 不能处理巨大数组（1e6长度），需要：
    - summary: 统计摘要
    - data_preview: 前100个点预览
    - full_data_ref: 完整数据引用

    Args:
        data: 原始数据

    Returns:
        Dict: LLM友好数据
    """
    if data.get("type") != "timeseries":
        return data

    inner_data = data.get("data", {})
    t = np.array(inner_data.get("t", []))
    x = np.array(inner_data.get("x", []))

    length = len(t)

    # 统计摘要
    summary = {
        "length": length,
        "t_range": [float(t[0]), float(t[-1])] if length > 0 else [0, 0],
        "x_mean": float(np.mean(x)) if length > 0 else 0,
        "x_std": float(np.std(x)) if length > 0 else 0,
        "x_max": float(np.max(x)) if length > 0 else 0,
        "x_min": float(np.min(x)) if length > 0 else 0
    }

    # 数据预览（前100个点）
    preview_size = min(100, length)
    data_preview = {
        "t": t[:preview_size].tolist(),
        "x": x[:preview_size].tolist()
    }

    # 完整数据引用
    full_data_ref = "session://last_result"

    return {
        "type": "timeseries",
        "summary": summary,
        "data_preview": data_preview,
        "full_data_ref": full_data_ref,
        # 保留原始数据供后续工具使用
        "_raw_data": inner_data
    }


# 注册到 MCP registry
from backend.mcp.registry import tool_registry
tool_registry.register("chaos_simulate", chaos_simulate)