"""
FFT 频谱分析技能

对时序数据进行快速傅里叶变换，提取频谱特征。
"""

from typing import Dict, Any, List
import numpy as np

from .base import Skill
from backend.core.data_protocol import create_spectrum, validate_timeseries


class FFTSkill(Skill):
    """
    FFT 频谱分析技能

    将时序数据转换为频谱数据，揭示信号的频率成分。

    Attributes:
        name: "fft"
        input_type: "timeseries"
        output_type: "spectrum"
    """

    name: str = "fft"
    description: str = "FFT频谱分析"
    input_type: str = "timeseries"
    output_type: str = "spectrum"

    def run(self, data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行 FFT 分析

        Args:
            data: 时序数据包
            params: 分析参数（可选）
                - fs: 采样频率（默认从数据推断）

        Returns:
            Dict: 频谱数据包
        """
        if not validate_timeseries(data):
            raise ValueError("输入数据格式错误，期望 timeseries 类型")

        # 提取数据
        inner_data = data.get("data", {})
        t = np.array(inner_data.get("t", []))
        x = np.array(inner_data.get("x", []))

        if len(t) < 2 or len(x) < 2:
            raise ValueError("数据长度不足")

        # 推断采样频率
        params = params or {}
        fs = params.get("fs", 1.0 / (t[1] - t[0]) if len(t) > 1 else 1.0)

        # 执行 FFT（框架，待实现完整算法）
        n = len(x)

        # 基础 FFT 实现
        fft_result = np.fft.fft(x)
        f = np.fft.fftfreq(n, d=1.0/fs)

        # 只取正频率部分
        positive_mask = f >= 0
        f_positive = f[positive_mask]
        Pxx = np.abs(fft_result[positive_mask]) ** 2 / n

        return create_spectrum(
            f_positive.tolist(),
            Pxx.tolist()
        )