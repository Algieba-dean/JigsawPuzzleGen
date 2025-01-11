from typing import List, Set, Optional, Tuple, Iterator
from multiprocessing import Pool, cpu_count
from itertools import permutations
from ..models.direction import Direction
from ..models.piece import JigsawPiece
from ..models.puzzle import JigsawPuzzle


class PuzzleSolver:
    """拼图求解器类"""
    
    def __init__(self, puzzle: JigsawPuzzle):
        self.puzzle = puzzle
        self._corner_pieces = [p for p in puzzle.pieces if p.is_corner]
        self._edge_pieces = [p for p in puzzle.pieces if p.is_edge and not p.is_corner]
        self._inner_pieces = [p for p in puzzle.pieces if not p.is_edge]
    
    def _check_edge_compatibility(self, piece: JigsawPiece, row: int, col: int,
                                current_solution: List[List[Optional[JigsawPiece]]]) -> bool:
        """快速检查边缘兼容性"""
        # 检查是否是边缘位置
        is_edge_position = (row == 0 or row == self.puzzle.rows - 1 or 
                          col == 0 or col == self.puzzle.cols - 1)
        
        # 检查是否是角落位置
        is_corner_position = ((row == 0 or row == self.puzzle.rows - 1) and 
                            (col == 0 or col == self.puzzle.cols - 1))
        
        # 如果是角落位置，必须是角落片
        if is_corner_position:
            return piece.is_corner
        
        # 如果是边缘位置但不是角落位置，必须是边缘片但不是角落片
        if is_edge_position and not is_corner_position:
            return piece.is_edge and not piece.is_corner
        
        # 如果是内部位置，不能是边缘片或角落片
        return not piece.is_edge and not piece.is_corner
    
    def _check_placement(self, piece: JigsawPiece, row: int, col: int,
                        current_solution: List[List[Optional[JigsawPiece]]]) -> bool:
        """检查放置是否有效"""
        # 首先检查边缘兼容性
        if not self._check_edge_compatibility(piece, row, col, current_solution):
            return False
            
        # 检查边缘片的外边缘是否为0
        if row == 0 and piece.get_edge(Direction.UP) != 0:  # 上边缘
            return False
        if row == self.puzzle.rows - 1 and piece.get_edge(Direction.DOWN) != 0:  # 下边缘
            return False
        if col == 0 and piece.get_edge(Direction.LEFT) != 0:  # 左边缘
            return False
        if col == self.puzzle.cols - 1 and piece.get_edge(Direction.RIGHT) != 0:  # 右边缘
            return False
            
        # 检查与相邻片的匹配情况
        # 上方
        if row > 0 and current_solution[row-1][col]:
            if not piece.matches(current_solution[row-1][col], Direction.UP):
                return False
            # 双向检查
            if not current_solution[row-1][col].matches(piece, Direction.DOWN):
                return False
                
        # 左方
        if col > 0 and current_solution[row][col-1]:
            if not piece.matches(current_solution[row][col-1], Direction.LEFT):
                return False
            # 双向检查
            if not current_solution[row][col-1].matches(piece, Direction.RIGHT):
                return False
                
        # 下方
        if row < self.puzzle.rows - 1 and current_solution[row+1][col]:
            if not piece.matches(current_solution[row+1][col], Direction.DOWN):
                return False
            # 双向检查
            if not current_solution[row+1][col].matches(piece, Direction.UP):
                return False
                
        # 右方
        if col < self.puzzle.cols - 1 and current_solution[row][col+1]:
            if not piece.matches(current_solution[row][col+1], Direction.RIGHT):
                return False
            # 双向检查
            if not current_solution[row][col+1].matches(piece, Direction.LEFT):
                return False
                
        return True
    
    def _try_rotations(self, piece: JigsawPiece, row: int, col: int,
                      used_pieces: Set[int], current_solution: List[List[Optional[JigsawPiece]]],
                      next_row: int, next_col: int, solutions: List[List[Tuple[int, int, int, int]]]) -> bool:
        """尝试所有可能的旋转"""
        original_rotation = piece.rotation
        
        # 如果是边缘片，只需要尝试两个方向
        if piece.is_edge and not piece.is_corner:
            rotations = [0, 180] if row in (0, self.puzzle.rows-1) else [90, 270]
        # 如果是角片，只需要尝试一个方向
        elif piece.is_corner:
            if row == 0 and col == 0:
                rotations = [0]
            elif row == 0 and col == self.puzzle.cols-1:
                rotations = [90]
            elif row == self.puzzle.rows-1 and col == 0:
                rotations = [270]
            else:  # bottom-right corner
                rotations = [180]
        else:
            rotations = [0, 90, 180, 270]
        
        for rotation in rotations:
            piece.rotation = rotation
            if self._check_placement(piece, row, col, current_solution):
                used_pieces.add(piece.id)
                current_solution[row][col] = piece
                if self._find_solutions_recursive(next_row, next_col, used_pieces,
                                               current_solution, solutions):
                    piece.rotation = original_rotation
                    return True
                current_solution[row][col] = None
                used_pieces.remove(piece.id)
            piece.rotation = original_rotation
        return False
    
    def _find_solutions_recursive(self, row: int, col: int, used_pieces: Set[int],
                                current_solution: List[List[Optional[JigsawPiece]]],
                                solutions: List[List[Tuple[int, int, int, int]]]) -> bool:
        """递归查找解决方案"""
        if row == self.puzzle.rows:
            solutions.append(self._collect_solution(current_solution))
            return len(solutions) >= self.max_solutions if hasattr(self, 'max_solutions') else False
        
        next_row = row + (col + 1) // self.puzzle.cols
        next_col = (col + 1) % self.puzzle.cols
        
        # 根据位置选择合适的拼图片集合
        if (row == 0 and col == 0) or \
           (row == 0 and col == self.puzzle.cols-1) or \
           (row == self.puzzle.rows-1 and col == 0) or \
           (row == self.puzzle.rows-1 and col == self.puzzle.cols-1):
            pieces = self._corner_pieces
        elif row == 0 or row == self.puzzle.rows-1 or col == 0 or col == self.puzzle.cols-1:
            pieces = self._edge_pieces
        else:
            pieces = self._inner_pieces
        
        # 尝试每个可用的拼图片
        for piece in pieces:
            if piece.id not in used_pieces:
                # 保存原始旋转角度
                original_rotation = piece.rotation
                # 尝试所有可能的旋转
                rotations = self._get_valid_rotations(piece, row, col)
                for rotation in rotations:
                    piece.rotation = rotation
                    if self._check_placement(piece, row, col, current_solution):
                        used_pieces.add(piece.id)
                        current_solution[row][col] = piece
                        if self._find_solutions_recursive(next_row, next_col, used_pieces,
                                                       current_solution, solutions):
                            piece.rotation = original_rotation
                            return True
                        current_solution[row][col] = None
                        used_pieces.remove(piece.id)
                # 恢复原始旋转角度
                piece.rotation = original_rotation
        
        # 如果已经找到足够的解决方案，返回True
        if hasattr(self, 'max_solutions') and len(solutions) >= self.max_solutions:
            return True
            
        return False
    
    def _get_valid_rotations(self, piece: JigsawPiece, row: int, col: int) -> List[int]:
        """获取给定位置的有效旋转角度列表"""
        # 如果是角落片
        if piece.is_corner:
            valid_rotations = []
            original_rotation = piece.rotation
            # 尝试所有可能的旋转
            for rotation in [0, 90, 180, 270]:
                piece.rotation = rotation
                # 检查在此旋转下是否满足边缘条件
                if self._check_placement(piece, row, col, [[None] * self.puzzle.cols for _ in range(self.puzzle.rows)]):
                    valid_rotations.append(rotation)
            piece.rotation = original_rotation
            return valid_rotations if valid_rotations else [0]  # 如果没有找到有效旋转，返回默认值
            
        # 如果是边缘片（非角落）
        elif piece.is_edge:
            # 根据位置确定可能的旋转
            if row == 0:  # 上边缘
                return [0, 180]
            elif row == self.puzzle.rows - 1:  # 下边缘
                return [0, 180]
            elif col == 0:  # 左边缘
                return [90, 270]
            else:  # 右边缘
                return [90, 270]
            
        # 如果是内部片
        return [0, 90, 180, 270]
    
    def _collect_solution(self, current_solution: List[List[Optional[JigsawPiece]]]) -> List[Tuple[int, int, int, int]]:
        """收集当前解决方案"""
        return [(piece.id, r, c, piece.rotation)
                for r in range(self.puzzle.rows)
                for c in range(self.puzzle.cols)
                if (piece := current_solution[r][c])]
    
    def find_all_solutions(self, max_solutions: int = 1000) -> Iterator[List[Tuple[int, int, int, int]]]:
        """找出所有可能的拼图解决方案
        
        Args:
            max_solutions: 最大解决方案数量
            
        Returns:
            Iterator[List[Tuple[int, int, int, int]]]: 解决方案生成器
        """
        solutions = []
        used_pieces = set()
        current_solution = [[None for _ in range(self.puzzle.cols)]
                          for _ in range(self.puzzle.rows)]
        
        # 设置最大解决方案数量
        self.max_solutions = max_solutions
        
        # 从左上角开始尝试放置
        self._find_solutions_recursive(0, 0, used_pieces, current_solution, solutions)
        
        # 删除最大解决方案数量属性
        delattr(self, 'max_solutions')
        
        # 返回找到的解决方案
        yield from solutions
    
    def apply_solution(self, solution: List[Tuple[int, int, int, int]]) -> bool:
        """应用解决方案到拼图"""
        self.puzzle.board = [[None for _ in range(self.puzzle.cols)]
                           for _ in range(self.puzzle.rows)]
        
        for piece_id, row, col, rotation in solution:
            piece = next((p for p in self.puzzle.pieces if p.id == piece_id), None)
            if not piece:
                return False
            
            piece.rotation = rotation
            if not self.puzzle.place_piece(piece, row, col):
                return False
        
        return True 