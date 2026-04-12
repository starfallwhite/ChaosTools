"""
模型注册表

管理所有可用的混沌模型。
"""

from typing import Dict, List, Any, Type
from .base import ChaosModel


class ModelRegistry:
    """
    模型注册表

    用于注册和检索混沌模型。
    """

    _models: Dict[str, Type[ChaosModel]] = {}

    @classmethod
    def register(cls, model_class: Type[ChaosModel]) -> None:
        """
        注册模型

        Args:
            model_class: 模型类（必须继承 ChaosModel）
        """
        instance = model_class()
        cls._models[instance.name] = model_class

    @classmethod
    def get(cls, name: str) -> ChaosModel:
        """
        获取模型实例

        Args:
            name: 模型名称

        Returns:
            ChaosModel: 模型实例

        Raises:
            KeyError: 模型不存在
        """
        if name not in cls._models:
            raise KeyError(f"模型 '{name}' 未注册")
        return cls._models[name]()

    @classmethod
    def list(cls) -> List[str]:
        """
        列出所有已注册模型

        Returns:
            List[str]: 模型名称列表
        """
        return list(cls._models.keys())

    @classmethod
    def get_info(cls, name: str) -> Dict[str, Any]:
        """
        获取模型信息

        Args:
            name: 模型名称

        Returns:
            Dict: 模型信息（名称、描述、参数规范）
        """
        model = cls.get(name)
        return model.get_param_info()

    @classmethod
    def get_all_info(cls) -> List[Dict[str, Any]]:
        """
        获取所有模型信息

        Returns:
            List[Dict]: 所有模型信息列表
        """
        return [cls.get_info(name) for name in cls.list()]


# ==================== 便捷函数 ====================

def register_model(model_class: Type[ChaosModel]) -> None:
    """注册模型"""
    ModelRegistry.register(model_class)


def get_model(name: str) -> ChaosModel:
    """获取模型实例"""
    return ModelRegistry.get(name)


def list_models() -> List[str]:
    """列出所有模型"""
    return ModelRegistry.list()


# ==================== 自动注册 ====================

# 导入时自动注册已定义的模型
from .electrooptic import ElectroopticFeedbackModel, ElectroopticFeedbackWithMesModel

ModelRegistry.register(ElectroopticFeedbackModel)
ModelRegistry.register(ElectroopticFeedbackWithMesModel)


# ==================== 全局别名（符合 prompt 规范）====================

# Prompt 要求使用 MODEL_REGISTRY.get(model_name)
# 由于 ModelRegistry 使用 classmethod，这里创建类别名
MODEL_REGISTRY = ModelRegistry