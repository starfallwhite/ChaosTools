"""
计算引擎工具函数

提供 delay 处理等辅助功能。

根据 Prompt/1.compute_engine/prompt4.txt 实现线性插值 delay。
"""

import numpy as np

try:
    from numba import njit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    def njit(*args, **kwargs):
        def decorator(func):
            return func
        if len(args) == 1 and callable(args[0]):
            return args[0]
        return decorator


def delay_lookup(buffer: np.ndarray, index: int) -> float:
    """
    获取 delay 值（基础版本）

    Args:
        buffer: 数据缓冲区
        index: 查询索引

    Returns:
        float: 延迟值
    """
    if index < 0:
        return buffer[0]
    if index >= len(buffer):
        return buffer[-1]
    return buffer[index]


def delay_linear_interpolation(x_array: np.ndarray, idx: float) -> float:
    """
    线性插值获取 delay 值（高精度版本）

    用于处理非整数 delay（科研级精度）。

    Args:
        x_array: 状态数组
        idx: 查询索引（可以是浮点数）

    Returns:
        float: 插值后的延迟值

    计算方式：
        idx = (t - T1) / h
        i = floor(idx)
        alpha = idx - i
        x_delay = (1 - alpha) * x[i] + alpha * x[i+1]
    """
    i = int(np.floor(idx))
    alpha = idx - i

    # 边界处理
    if i < 0:
        # 使用初始历史值
        return x_array[0]
    if i + 1 >= len(x_array):
        # 安全处理，返回最后一个值
        return x_array[-1]

    # 线性插值
    x_delay = (1.0 - alpha) * x_array[i] + alpha * x_array[i + 1]
    return x_delay


@njit
def delay_linear_interpolation_numba(x_array: np.ndarray, idx: float) -> float:
    """
    线性插值（numba 加速版本）

    Args:
        x_array: 状态数组
        idx: 查询索引（浮点数）

    Returns:
        float: 插值值
    """
    i = int(np.floor(idx))
    alpha = idx - i

    # 边界处理
    if i < 0:
        return x_array[0]
    if i + 1 >= len(x_array):
        return x_array[-1]

    # 线性插值
    return (1.0 - alpha) * x_array[i] + alpha * x_array[i + 1]


def initialize_history(length: int, method: str = "random") -> np.ndarray:
    """
    初始化历史缓冲区

    Args:
        length: 缓冲区长度
        method: 初始化方法 ("random" | "constant" | "zero")

    Returns:
        np.ndarray: 历史缓冲区
    """
    if method == "random":
        return np.random.randn(length)
    elif method == "constant":
        return np.ones(length)
    else:
        return np.zeros(length)