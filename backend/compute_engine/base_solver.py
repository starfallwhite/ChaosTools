"""
抽象求解器基类

定义所有数值求解器的通用接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSolver(ABC):
    """
    数值求解器抽象基类

    所有求解器必须实现 solve 方法。
    """

    name: str = "base_solver"
    description: str = "基础求解器"

    @abstractmethod
    def solve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行数值求解

        Args:
            params: 求解参数，包含：
                - 初始值
                - 步长 h
                - 总步数 N
                - delay T1
                - 模型参数

        Returns:
            Dict: 求解结果，格式遵循 data_protocol
        """
        raise NotImplementedError("求解器必须实现 solve 方法")

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证参数有效性

        Args:
            params: 输入参数

        Returns:
            bool: 参数是否有效
        """
        required_keys = ["h", "N"]
        return all(key in params for key in required_keys)