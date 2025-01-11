from typing import List, Dict, Set, Optional, Iterator
from itertools import product
import random
from src.models.direction import Direction
from src.models.piece import JigsawPiece

class PuzzleGenerator:
    @staticmethod
    def generate_edge_values(edge_types: int = 3) -> List[int]:
        """生成有效的边缘值列表"""
        values = []
        for i in range(1, edge_types + 1):
            values.extend([i, -i])  # 添加正负值对
        return values
    
    @staticmethod
    def _create_puzzle_piece(piece_id: int, edges: Dict[Direction, int],
                           is_corner: bool = False, is_edge: bool = False) -> JigsawPiece:
        """创建一个新的拼图片"""
        return JigsawPiece(piece_id, edges, is_corner, is_edge)
    
    def generate_solvable_puzzle(self, rows: int, cols: int, edge_types: int = 3) -> List[JigsawPiece]:
        """生成一个可解的拼图"""
        if rows < 2 or cols < 2:
            raise ValueError("拼图必须至少是2x2的大小")
            
        pieces: List[JigsawPiece] = []
        piece_id = 0
        edge_values = self.generate_edge_values(edge_types)
        
        # 为每个位置创建拼图片
        for row in range(rows):
            for col in range(cols):
                edges = {}
                is_corner = (row in (0, rows-1) and col in (0, cols-1))
                is_edge = (row in (0, rows-1) or col in (0, cols-1)) and not is_corner
                
                # 上边
                if row == 0:
                    edges[Direction.UP] = 0  # 外边缘为平的
                else:
                    edges[Direction.UP] = -pieces[(row-1)*cols + col].get_edge(Direction.DOWN)
                    
                # 左边
                if col == 0:
                    edges[Direction.LEFT] = 0  # 外边缘为平的
                else:
                    edges[Direction.LEFT] = -pieces[row*cols + col-1].get_edge(Direction.RIGHT)
                    
                # 下边和右边可以随机生成
                edges[Direction.DOWN] = random.choice(edge_values) if row < rows-1 else 0
                edges[Direction.RIGHT] = random.choice(edge_values) if col < cols-1 else 0
                
                piece = self._create_puzzle_piece(piece_id, edges, is_corner, is_edge)
                pieces.append(piece)
                piece_id += 1
                
        return pieces 