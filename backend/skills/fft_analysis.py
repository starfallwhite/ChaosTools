"""
fft_analysis 工具实现

MCP Tool: 对时序数据进行FFT频谱分析。

根据 Prompt/4.mcp/prompt3.txt 规范实现。
"""

import numpy as np
from typing import Dict, Any

from backend.mcp.session import session_manager


def fft_analysis(params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    执行 FFT 频谱分析

    从 session 中读取原始时序数据，计算频谱。

    Args:
        params: 工具参数（可选）
        session_id: 会话ID

    Returns:
        Dict: 频谱数据
            {
                "type": "spectrum",
                "data": {
                    "f": [...],    # 频率数组
                    "Pxx": [...]   # 功率谱
                }
            }
    """
    # 从 session 获取原始时序数据（关键：使用 original_timeseries）
    session_data = session_manager.get(session_id)
    data = session_data.get("original_timeseries")

    if data is None:
        return {"error": "no timeseries data found in session. Run chaos_simulate first."}

    # 获取时序数据（兼容 LLM友好格式和原始格式）
    raw_data = data.get("_raw_data", data.get("data", {}))

    t = np.array(raw_data.get("t", []))
    x = np.array(raw_data.get("x", []))

    if len(t) < 2 or len(x) < 2:
        return {"error": "insufficient data length"}

    # 采样间隔
    dt = t[1] - t[0]

    # FFT
    X = np.fft.fft(x)
    freqs = np.fft.fftfreq(len(x), dt)

    # 只取正频率
    mask = freqs > 0
    freqs = freqs[mask]
    spectrum = np.abs(X[mask])

    # 构建结果
    result = {
        "type": "spectrum",
        "data": {
            "f": freqs.tolist(),
            "Pxx": spectrum.tolist()
        }
    }

    # 存回 session（关键）
    session_manager.set(session_id, "last_result", result)

    # 返回 LLM友好格式（添加摘要）
    return make_spectrum_llm_friendly(result)


def make_spectrum_llm_friendly(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将频谱数据转换为 LLM友好格式

    Args:
        data: 原始频谱数据

    Returns:
        Dict: LLM友好格式（含摘要和预览）
    """
    if data.get("type") != "spectrum":
        return data

    inner_data = data.get("data", {})
    f = np.array(inner_data.get("f", []))
    Pxx = np.array(inner_data.get("Pxx", []))

    length = len(f)

    # 找主要频率成分
    if length > 1:
        # 跳过 DC 分量，找最大功率频率
        max_idx = np.argmax(Pxx[1:]) + 1
        dominant_freq = float(f[max_idx])
        max_power = float(Pxx[max_idx])
    else:
        dominant_freq = 0.0
        max_power = 0.0

    summary = {
        "length": length,
        "f_range": [float(f[0]), float(f[-1])] if length > 0 else [0.0, 0.0],
        "dominant_freq": dominant_freq,
        "max_power": max_power
    }

    # 数据预览（前50个点）
    preview_size = min(50, length)
    data_preview = {
        "f": f[:preview_size].tolist(),
        "Pxx": Pxx[:preview_size].tolist()
    }

    return {
        "type": "spectrum",
        "summary": summary,
        "data_preview": data_preview,
        "full_data_ref": "session://last_result",
        "_raw_data": inner_data
    }


# 注册到 MCP registry
from backend.mcp.registry import tool_registry
tool_registry.register("fft_analysis", fft_analysis)