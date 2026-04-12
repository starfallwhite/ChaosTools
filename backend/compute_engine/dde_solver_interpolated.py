"""
线性插值版 DDE 求解器

根据 Prompt/1.compute_engine/prompt4.txt 实现。
支持非整数 delay 的高精度求解。

使用线性插值：
    idx = (t - T1) / h
    i = floor(idx)
    alpha = idx - i
    x_delay = (1 - alpha) * x[i] + alpha * x[i+1]
"""

from typing import Dict, Any
import numpy as np

from .base_solver import BaseSolver
from .utils import delay_linear_interpolation
from backend.core.data_protocol import create_timeseries


class DDESolverInterpolated(BaseSolver):
    """
    线性插值版 DDE 求解器

    使用线性插值处理非整数 delay，提供科研级精度。

    与基础版本的区别：
    - 基础版本：x_delay = x_array[int(T1/h)]
    - 插值版本：x_delay = interpolate(x_array, (t-T1)/h)
    """

    name: str = "dde_solver_interpolated"
    description: str = "线性插值版 DDE 求解器（科研级精度）"

    def __init__(self):
        """初始化求解器"""
        pass

    def solve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 DDE 数值求解（带插值）

        Args:
            params: 求解参数

        Returns:
            Dict: 时序数据包
        """
        # 参数提取
        xin = params.get("xin", [0.1, 0.1])
        h = params.get("h", 0.01)
        N = params.get("N", 1000)
        T1 = params.get("T1", 1.0)

        beta = params.get("beta", 2.0)
        phi = params.get("phi", 0.5)
        tou = params.get("tau", 1.0)
        xita = params.get("xita", 1.0)

        # 初始化数组
        t_array = np.zeros(N)
        x_array = np.zeros(N)
        y_array = np.zeros(N)

        # 初始状态
        x_0 = xin[0]
        y_0 = xin[1]

        # delay 步数（浮点数，用于插值）
        n_delay_float = T1 / h
        n_delay_int = int(np.floor(n_delay_float))

        # 主循环 - RK4 求解（带插值）
        for j in range(N):
            t_array[j] = (j + 1) * h
            t_current = (j + 1) * h

            # delay 处理（使用线性插值）
            if j < n_delay_int:
                # 初始化阶段：使用随机值
                x_delay = np.random.rand() - 0.5
            else:
                # 计算精确 delay 索引
                idx = (t_current - T1) / h
                # 使用线性插值
                x_delay = delay_linear_interpolation(x_array[:j], idx)

            # RK4 四个阶段
            cos_val = np.cos(x_delay - phi)
            cos_sq = cos_val * cos_val

            k11 = -(1/tou) * x_0 - (1/(xita*tou)) * y_0 + (beta/tou) * cos_sq
            k21 = x_0

            k12 = -(1/tou) * (x_0 + 0.5*h*k11) - (1/(xita*tou)) * (y_0 + 0.5*h*k21) + (beta/tou) * cos_sq
            k22 = x_0 + 0.5*h*k11

            k13 = -(1/tou) * (x_0 + 0.5*h*k12) - (1/(xita*tou)) * (y_0 + 0.5*h*k22) + (beta/tou) * cos_sq
            k23 = x_0 + 0.5*h*k12

            k14 = -(1/tou) * (x_0 + h*k13) - (1/(xita*tou)) * (y_0 + h*k23) + (beta/tou) * cos_sq
            k24 = x_0 + h*k13

            # 更新状态
            x_0 = x_0 + h * (k11 + 2*k12 + 2*k13 + k14) / 6
            y_0 = y_0 + h * (k21 + 2*k22 + 2*k23 + k24) / 6

            # 保存结果
            x_array[j] = x_0
            y_array[j] = y_0

        return create_timeseries(
            t_array.tolist(),
            x_array.tolist(),
            y_array.tolist()
        )