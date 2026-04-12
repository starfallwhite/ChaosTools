"""
分析技能抽象基类

定义所有分析工具的统一接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Skill(ABC):
    """
    分析技能抽象基类

    所有分析工具必须实现此接口。

    Attributes:
        name: 技能名称（唯一标识）
        input_type: 输入数据类型
        output_type: 输出数据类型
    """

    name: str = "base_skill"
    description: str = "基础分析技能"
    input_type: str = "timeseries"
    output_type: str = "unknown"

    @abstractmethod
    def run(self, data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行分析

        Args:
            data: 输入数据（格式由 input_type 指定）
            params: 分析参数（可选）

        Returns:
            Dict: 分析结果（格式由 output_type 指定）
        """
        raise NotImplementedError("技能必须实现 run 方法")

    def validate_input(self, data: Dict[str, Any]) -> bool:
        """
        验证输入数据

        Args:
            data: 输入数据

        Returns:
            bool: 数据格式是否正确
        """
        return data.get("type") == self.input_type

    def get_info(self) -> Dict[str, Any]:
        """
        获取技能信息

        Returns:
            Dict: 技能描述信息
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_type": self.input_type,
            "output_type": self.output_type
        }