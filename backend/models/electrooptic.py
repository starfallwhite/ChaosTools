"""
光电反馈混沌模型

模拟光电反馈系统的混沌动力学。

系统方程（与 MATLAB chaos.m 一致）：
    dx/dt = -(1/tou)*x - (1/(xita*tou))*y + (beta/tou)*cos(x_delay - phi)^2
    dy/dt = x
"""

import math
from typing import Dict, Any
import numpy as np

from .base import ChaosModel
from backend.compute_engine import DDESolver
from backend.core.data_protocol import create_timeseries


class ElectroopticFeedbackModel(ChaosModel):
    """
    光电反馈混沌模型

    模拟带延迟的光电反馈系统，产生混沌行为。

    基于 MATLAB RungeSolve_electrooptic_intensity_feedback_chaos 实现。

    Attributes:
        name: 模型标识符 "electrooptic_feedback"
        param_schema: 参数定义
    """

    name: str = "electrooptic_feedback"
    description: str = "光电反馈混沌模型（延迟微分方程）"

    # 混沌生成的推荐参数
    param_schema: Dict[str, Any] = {
        "x0": {
            "type": "float",
            "description": "初始状态 x0（y0 固定为 0）",
            "default": 1.0
        },
        "h": {
            "type": "float",
            "description": "步长（秒），推荐 10ps = 1e-11",
            "default": 1e-11  # 10 ps
        },
        "N": {
            "type": "int",
            "description": "仿真步数",
            "default": 300000  # 3e5 (避免内存溢出，实际3e6需要分批)
        },
        "T1": {
            "type": "float",
            "description": "延迟时间（秒），纳秒级别",
            "default": 15e-9  # 15 ns
        },
        "beta": {
            "type": "float",
            "description": "反馈强度",
            "default": 4.0
        },
        "phi": {
            "type": "float",
            "description": "相位偏移（rad），pi/4 ≈ 0.7854",
            "default": math.pi / 4  # pi/4
        },
        "tau": {
            "type": "float",
            "description": "时间常数 tou（秒）",
            "default": 25e-12  # 25 ps
        },
        "xita": {
            "type": "float",
            "description": "时间常数 xita（秒）",
            "default": 5e-6  # 5 us
        }
    }

    def __init__(self):
        """初始化模型"""
        self.solver = DDESolver()

    def simulate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行光电反馈混沌系统仿真

        Args:
            params: 模型参数

        Returns:
            Dict: 时序数据包
        """
        # 合并默认参数
        full_params = self._merge_default_params(params)

        # 调用求解器
        result = self.solver.solve(full_params)

        return result

    def _merge_default_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并默认参数

        Args:
            params: 用户输入参数

        Returns:
            Dict: 完整参数集
        """
        full_params = {}
        for key, schema in self.param_schema.items():
            full_params[key] = params.get(key, schema.get("default"))
        return full_params

    def get_default_params(self) -> Dict[str, Any]:
        """
        获取默认参数

        Returns:
            Dict: 默认参数值
        """
        return {
            key: schema.get("default")
            for key, schema in self.param_schema.items()
        }


class ElectroopticFeedbackWithMesModel(ChaosModel):
    """
    带信息耦合的光电反馈混沌模型

    基于 MATLAB RungeSolve_electrooptic_chaos_mes 实现。
    支持信息调制（OOK）。

    Attributes:
        name: 模型标识符 "electrooptic_feedback_mes"
    """

    name: str = "electrooptic_feedback_mes"
    description: str = "带信息耦合的光电反馈混沌模型"

    # 混沌生成的推荐参数
    param_schema: Dict[str, Any] = {
        "x0": {
            "type": "float",
            "description": "初始状态 x0（y0 固定为 0）",
            "default": 1.0
        },
        "h": {
            "type": "float",
            "description": "步长（秒），推荐 10ps = 1e-11",
            "default": 1e-11  # 10 ps
        },
        "N": {
            "type": "int",
            "description": "仿真步数",
            "default": 300000  # 3e5
        },
        "T1": {
            "type": "float",
            "description": "延迟时间（秒），纳秒级别",
            "default": 15e-9  # 15 ns
        },
        "beta": {
            "type": "float",
            "description": "反馈强度",
            "default": 4.0
        },
        "phi": {
            "type": "float",
            "description": "相位偏移（rad），pi/4 ≈ 0.7854",
            "default": math.pi / 4  # pi/4
        },
        "tau": {
            "type": "float",
            "description": "时间常数 tou（秒）",
            "default": 25e-12  # 25 ps
        },
        "xita": {
            "type": "float",
            "description": "时间常数 xita（秒）",
            "default": 5e-6  # 5 us
        },
        "mes_bits": {
            "type": "array",
            "description": "信息比特序列 [0, 1, ...]",
            "default": [1, 0, 1, 1, 0]
        },
        "mes_rate": {
            "type": "float",
            "description": "比特率 (bps)",
            "default": 1e6  # 1 Mbps
        }
    }

    def __init__(self):
        """初始化模型"""
        from backend.compute_engine import DDESolverWithMes
        self.solver = DDESolverWithMes()

    def simulate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行仿真"""
        full_params = self._merge_default_params(params)
        return self.solver.solve(full_params)

    def _merge_default_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """合并默认参数"""
        full_params = {}
        for key, schema in self.param_schema.items():
            full_params[key] = params.get(key, schema.get("default"))
        return full_params