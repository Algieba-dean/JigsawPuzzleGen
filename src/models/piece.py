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
    
    def __init__(self, id: int, edges: Dict[Direction, int], is_corner: bool = False, is_edge: bool = False):
        self.id = id
        self._edges = edges.copy()  # 创建edges的副本
        self.position: Optional[Tuple[int, int]] = None  # (row, col)
        self._rotation = 0  # 0, 90, 180, 270
        self.is_corner = is_corner
        self.is_edge = is_edge or is_corner  # 角落片也是边缘片
        
        # 验证边缘值的有效性
        if not all(isinstance(v, int) for v in edges.values()):
            raise ValueError("所有边缘值必须是整数")
            
        # 验证方向的完整性
        if set(edges.keys()) != set(Direction):
            raise ValueError("必须为所有方向指定边缘值")
    
    @property
    def rotation(self) -> int:
        """获取当前旋转角度"""
        return self._rotation
    
    @rotation.setter
    def rotation(self, degrees: int):
        """设置旋转角度"""
        if degrees % 90 != 0:
            raise ValueError("旋转角度必须是90的倍数")
        self._rotation = degrees % 360
    
    def rotate(self, degrees: int):
        """旋转拼图片
        
        Args:
            degrees: 旋转的角度 (可以是任意整数，会自动转换为[0, 360)范围内)
        """
        if degrees % 90 != 0:
            raise ValueError("旋转角度必须是90的倍数")
        self._rotation = (self._rotation + degrees) % 360
    
    def get_edge(self, direction: Direction) -> int:
        """获取指定方向的边缘值，考虑旋转"""
        rotations = self._rotation // 90  # 将角度转换为90度的倍数
        # 根据旋转次数调整方向
        adjusted_direction = Direction((direction.value - rotations) % 4)
        return self._edges[adjusted_direction]
    
    def set_position(self, row: int, col: int):
        """设置拼图片在拼图中的位置"""
        self.position = (row, col)
    
    def matches(self, other: 'JigsawPiece', direction: Direction) -> bool:
        """检查两片是否在指定方向上匹配
        
        Args:
            other: 要检查匹配的另一片拼图片
            direction: 从当前片看向另一片的方向
            
        Returns:
            bool: 如果两片在指定方向上匹配则返回True
        """
        if not other:
            return False
            
        # 获取当前片在指定方向的边缘值
        this_edge = self.get_edge(direction)
        # 获取另一片在相反方向的边缘值
        other_edge = other.get_edge(direction.opposite())
        
        # 如果两个边缘都是0，说明都是外边缘，不应该匹配
        if this_edge == 0 and other_edge == 0:
            return False
            
        # 边缘值之和应为0表示匹配
        return this_edge + other_edge == 0
    
    def __str__(self) -> str:
        return f"JigsawPiece(id={self.id}, pos={self.position}, rotation={self._rotation}°)" 