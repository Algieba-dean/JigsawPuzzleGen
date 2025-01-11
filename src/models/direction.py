from enum import Enum


class Direction(Enum):
    """表示拼图片边的方向"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    
    def opposite(self) -> 'Direction':
        """获取相反的方向"""
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        else:  # RIGHT
            return Direction.LEFT 