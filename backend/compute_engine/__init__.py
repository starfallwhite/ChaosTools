"""
计算引擎模块

提供混沌系统数值求解功能，支持延迟微分方程（DDE）求解。

包含三个版本：
- DDESolver: 标准 Python 版本（支持随机初始化）
- DDESolverNumba: Numba 加速版本（支持 N > 1e6）
- DDESolverInterpolated: 线性插值版本（科研级精度）
"""

from .base_solver import BaseSolver
from .dde_solver import DDESolver, DDESolverWithMes
from .dde_solver_numba import DDESolverNumba
from .dde_solver_interpolated import DDESolverInterpolated
from .utils import delay_lookup, delay_linear_interpolation, delay_linear_interpolation_numba

__all__ = [
    "BaseSolver",
    "DDESolver",
    "DDESolverWithMes",
    "DDESolverNumba",
    "DDESolverInterpolated",
    "delay_lookup",
    "delay_linear_interpolation",
    "delay_linear_interpolation_numba"
]