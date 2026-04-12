"""
lyapunov_calculate 工具实现

MCP Tool: 计算混沌系统的最大 Lyapunov 指数。

根据 Prompt/4.mcp/prompt4.txt 规范实现。
使用简单的邻近轨道发散方法（工程近似版本）。
"""

import numpy as np
from typing import Dict, Any

from backend.mcp.session import session_manager


def lyapunov_calculate(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    计算最大 Lyapunov 指数

    基于时间序列估计最大 Lyapunov 指数。
    使用简单的邻近轨道发散方法。

    Args:
        params: 工具参数（可选）
        session_id: 会话ID

    Returns:
        Dict: Lyapunov 指数结果
            {
                "type": "lyapunov",
                "data": {
                    "lambda_max": 0.xxx
                }
            }
    """
    # 从 session 获取原始时序数据
    session_data = session_manager.get(session_id)

    # 优先使用 original_timeseries（chaos_simulate 保存的原始数据）
    data = session_data.get("original_timeseries")
    if data is None:
        data = session_data.get("last_result")

    if data is None:
        return {"error": "no data found"}

    # 获取时序数据（兼容两种格式）
    raw_data = data.get("_raw_data", data.get("data", {}))
    x = np.array(raw_data.get("x", []))
    N = len(x)

    if N < 10:
        return {"error": "insufficient data"}

    # 简单 Lyapunov 估算算法
    eps = 1e-8
    max_iter = min(1000, N // 10)

    d0 = eps
    d = d0

    lyap_sum = 0.0
    count = 0

    for i in range(max_iter):
        if i + 1 >= N:
            break

        # 计算邻近轨道发散
        dx = abs(x[i + 1] - x[i]) + eps

        lyap_sum += np.log(abs(dx / d))
        d = dx
        count += 1

    if count == 0:
        return {"error": "insufficient data"}

    lambda_max = lyap_sum / count

    # 构建结果
    result = {
        "type": "lyapunov",
        "data": {
            "lambda_max": float(lambda_max)
        }
    }

    # 存回 session
    session_manager.set(session_id, "last_result", result)

    # 返回结果（添加解释）
    return {
        "type": "lyapunov",
        "data": {
            "lambda_max": float(lambda_max)
        },
        "interpretation": interpret_lyapunov(lambda_max)
    }


def interpret_lyapunov(lambda_max: float) -> str:
    """
    解释 Lyapunov 指数含义

    Args:
        lambda_max: Lyapunov 指数

    Returns:
        str: 解释文本
    """
    if lambda_max > 0.1:
        return "Strong chaotic behavior - sensitive to initial conditions"
    elif lambda_max > 0:
        return "Weak chaotic behavior"
    elif lambda_max == 0:
        return "Periodic or quasi-periodic behavior"
    else:
        return "Stable convergent system"


# 注册到 MCP registry
from backend.mcp.registry import tool_registry
tool_registry.register("lyapunov_calculate", lyapunov_calculate)