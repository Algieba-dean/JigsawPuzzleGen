import pytest
from src.models.direction import Direction


def test_direction_values():
    """测试方向枚举值"""
    assert Direction.UP.value == "up"
    assert Direction.DOWN.value == "down"
    assert Direction.LEFT.value == "left"
    assert Direction.RIGHT.value == "right"


def test_direction_opposite():
    """测试获取相反方向"""
    assert Direction.UP.opposite() == Direction.DOWN
    assert Direction.DOWN.opposite() == Direction.UP
    assert Direction.LEFT.opposite() == Direction.RIGHT
    assert Direction.RIGHT.opposite() == Direction.LEFT


def test_direction_comparison():
    """测试方向比较"""
    assert Direction.UP == Direction.UP
    assert Direction.UP != Direction.DOWN
    assert Direction.LEFT != Direction.RIGHT 