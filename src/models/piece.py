from typing import Dict, Optional, Tuple
from .direction import Direction


class JigsawPiece:
    """表示一个拼图片的类
    
    属性:
        id: 拼图片的唯一标识
        edges: 拼图片四个边的形状值
        position: 拼图片在拼图中的位置 (x, y)
        rotation: 拼图片的旋转角度 (0, 90, 180, 270)
        is_corner: 是否是角落拼图片
        is_edge: 是否是边缘拼图片
    """
    
    def __init__(self, piece_id: int):
        self.id = piece_id
        self.edges: Dict[Direction, int] = {
            Direction.UP: 0,
            Direction.RIGHT: 0,
            Direction.DOWN: 0,
            Direction.LEFT: 0
        }
        self.position: Tuple[Optional[int], Optional[int]] = (None, None)
        self.rotation: int = 0  # 0, 90, 180, 270
        self.is_corner: bool = False
        self.is_edge: bool = False
    
    def set_edge(self, direction: Direction, value: int) -> None:
        """设置指定方向边的形状值"""
        self.edges[direction] = value
    
    def get_edge(self, direction: Direction) -> int:
        """获取指定方向边的形状值"""
        return self.edges[direction]
    
    def set_position(self, x: int, y: int) -> None:
        """设置拼图片在拼图中的位置"""
        self.position = (x, y)
    
    def rotate(self, degrees: int) -> None:
        """旋转拼图片
        
        Args:
            degrees: 旋转的角度 (90的倍数)
        """
        if degrees % 90 != 0:
            raise ValueError("旋转角度必须是90的倍数")
            
        times = (degrees // 90) % 4
        for _ in range(times):
            # 顺时针旋转90度
            temp = self.edges[Direction.UP]
            self.edges[Direction.UP] = self.edges[Direction.LEFT]
            self.edges[Direction.LEFT] = self.edges[Direction.DOWN]
            self.edges[Direction.DOWN] = self.edges[Direction.RIGHT]
            self.edges[Direction.RIGHT] = temp
        
        self.rotation = (self.rotation + degrees) % 360
    
    def matches(self, other: 'JigsawPiece', direction: Direction) -> bool:
        """检查当前拼图片是否能与另一个拼图片在指定方向匹配"""
        return self.edges[direction] + other.edges[direction.opposite()] == 0
    
    def is_placed(self) -> bool:
        """检查拼图片是否已放置在拼图中"""
        return self.position[0] is not None and self.position[1] is not None
    
    def __str__(self) -> str:
        return f"JigsawPiece(id={self.id}, pos={self.position}, rotation={self.rotation}°)" 