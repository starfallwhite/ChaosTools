"""
phase_reconstruct 工具实现

MCP Tool: 相空间重构（delay embedding）。

根据 Prompt/4.mcp/prompt5.txt 规范实现。
"""

import numpy as np
from typing import Dict, Any

from backend.mcp.session import session_manager


def phase_reconstruct(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    相空间重构（delay embedding）

    将一维时间序列重构为多维相空间。

    Args:
        params: 工具参数
            {
                "tau": 10,      # 延迟时间（采样点数）
                "dim": 2        # 嵌入维度
            }
        session_id: 会话ID

    Returns:
        Dict: 相空间数据
            {
                "type": "phase_space",
                "data": {
                    "points": [[x1, x2], [x1, x2], ...]  # M x dim
                }
            }
    """
    # 获取参数
    tau = params.get("tau", 10)
    dim = params.get("dim", 2)

    # 从 session 获取原始时序数据
    session_data = session_manager.get(session_id)

    # 优先使用 original_timeseries（chaos_simulate 保存的原始数据）
    data = session_data.get("original_timeseries")
    if data is None:
        data = session_data.get("last_result")

    if data is None:
        return {"error": "no data"}

    # 获取时序数据（兼容两种格式）
    raw_data = data.get("_raw_data", data.get("data", {}))
    x = np.array(raw_data.get("x", []))
    N = len(x)

    # 计算重构后的点数
    M = N - (dim - 1) * tau

    if M <= 0:
        return {"error": "invalid parameters - tau or dim too large"}

    # Delay embedding
    embedded = np.zeros((M, dim))

    for i in range(dim):
        embedded[:, i] = x[i * tau: i * tau + M]

    # 构建结果
    result = {
        "type": "phase_space",
        "data": {
            "points": embedded.tolist()
        }
    }

    # 存回 session
    session_manager.set(session_id, "last_result", result)

    # 返回 LLM友好格式
    return make_phase_space_llm_friendly(result, tau, dim)


def make_phase_space_llm_friendly(data: Dict[str, Any], tau: int, dim: int) -> Dict[str, Any]:
    """
    将相空间数据转换为 LLM友好格式

    Args:
        data: 原始相空间数据
        tau: 延迟参数
        dim: 嵌入维度

    Returns:
        Dict: LLM友好格式
    """
    inner_data = data.get("data", {})
    points = np.array(inner_data.get("points", []))

    M, D = points.shape if len(points) > 0 else (0, 0)

    # 统计摘要
    summary = {
        "num_points": M,
        "embedding_dim": dim,
        "delay_tau": tau,
        "range": {
            "x1": [float(np.min(points[:, 0])), float(np.max(points[:, 0]))] if M > 0 else [0, 0],
            "x2": [float(np.min(points[:, 1])), float(np.max(points[:, 1]))] if dim > 1 and M > 0 else [0, 0]
        }
    }

    # 数据预览（前100个点）
    preview_size = min(100, M)
    data_preview = points[:preview_size].tolist()

    return {
        "type": "phase_space",
        "summary": summary,
        "data_preview": data_preview,
        "full_data_ref": "session://last_result",
        "_raw_data": inner_data
    }


# 注册到 MCP registry
from backend.mcp.registry import tool_registry
tool_registry.register("phase_reconstruct", phase_reconstruct)