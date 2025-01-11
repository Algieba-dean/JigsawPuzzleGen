import pytest
from src.generators.puzzle_generator import PuzzleGenerator
from src.models.direction import Direction


def test_generate_edge_values():
    """测试边值生成器"""
    edge_values = list(PuzzleGenerator._generate_edge_values(2, 3))
    assert len(edge_values) == 8  # 2^3
    assert all(len(values) == 3 for values in edge_values)
    assert all(1 <= value <= 2 for values in edge_values for value in values)


def test_create_puzzle_from_edges():
    """测试从边值创建拼图"""
    # 创建一个2x2的拼图
    h_edges = [1, 2]  # 2个水平边
    v_edges = [3, 4]  # 2个垂直边
    
    puzzle = PuzzleGenerator._create_puzzle_from_edges(2, 2, h_edges, v_edges)
    assert puzzle is not None
    assert len(puzzle.pieces) == 4
    
    # 验证边值
    # 左上角片
    assert puzzle.board[0][0].get_edge(Direction.RIGHT) == h_edges[0]
    assert puzzle.board[0][0].get_edge(Direction.DOWN) == v_edges[0]
    
    # 右上角片
    assert puzzle.board[0][1].get_edge(Direction.LEFT) == -h_edges[0]
    assert puzzle.board[0][1].get_edge(Direction.DOWN) == v_edges[1]


def test_generate_solvable_puzzle():
    """测试生成可解的拼图"""
    puzzle = PuzzleGenerator.generate_solvable_puzzle(2, 2, 2)
    assert puzzle is not None
    assert puzzle.rows == 2
    assert puzzle.cols == 2
    assert len(puzzle.pieces) == 4
    
    # 验证边缘和角落标记
    corner_count = sum(1 for p in puzzle.pieces if p.is_corner)
    edge_count = sum(1 for p in puzzle.pieces if p.is_edge and not p.is_corner)
    assert corner_count == 4
    assert edge_count == 0


def test_generate_all_possible_puzzles():
    """测试生成所有可能的拼图配置"""
    puzzles = list(PuzzleGenerator.generate_all_possible_puzzles(
        rows=2, cols=2, edge_types=1, max_combinations=10
    ))
    assert len(puzzles) > 0
    assert all(len(p.pieces) == 4 for p in puzzles)
    
    # 验证每个拼图的有效性
    for puzzle in puzzles:
        # 检查边缘和角落标记
        corner_count = sum(1 for p in puzzle.pieces if p.is_corner)
        edge_count = sum(1 for p in puzzle.pieces if p.is_edge and not p.is_corner)
        assert corner_count == 4
        assert edge_count == 0


def test_parallel_generation():
    """测试并行生成拼图"""
    puzzles_parallel = list(PuzzleGenerator.generate_all_possible_puzzles(
        rows=2, cols=2, edge_types=1, max_combinations=10, use_parallel=True
    ))
    puzzles_serial = list(PuzzleGenerator.generate_all_possible_puzzles(
        rows=2, cols=2, edge_types=1, max_combinations=10, use_parallel=False
    ))
    
    # 验证并行和串行生成的结果数量相同
    assert len(puzzles_parallel) == len(puzzles_serial) 