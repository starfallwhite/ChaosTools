"""
Numba 加速版 DDE 求解器

根据 Prompt/1.compute_engine/prompt3.txt 规范实现。
使用 numba @njit 加速核心循环。

注意事项：
- numba 不支持 Python 对象
- 所有变量必须是 numpy array 或基本类型
- 不在 njit 中使用 dict
- 目标：支持 N > 1e6
"""

from typing import Dict, Any
import numpy as np

try:
    from numba import njit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    # 创建一个空的装饰器作为备用
    def njit(*args, **kwargs):
        def decorator(func):
            return func
        if len(args) == 1 and callable(args[0]):
            return args[0]
        return decorator

from .base_solver import BaseSolver
from backend.core.data_protocol import create_timeseries


# ==================== Numba 加速核心函数 ====================

@njit
def _rk4_core(x_0: float, y_0: float, x_delay: float,
              h: float, beta: float, phi: float,
              tou: float, xita: float) -> tuple:
    """
    RK4 单步计算（numba 加速）

    系统方程：
        dx/dt = -(1/tou)*x - (1/(xita*tou))*y + (beta/tou)*cos(x_delay - phi)^2
        dy/dt = x

    Args:
        x_0, y_0: 当前状态
        x_delay: 延迟状态
        h: 步长
        beta, phi, tou, xita: 系统参数

    Returns:
        tuple: (x_new, y_new)
    """
    # k11, k21
    cos_val = np.cos(x_delay - phi)
    k11 = -(1.0/tou) * x_0 - (1.0/(xita*tou)) * y_0 + (beta/tou) * cos_val * cos_val
    k21 = x_0

    # k12, k22
    x_temp1 = x_0 + 0.5 * h * k11
    y_temp1 = y_0 + 0.5 * h * k21
    k12 = -(1.0/tou) * x_temp1 - (1.0/(xita*tou)) * y_temp1 + (beta/tou) * cos_val * cos_val
    k22 = x_0 + 0.5 * h * k11

    # k13, k23
    x_temp2 = x_0 + 0.5 * h * k12
    y_temp2 = y_0 + 0.5 * h * k22
    k13 = -(1.0/tou) * x_temp2 - (1.0/(xita*tou)) * y_temp2 + (beta/tou) * cos_val * cos_val
    k23 = x_0 + 0.5 * h * k12

    # k14, k24
    x_temp3 = x_0 + h * k13
    y_temp3 = y_0 + h * k23
    k14 = -(1.0/tou) * x_temp3 - (1.0/(xita*tou)) * y_temp3 + (beta/tou) * cos_val * cos_val
    k24 = x_0 + h * k13

    # 更新状态
    x_new = x_0 + h * (k11 + 2.0*k12 + 2.0*k13 + k14) / 6.0
    y_new = y_0 + h * (k21 + 2.0*k22 + 2.0*k23 + k24) / 6.0

    return x_new, y_new


@njit
def _dde_solve_loop(N: int, h: float, n_delay: int,
                    x_0: float, y_0: float,
                    beta: float, phi: float, tou: float, xita: float) -> tuple:
    """
    DDE 求解主循环（numba 加速）

    Args:
        N: 仿真步数
        h: 步长
        n_delay: delay 步数
        x_0, y_0: 初始状态
        beta, phi, tou, xita: 系统参数

    Returns:
        tuple: (t_array, x_array, y_array)
    """
    # 初始化数组
    t_array = np.zeros(N)
    x_array = np.zeros(N)
    y_array = np.zeros(N)

    # 主循环
    for j in range(N):
        t_array[j] = (j + 1) * h

        # delay 处理
        if j < n_delay:
            # 初始化阶段：使用固定值（避免 numba 不支持 random）
            x_delay = 0.0
        else:
            x_delay = x_array[j - n_delay]

        # RK4 单步
        x_0, y_0 = _rk4_core(x_0, y_0, x_delay, h, beta, phi, tou, xita)

        # 保存结果
        x_array[j] = x_0
        y_array[j] = y_0

    return t_array, x_array, y_array


# ==================== Python 封装类 ====================

class DDESolverNumba(BaseSolver):
    """
    Numba 加速版 DDE 求解器

    使用 @njit 加速核心循环，支持 N > 1e6。

    注意：numba 版本不支持随机初始化 delay，
    使用固定值 0.0 初始化。
    """

    name: str = "dde_solver_numba"
    description: str = "Numba 加速版 DDE 求解器"

    def __init__(self):
        """初始化求解器"""
        pass

    def solve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 DDE 数值求解

        Args:
            params: 求解参数

        Returns:
            Dict: 时序数据包
        """
        # 参数提取（从 dict 提取为基本类型，符合 numba 要求）
        xin = params.get("xin", [0.1, 0.1])
        h = float(params.get("h", 0.01))
        N = int(params.get("N", 1000))
        T1 = float(params.get("T1", 1.0))

        beta = float(params.get("beta", 2.0))
        phi = float(params.get("phi", 0.5))
        tou = float(params.get("tau", 1.0))
        xita = float(params.get("xita", 1.0))

        # 初始状态
        x_0 = float(xin[0])
        y_0 = float(xin[1])

        # delay 步数
        n_delay = int(np.floor(T1 / h))

        # 调用 numba 加速函数
        t_array, x_array, y_array = _dde_solve_loop(
            N, h, n_delay, x_0, y_0, beta, phi, tou, xita
        )

        return create_timeseries(
            t_array.tolist(),
            x_array.tolist(),
            y_array.tolist()
        )