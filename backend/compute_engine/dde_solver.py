"""
延迟微分方程求解器

使用 RK4 方法求解 DDE 系统。

根据 MATLAB chaos.m 实现光电反馈混沌系统 RK4 求解器。

系统方程（光电反馈）：
    dx/dt = -(1/tou)*x - (1/(xita*tou))*y + (beta/tou)*cos(x_delay - phi)^2
    dy/dt = x

求解目标：
    dx/dt = f(x(t), x(t - T1), params)
"""

import math
from typing import Dict, Any
import numpy as np

from .base_solver import BaseSolver
from .utils import delay_lookup, delay_linear_interpolation
from backend.core.data_protocol import create_timeseries


class DDESolver(BaseSolver):
    """
    延迟微分方程求解器

    使用四阶 Runge-Kutta (RK4) 方法求解含延迟项的微分方程。

    基于 MATLAB RungeSolve_electrooptic_intensity_feedback_chaos 实现。
    """

    name: str = "dde_solver"
    description: str = "延迟微分方程 RK4 求解器"

    def __init__(self):
        """初始化求解器"""
        pass

    def solve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 DDE 数值求解

        Args:
            params: 求解参数，包含：
                - xin: 初始状态 [x0, y0]
                - h: 步长
                - N: 仿真步数
                - T1: delay 延迟时间
                - beta, phi, tau, xita: 系统参数

        Returns:
            Dict: 时序数据包，格式为 TimeseriesPacket
        """
        # 参数提取
        xin = params.get("xin", [0.1, 0.1])
        h = params.get("h", 0.01)
        N = params.get("N", 1000)
        T1 = params.get("T1", 1.0)

        # 系统参数（命名与 MATLAB 一致）
        beta = params.get("beta", 4.0)
        phi = params.get("phi", math.pi / 4)
        tou = params.get("tau", 25e-12)      # MATLAB: tou (25 ps)
        xita = params.get("xita", 5e-6)      # MATLAB: xita (5 us)

        # 初始化数组
        t_array = np.zeros(N)
        x_array = np.zeros(N)
        y_array = np.zeros(N)

        # 初始状态
        x_0 = xin[0]
        y_0 = xin[1]

        # delay 步数
        n_delay = int(np.floor(T1 / h))

        # 主循环 - RK4 求解
        for j in range(N):
            # 时间记录
            t_array[j] = (j + 1) * h

            # delay 处理（根据 MATLAB 逻辑）
            if j < n_delay:
                # 初始化阶段：使用随机值
                x_delay = np.random.rand() - 0.5
            else:
                # 正常阶段：使用历史值
                x_delay = x_array[j - n_delay]

            # RK4 四个阶段
            # k11, k21
            k11 = -(1/tou) * x_0 - (1/(xita*tou)) * y_0 + (beta/tou) * np.cos(x_delay - phi)**2
            k21 = x_0

            # k12, k22
            k12 = -(1/tou) * (x_0 + 0.5*h*k11) - (1/(xita*tou)) * (y_0 + 0.5*h*k21) + (beta/tou) * np.cos(x_delay - phi)**2
            k22 = x_0 + 0.5*h*k11

            # k13, k23
            k13 = -(1/tou) * (x_0 + 0.5*h*k12) - (1/(xita*tou)) * (y_0 + 0.5*h*k22) + (beta/tou) * np.cos(x_delay - phi)**2
            k23 = x_0 + 0.5*h*k12

            # k14, k24
            k14 = -(1/tou) * (x_0 + h*k13) - (1/(xita*tou)) * (y_0 + h*k23) + (beta/tou) * np.cos(x_delay - phi)**2
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


class DDESolverWithMes(BaseSolver):
    """
    带信息耦合的延迟微分方程求解器

    基于 MATLAB RungeSolve_electrooptic_chaos_mes 实现。
    支持信息调制（OOK）。
    """

    name: str = "dde_solver_mes"
    description: str = "带信息耦合的 DDE 求解器"

    def __init__(self):
        """初始化求解器"""
        pass

    def solve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行带信息耦合的 DDE 数值求解

        Args:
            params: 求解参数，包含：
                - xin: 初始状态 [x0, y0]
                - h: 步长
                - N: 仿真步数
                - T1: delay 延迟时间
                - beta, phi: 系统参数
                - mes_bits: 信息比特序列 [0, 1, ...]
                - mes_rate: 比特率 (bps)

        Returns:
            Dict: 时序数据包
        """
        # 参数提取
        xin = params.get("xin", [0.1, 0.1])
        h = params.get("h", 0.01)
        N = params.get("N", 1000)
        T1 = params.get("T1", 1.0)

        # 系统参数
        beta = params.get("beta", 4.0)
        phi = params.get("phi", math.pi / 4)
        tou = params.get("tau", 25e-12)   # 从参数获取
        xita = params.get("xita", 5e-6)   # 从参数获取

        # 信息调制参数
        mes_bits = params.get("mes_bits", [1, 0, 1, 1, 0])
        mes_rate = params.get("mes_rate", 1e6)  # 1 Mbps

        # 初始化数组
        t_array = np.zeros(N)
        x_array = np.zeros(N)

        # 初始状态
        x_0 = xin[0]
        y_0 = xin[1]

        # delay 步数
        n_delay = int(np.floor(T1 / h))

        # OOK 调制波形生成
        T_bit = 1.0 / mes_rate
        mes_waveform = np.zeros(N)
        for j in range(N):
            t = (j + 1) * h
            bit_idx = int(np.floor(t / T_bit))
            if bit_idx < len(mes_bits):
                mes_waveform[j] = mes_bits[bit_idx]

        # 主循环 - RK4 求解
        for j in range(N):
            t_array[j] = (j + 1) * h

            # delay 处理
            if j < n_delay:
                x_delay = 20 * (np.random.rand() - 0.5)
            else:
                x_delay = x_array[j - n_delay]

            # 当前信息信号
            mes_cur = mes_waveform[j]

            # RK4 四个阶段（带信息耦合）
            k11 = -(1/tou) * x_0 - (1/(xita*tou)) * y_0 + (beta/tou) * np.cos(x_delay - phi + mes_cur)**2
            k21 = x_0

            k12 = -(1/tou) * (x_0 + 0.5*h*k11) - (1/(xita*tou)) * (y_0 + 0.5*h*k21) + (beta/tou) * np.cos(x_delay - phi + mes_cur)**2
            k22 = x_0 + 0.5*h*k11

            k13 = -(1/tou) * (x_0 + 0.5*h*k12) - (1/(xita*tou)) * (y_0 + 0.5*h*k22) + (beta/tou) * np.cos(x_delay - phi + mes_cur)**2
            k23 = x_0 + 0.5*h*k12

            k14 = -(1/tou) * (x_0 + h*k13) - (1/(xita*tou)) * (y_0 + h*k23) + (beta/tou) * np.cos(x_delay - phi + mes_cur)**2
            k24 = x_0 + h*k13

            # 更新状态
            x_0 = x_0 + h * (k11 + 2*k12 + 2*k13 + k14) / 6
            y_0 = y_0 + h * (k21 + 2*k22 + 2*k23 + k24) / 6

            x_array[j] = x_0

        return create_timeseries(
            t_array.tolist(),
            x_array.tolist(),
            [0.0] * N  # y 不单独输出
        )