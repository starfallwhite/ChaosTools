"""
分析技能模块

提供混沌系统的各种分析工具（FFT、Lyapunov、相空间重构等）。

包含：
- MCP 工具函数（用于 LLM 调用）
- Skill 类体系（用于内部调用）
"""

# MCP 工具函数（Prompt 规范）
from .chaos_simulate import chaos_simulate
from .fft_analysis import fft_analysis
from .lyapunov import lyapunov_calculate
from .phase_space import phase_reconstruct
from .list_models import list_models_tool, get_model_params_tool

# Skill 类体系（内部使用）
from .base import Skill
from .fft import FFTSkill
from .registry import SkillRegistry, get_skill, register_skill, list_skills

__all__ = [
    # MCP 工具（Prompt 规范）
    "chaos_simulate",
    "fft_analysis",
    "lyapunov_calculate",
    "phase_reconstruct",
    "list_models_tool",
    "get_model_params_tool",
    # Skill 类
    "Skill",
    "FFTSkill",
    "SkillRegistry",
    "get_skill",
    "register_skill",
    "list_skills"
]