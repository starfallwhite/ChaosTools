"""
统一数据协议模块

定义混沌系统仿真平台中所有模块间通信的标准数据格式。
"""

from typing import Dict, List, Any, TypedDict


# ==================== 数据类型定义 ====================

class TimeseriesData(TypedDict):
    """时序数据格式"""
    t: List[float]      # 时间数组
    x: List[float]      # 状态变量 x
    y: List[float]      # 状态变量 y


class SpectrumData(TypedDict):
    """频谱数据格式"""
    f: List[float]      # 频率数组
    Pxx: List[float]    # 功率谱密度


class LyapunovData(TypedDict):
    """Lyapunov指数数据格式"""
    lambda_max: float   # 最大Lyapunov指数


# ==================== 数据包格式 ====================

class TimeseriesPacket(TypedDict):
    """时序数据包"""
    type: str           # 固定为 "timeseries"
    data: TimeseriesData


class SpectrumPacket(TypedDict):
    """频谱数据包"""
    type: str           # 固定为 "spectrum"
    data: SpectrumData


class LyapunovPacket(TypedDict):
    """Lyapunov数据包"""
    type: str           # 固定为 "lyapunov"
    data: LyapunovData


# ==================== 工作流协议 ====================

class WorkflowStep(TypedDict):
    """工作流单步"""
    type: str           # "model" 或 "skill"
    name: str           # 工具名称
    params: Dict[str, Any]  # 参数（可选）


class WorkflowPacket(TypedDict):
    """工作流协议"""
    workflow: List[WorkflowStep]


# ==================== 常量定义 ====================

DATA_TYPES = {
    "timeseries": "时序数据",
    "spectrum": "频谱数据",
    "lyapunov": "Lyapunov指数"
}


# ==================== 验证函数 ====================

def validate_timeseries(data: Dict) -> bool:
    """验证时序数据格式"""
    if data.get("type") != "timeseries":
        return False
    inner = data.get("data", {})
    required_keys = ["t", "x", "y"]
    return all(key in inner for key in required_keys)


def validate_spectrum(data: Dict) -> bool:
    """验证频谱数据格式"""
    if data.get("type") != "spectrum":
        return False
    inner = data.get("data", {})
    required_keys = ["f", "Pxx"]
    return all(key in inner for key in required_keys)


def validate_lyapunov(data: Dict) -> bool:
    """验证Lyapunov数据格式"""
    if data.get("type") != "lyapunov":
        return False
    inner = data.get("data", {})
    return "lambda_max" in inner


def validate_data(data: Dict) -> bool:
    """通用数据验证"""
    data_type = data.get("type")
    validators = {
        "timeseries": validate_timeseries,
        "spectrum": validate_spectrum,
        "lyapunov": validate_lyapunov
    }
    validator = validators.get(data_type)
    if validator:
        return validator(data)
    return False


# ==================== 工厂函数 ====================

def create_timeseries(t: List[float], x: List[float], y: List[float]) -> TimeseriesPacket:
    """创建时序数据包"""
    return {
        "type": "timeseries",
        "data": {"t": t, "x": x, "y": y}
    }


def create_spectrum(f: List[float], Pxx: List[float]) -> SpectrumPacket:
    """创建频谱数据包"""
    return {
        "type": "spectrum",
        "data": {"f": f, "Pxx": Pxx}
    }


def create_lyapunov(lambda_max: float) -> LyapunovPacket:
    """创建Lyapunov数据包"""
    return {
        "type": "lyapunov",
        "data": {"lambda_max": lambda_max}
    }