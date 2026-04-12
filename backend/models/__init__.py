"""
混沌模型模块

提供各种混沌系统的模型定义和求解。

包含：
- ChaosModel 基类
- 模型注册表
- 模型实现
- API 接口
"""

from .base import ChaosModel
from .electrooptic import ElectroopticFeedbackModel, ElectroopticFeedbackWithMesModel
from .registry import ModelRegistry, get_model, register_model, list_models, MODEL_REGISTRY
from .api import get_all_model_schemas, get_model_schema, get_model_info, get_all_models_info

__all__ = [
    # 基类
    "ChaosModel",
    # 模型实现
    "ElectroopticFeedbackModel",
    "ElectroopticFeedbackWithMesModel",
    # 注册表
    "ModelRegistry",
    "get_model",
    "register_model",
    "list_models",
    "MODEL_REGISTRY",
    # API 接口
    "get_all_model_schemas",
    "get_model_schema",
    "get_model_info",
    "get_all_models_info"
]