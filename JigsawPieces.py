from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import random
from copy import deepcopy


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class JigsawPiece:
    """表示一个拼图片的类
    
    属性:
        id: 拼图片的唯一标识
        edges: 拼图片四个边的形状值
        position: 拼图片在拼图中的位置 (x, y)
        rotation: 拼图片的旋转角度 (0, 90, 180, 270)
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
        """检查当前拼图片是否能与另一个拼图片在指定方向匹配
        
        Args:
            other: 要匹配的另一个拼图片
            direction: 匹配的方向
            
        Returns:
            bool: 是否匹配
        """
        if direction == Direction.RIGHT:
            return self.edges[Direction.RIGHT] + other.edges[Direction.LEFT] == 0
        elif direction == Direction.LEFT:
            return self.edges[Direction.LEFT] + other.edges[Direction.RIGHT] == 0
        elif direction == Direction.UP:
            return self.edges[Direction.UP] + other.edges[Direction.DOWN] == 0
        elif direction == Direction.DOWN:
            return self.edges[Direction.DOWN] + other.edges[Direction.UP] == 0
        
        return False
    
    def is_placed(self) -> bool:
        """检查拼图片是否已放置在拼图中"""
        return self.position[0] is not None and self.position[1] is not None
    
    def __str__(self) -> str:
        return f"JigsawPiece(id={self.id}, pos={self.position}, rotation={self.rotation}°)"


class JigsawPuzzle:
    """表示整个拼图的类"""
    
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board: List[List[Optional[JigsawPiece]]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]
        self.pieces: List[JigsawPiece] = []
    
    def add_piece(self, piece: JigsawPiece) -> None:
        """添加拼图片到拼图中"""
        self.pieces.append(piece)
    
    def _check_adjacent_piece(self, piece: JigsawPiece, row: int, col: int, direction: Direction) -> bool:
        """检查与指定方向相邻拼图片的匹配情况"""
        adjacent_row = row + (direction == Direction.DOWN) - (direction == Direction.UP)
        adjacent_col = col + (direction == Direction.RIGHT) - (direction == Direction.LEFT)
        
        if not (0 <= adjacent_row < self.rows and 0 <= adjacent_col < self.cols):
            return True
            
        adjacent_piece = self.board[adjacent_row][adjacent_col]
        return not adjacent_piece or piece.matches(adjacent_piece, direction)
    
    def place_piece(self, piece: JigsawPiece, row: int, col: int) -> bool:
        """在指定位置放置拼图片"""
        if not (0 <= row < self.rows and 0 <= col < self.cols) or self.board[row][col]:
            return False
            
        # 检查四个方向的匹配情况
        for direction in Direction:
            if not self._check_adjacent_piece(piece, row, col, direction):
                return False
        
        self.board[row][col] = piece
        piece.set_position(row, col)
        return True
    
    def is_complete(self) -> bool:
        """检查拼图是否完成"""
        return all(all(piece is not None for piece in row) for row in self.board)
    
    def print_board(self) -> None:
        """打印当前拼图状态"""
        for row in self.board:
            print(" ".join(str(piece.id) if piece else "X" for piece in row))
    
    @staticmethod
    def generate_solvable_puzzle(rows: int, cols: int, edge_types: int) -> 'JigsawPuzzle':
        """生成一个有解的拼图
        
        Args:
            rows: 拼图的行数
            cols: 拼图的列数
            edge_types: 边的类型数量（每种类型会有正负两个值）
            
        Returns:
            JigsawPuzzle: 生成的拼图对象
        """
        puzzle = JigsawPuzzle(rows, cols)
        # 创建一个二维数组来存储边的值
        horizontal_edges = [[random.randint(1, edge_types) for _ in range(cols-1)] for _ in range(rows)]
        vertical_edges = [[random.randint(1, edge_types) for _ in range(cols)] for _ in range(rows-1)]
        
        # 创建所有拼图片
        piece_id = 1
        for row in range(rows):
            for col in range(cols):
                piece = JigsawPiece(piece_id)
                piece_id += 1
                
                # 设置上边
                if row > 0:
                    piece.set_edge(Direction.UP, -vertical_edges[row-1][col])
                
                # 设置下边
                if row < rows-1:
                    piece.set_edge(Direction.DOWN, vertical_edges[row][col])
                
                # 设置左边
                if col > 0:
                    piece.set_edge(Direction.LEFT, -horizontal_edges[row][col-1])
                
                # 设置右边
                if col < cols-1:
                    piece.set_edge(Direction.RIGHT, horizontal_edges[row][col])
                
                # 标记边缘和角落的拼图片
                piece.is_edge = (row == 0 or row == rows-1 or col == 0 or col == cols-1)
                piece.is_corner = ((row == 0 or row == rows-1) and (col == 0 or col == cols-1))
                
                puzzle.add_piece(piece)
                puzzle.board[row][col] = piece
                piece.set_position(row, col)
        
        return puzzle
    
    def shuffle(self) -> None:
        """打乱拼图片的顺序和方向"""
        # 清空棋盘
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        # 打乱拼图片
        random.shuffle(self.pieces)
        # 随机旋转每个拼图片
        for piece in self.pieces:
            piece.rotate(random.choice([0, 90, 180, 270]))
            piece.position = (None, None)
    
    def get_solution(self) -> List[Tuple[int, int, int, int]]:
        """获取拼图的解决方案
        
        Returns:
            List[Tuple[int, int, int, int]]: 列表中每个元素为 (piece_id, row, col, rotation)
        """
        solution = []
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece:
                    solution.append((piece.id, row, col, piece.rotation))
        return solution
    
    def _try_rotations(self, piece: JigsawPiece, row: int, col: int, 
                     used_pieces: Set[int], current_solution: List[List[Optional[JigsawPiece]]], 
                     next_row: int, next_col: int, solutions: List[List[Tuple[int, int, int, int]]]) -> None:
        """尝试所有可能的旋转"""
        original_rotation = piece.rotation
        for rotation in [0, 90, 180, 270]:
            if self._try_single_rotation(piece, row, col, used_pieces, current_solution, 
                                       next_row, next_col, solutions, rotation, original_rotation):
                break
    
    def _try_single_rotation(self, piece: JigsawPiece, row: int, col: int,
                           used_pieces: Set[int], current_solution: List[List[Optional[JigsawPiece]]],
                           next_row: int, next_col: int, solutions: List[List[Tuple[int, int, int, int]]],
                           rotation: int, original_rotation: int) -> bool:
        """尝试单个旋转角度"""
        piece.rotate(rotation - original_rotation)
        if self._check_placement(piece, row, col, current_solution):
            used_pieces.add(piece.id)
            current_solution[row][col] = piece
            self._find_solutions_recursive(next_row, next_col, used_pieces, current_solution, solutions)
            current_solution[row][col] = None
            used_pieces.remove(piece.id)
        piece.rotate(original_rotation - rotation)
        return False
    
    def _check_placement(self, piece: JigsawPiece, row: int, col: int, 
                        current_solution: List[List[Optional[JigsawPiece]]]) -> bool:
        """检查放置是否有效"""
        if row > 0 and current_solution[row-1][col]:
            if not piece.matches(current_solution[row-1][col], Direction.UP):
                return False
        if col > 0 and current_solution[row][col-1]:
            if not piece.matches(current_solution[row][col-1], Direction.LEFT):
                return False
        return True
    
    def _collect_solution(self, current_solution: List[List[Optional[JigsawPiece]]]) -> List[Tuple[int, int, int, int]]:
        """收集当前解决方案"""
        return [(piece.id, r, c, piece.rotation)
                for r in range(self.rows)
                for c in range(self.cols)
                if (piece := current_solution[r][c])]
    
    def _find_solutions_recursive(self, row: int, col: int, used_pieces: Set[int],
                                current_solution: List[List[Optional[JigsawPiece]]],
                                solutions: List[List[Tuple[int, int, int, int]]]) -> None:
        """递归查找解决方案"""
        if row == self.rows:
            solutions.append(self._collect_solution(current_solution))
            return
            
        next_row = row + (col + 1) // self.cols
        next_col = (col + 1) % self.cols
        
        for piece in self.pieces:
            if piece.id not in used_pieces:
                self._try_rotations(piece, row, col, used_pieces, current_solution, 
                                  next_row, next_col, solutions)
    
    def find_all_solutions(self) -> List[List[Tuple[int, int, int, int]]]:
        """找出所有可能的拼图解决方案"""
        solutions = []
        used_pieces = set()
        current_solution = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self._find_solutions_recursive(0, 0, used_pieces, current_solution, solutions)
        return solutions
    
    @staticmethod
    def _generate_edge_combinations(edge_types: int, count: int) -> List[List[int]]:
        """生成所有可能的边值组合"""
        if count == 0:
            return [[]]
        
        result = []
        for value in range(1, edge_types + 1):
            for sub_combination in JigsawPuzzle._generate_edge_combinations(edge_types, count - 1):
                result.append([value] + sub_combination)
        return result
    
    @staticmethod
    def _create_puzzle_piece(puzzle: 'JigsawPuzzle', piece_id: int, row: int, col: int,
                           h_edges: List[int], v_edges: List[int], h_idx: int, v_idx: int,
                           rows: int, cols: int) -> Tuple[JigsawPiece, int, int]:
        """创建单个拼图片"""
        piece = JigsawPiece(piece_id)
        
        if row > 0:
            piece.set_edge(Direction.UP, -v_edges[v_idx - cols])
        if row < rows - 1:
            piece.set_edge(Direction.DOWN, v_edges[v_idx])
            v_idx += 1
        if col > 0:
            piece.set_edge(Direction.LEFT, -h_edges[h_idx - 1])
        if col < cols - 1:
            piece.set_edge(Direction.RIGHT, h_edges[h_idx])
            h_idx += 1
        
        puzzle.add_piece(piece)
        puzzle.board[row][col] = piece
        piece.set_position(row, col)
        
        return piece, h_idx, v_idx
    
    @staticmethod
    def _create_puzzle_from_edges(rows: int, cols: int, h_edges: List[int], v_edges: List[int]) -> 'JigsawPuzzle':
        """从给定的边值创建拼图"""
        puzzle = JigsawPuzzle(rows, cols)
        h_idx = v_idx = 0
        piece_id = 1
        
        for row in range(rows):
            for col in range(cols):
                _, h_idx, v_idx = JigsawPuzzle._create_puzzle_piece(
                    puzzle, piece_id, row, col, h_edges, v_edges, h_idx, v_idx, rows, cols
                )
                piece_id += 1
        
        return puzzle
    
    @staticmethod
    def generate_all_possible_puzzles(rows: int, cols: int, edge_types: int) -> List['JigsawPuzzle']:
        """生成所有可能的有效拼图配置"""
        horizontal_edges_count = (cols - 1) * rows
        vertical_edges_count = cols * (rows - 1)
        
        horizontal_combinations = JigsawPuzzle._generate_edge_combinations(edge_types, horizontal_edges_count)
        vertical_combinations = JigsawPuzzle._generate_edge_combinations(edge_types, vertical_edges_count)
        
        max_combinations = 1000
        puzzles = []
        
        for h_edges in horizontal_combinations[:max_combinations]:
            for v_edges in vertical_combinations[:max_combinations]:
                puzzle = JigsawPuzzle._create_puzzle_from_edges(rows, cols, h_edges, v_edges)
                puzzles.append(puzzle)
                
                if len(puzzles) >= max_combinations:
                    return puzzles
        
        return puzzles


if __name__ == "__main__":
    # 生成一个2x2的拼图，有2种边的类型
    puzzle = JigsawPuzzle.generate_solvable_puzzle(rows=1, cols=1, edge_types=2)
    print("初始拼图状态：")
    puzzle.print_board()
    
    print("\n查找所有可能的解决方案：")
    solutions = puzzle.find_all_solutions()
    print(f"共找到 {len(solutions)} 个解决方案")
    
    for i, solution in enumerate(solutions, 1):
        print(f"\n解决方案 {i}:")
        for piece_id, row, col, rotation in solution:
            print(f"拼图片 {piece_id} 应放在位置 ({row}, {col})，旋转 {rotation}°")
    
    print("\n生成所有可能的拼图配置：")
    all_puzzles = JigsawPuzzle.generate_all_possible_puzzles(rows=5, cols=5, edge_types=2)
    print(f"共生成 {len(all_puzzles)} 种不同的拼图配置")
