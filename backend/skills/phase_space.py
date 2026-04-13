"""
phase_reconstruct 工具实现

MCP Tool: 相空间重构。

绘制 x(t-T1) vs x(t) 的相空间图。
T1 为仿真参数中的延迟时间，延迟点数 = T1/h。
"""

import numpy as np
from typing import Dict, Any

from backend.mcp.session import session_manager


def phase_reconstruct(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    相空间重构

    绘制 x(t-T1) vs x(t) 的关系图。
    使用仿真参数中的 T1（延迟时间）和 h（步长）计算延迟点数。

    Args:
        params: 工具参数（可选，可覆盖默认值）
            {
                "tau": None,  # 可选，覆盖延迟点数（默认使用 T1/h）
                "dim": 2      # 嵌入维度（默认 2）
            }
        session_id: 会话ID

    Returns:
        Dict: 相空间数据
            {
                "type": "phase_space",
                "data": {
                    "x_delay": [...],  # x(t-T1)
                    "x_current": [...]  # x(t)
                },
                "summary": {
                    "n_delay": ...,  # 延迟点数 T1/h
                    "T1": ...,       # 延迟时间
                    "h": ...         # 步长
                }
            }
    """
    # 获取参数
    dim = params.get("dim", 2)  # 嵌入维度，默认为 2

    # 从 session 获取原始时序数据
    session_data = session_manager.get(session_id)

    # 获取仿真参数（关键：获取 T1 和 h）
    sim_params = session_data.get("simulation_params", {})
    T1 = sim_params.get("T1", 15e-9)  # 延迟时间
    h = sim_params.get("h", 1e-11)    # 步长

    # 计算延迟点数
    n_delay = int(np.floor(T1 / h))

    # 用户可覆盖 tau
    tau = params.get("tau")
    if tau is not None:
        n_delay = int(tau)

    # 获取原始时序数据
    data = session_data.get("original_timeseries")
    if data is None:
        data = session_data.get("last_result")

    if data is None:
        return {"error": "no data. Run chaos_simulate first."}

    # 获取时序数据
    raw_data = data.get("_raw_data", data.get("data", {}))
    x = np.array(raw_data.get("x", []))
    N = len(x)

    if N <= n_delay:
        return {"error": f"insufficient data: N={N}, n_delay={n_delay}"}

    # 相空间重构：x(t-T1) vs x(t)
    # x_delay = x[0 : N-n_delay]  对应 x(t-T1)
    # x_current = x[n_delay : N]  对应 x(t)
    x_delay = x[:N - n_delay]
    x_current = x[n_delay:]
    M = len(x_delay)

    # 构建结果
    result = {
        "type": "phase_space",
        "data": {
            "x_delay": x_delay.tolist(),
            "x_current": x_current.tolist()
        },
        "summary": {
            "num_points": M,
            "n_delay": n_delay,
            "T1": T1,
            "h": h,
            "T1_ns": T1 * 1e9  # 转换为纳秒显示
        }
    }

    # 存回 session
    session_manager.set(session_id, "last_result", result)

    # 返回 LLM友好格式（添加预览）
    return make_phase_space_llm_friendly(result)


def make_phase_space_llm_friendly(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将相空间数据转换为 LLM友好格式

    Args:
        data: 原始相空间数据

    Returns:
        Dict: LLM友好格式
    """
    inner_data = data.get("data", {})
    summary = data.get("summary", {})

    x_delay = np.array(inner_data.get("x_delay", []))
    x_current = np.array(inner_data.get("x_current", []))
    M = len(x_delay)

    # 数据预览（前 5000 个点，确保足够密集）
    preview_size = min(5000, M)
    data_preview = {
        "x_delay": x_delay[:preview_size].tolist(),
        "x_current": x_current[:preview_size].tolist()
    }

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