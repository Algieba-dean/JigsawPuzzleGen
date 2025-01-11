from enum import Enum


class Direction(Enum):
    """表示拼图片边的方向"""

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(self) -> "Direction":
        """获取相反的方向"""
        return Direction((self.value + 2) % 4)
