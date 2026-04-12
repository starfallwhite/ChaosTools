"""
混沌模型抽象基类

定义所有混沌模型的统一接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class ChaosModel(ABC):
    """
    混沌模型抽象基类

    所有混沌系统模型必须实现此接口。

    Attributes:
        name: 模型名称（唯一标识）
        param_schema: 参数定义规范
    """

    name: str = "base_model"
    description: str = "基础混沌模型"
    param_schema: Dict[str, Any] = {}

    @abstractmethod
    def simulate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行混沌系统仿真

        Args:
            params: 模型参数，包含：
                - 模型特定参数（如 beta, phi, tau）
                - 求解参数（如 h, N, T1）

        Returns:
            Dict: 时序数据包，格式遵循 data_protocol
        """
        raise NotImplementedError("模型必须实现 simulate 方法")

    def get_param_info(self) -> Dict[str, Any]:
        """
        获取参数信息

        Returns:
            Dict: 参数定义规范
        """
        return {
            "name": self.name,
            "description": self.description,
            "param_schema": self.param_schema
        }

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证参数有效性

        Args:
            params: 输入参数

        Returns:
            bool: 参数是否有效
        """
        required_keys = list(self.param_schema.keys())
        return all(key in params for key in required_keys)