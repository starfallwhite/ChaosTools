"""
技能注册表

管理所有可用的分析技能。
"""

from typing import Dict, List, Any, Type
from .base import Skill


class SkillRegistry:
    """
    技能注册表

    用于注册和检索分析技能。
    """

    _skills: Dict[str, Type[Skill]] = {}

    @classmethod
    def register(cls, skill_class: Type[Skill]) -> None:
        """
        注册技能

        Args:
            skill_class: 技能类（必须继承 Skill）
        """
        instance = skill_class()
        cls._skills[instance.name] = skill_class

    @classmethod
    def get(cls, name: str) -> Skill:
        """
        获取技能实例

        Args:
            name: 技能名称

        Returns:
            Skill: 技能实例

        Raises:
            KeyError: 技能不存在
        """
        if name not in cls._skills:
            raise KeyError(f"技能 '{name}' 未注册")
        return cls._skills[name]()

    @classmethod
    def list(cls) -> List[str]:
        """
        列出所有已注册技能

        Returns:
            List[str]: 技能名称列表
        """
        return list(cls._skills.keys())

    @classmethod
    def get_info(cls, name: str) -> Dict[str, Any]:
        """
        获取技能信息

        Args:
            name: 技能名称

        Returns:
            Dict: 技能信息
        """
        skill = cls.get(name)
        return skill.get_info()

    @classmethod
    def get_all_info(cls) -> List[Dict[str, Any]]:
        """
        获取所有技能信息

        Returns:
            List[Dict]: 所有技能信息列表
        """
        return [cls.get_info(name) for name in cls.list()]


# ==================== 便捷函数 ====================

def register_skill(skill_class: Type[Skill]) -> None:
    """注册技能"""
    SkillRegistry.register(skill_class)


def get_skill(name: str) -> Skill:
    """获取技能实例"""
    return SkillRegistry.get(name)


def list_skills() -> List[str]:
    """列出所有技能"""
    return SkillRegistry.list()


# ==================== 自动注册 ====================

# 导入时自动注册已定义的 Skill 类
from .fft import FFTSkill

SkillRegistry.register(FFTSkill)

# 注意：lyapunov.py 现在只包含 MCP 工具函数，不包含 Skill 类
# MCP 工具函数在各自的文件中自动注册到 tool_registry