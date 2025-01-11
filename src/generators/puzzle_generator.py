from typing import List, Tuple, Iterator, Optional
import random
from multiprocessing import Pool, cpu_count
from itertools import product, islice
from ..models.direction import Direction
from ..models.piece import JigsawPiece
from ..models.puzzle import JigsawPuzzle


class PuzzleGenerator:
    """拼图生成器类"""
    
    @staticmethod
    def _generate_edge_values(edge_types: int, count: int) -> Iterator[List[int]]:
        """使用生成器生成边值组合"""
        for values in product(range(1, edge_types + 1), repeat=count):
            yield list(values)
    
    @staticmethod
    def _create_puzzle_from_edges(rows: int, cols: int, h_edges: List[int],
                                v_edges: List[int]) -> Optional[JigsawPuzzle]:
        """从给定的边值创建拼图，如果无效则返回 None"""
        puzzle = JigsawPuzzle(rows, cols)
        h_idx = v_idx = 0
        piece_id = 1
        
        # 预先检查边值的有效性
        if not all(-edge_types <= x <= edge_types for x in h_edges + v_edges):
            return None
            
        try:
            for row in range(rows):
                for col in range(cols):
                    piece = JigsawPiece(piece_id)
                    piece_id += 1
                    
                    # 设置边的值
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
                    
                    piece.is_edge = (row == 0 or row == rows-1 or col == 0 or col == cols-1)
                    piece.is_corner = ((row == 0 or row == rows-1) and (col == 0 or col == cols-1))
                    
                    puzzle.add_piece(piece)
                    puzzle.board[row][col] = piece
                    piece.set_position(row, col)
            
            return puzzle
        except Exception:
            return None
    
    @staticmethod
    def _process_edge_combination(args: Tuple[int, int, List[int], List[int]]) -> Optional[JigsawPuzzle]:
        """处理单个边值组合"""
        rows, cols, h_edges, v_edges = args
        return PuzzleGenerator._create_puzzle_from_edges(rows, cols, h_edges, v_edges)
    
    @staticmethod
    def generate_all_possible_puzzles(rows: int, cols: int, edge_types: int,
                                    max_combinations: int = 1000,
                                    use_parallel: bool = True) -> Iterator[JigsawPuzzle]:
        """生成所有可能的有效拼图配置
        
        Args:
            rows: 拼图的行数
            cols: 拼图的列数
            edge_types: 边的类型数量
            max_combinations: 最大生成数量
            use_parallel: 是否使用并行处理
            
        Returns:
            Iterator[JigsawPuzzle]: 拼图生成器
        """
        horizontal_edges_count = (cols - 1) * rows
        vertical_edges_count = cols * (rows - 1)
        
        # 生成边值组合
        h_combinations = PuzzleGenerator._generate_edge_values(edge_types, horizontal_edges_count)
        v_combinations = list(PuzzleGenerator._generate_edge_values(edge_types, vertical_edges_count))
        
        if use_parallel and max_combinations > 100:
            # 并行处理
            with Pool(cpu_count()) as pool:
                args = ((rows, cols, list(h), list(v))
                       for h, v in product(h_combinations, v_combinations))
                
                for puzzle in pool.imap_unordered(
                    PuzzleGenerator._process_edge_combination,
                    islice(args, max_combinations)
                ):
                    if puzzle is not None:
                        yield puzzle
        else:
            # 串行处理
            count = 0
            for h_edges in h_combinations:
                if count >= max_combinations:
                    break
                    
                for v_edges in v_combinations:
                    if count >= max_combinations:
                        break
                        
                    puzzle = PuzzleGenerator._create_puzzle_from_edges(
                        rows, cols, h_edges, v_edges
                    )
                    if puzzle is not None:
                        yield puzzle
                        count += 1 