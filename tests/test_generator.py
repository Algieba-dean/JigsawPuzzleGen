import pytest
from src.models.direction import Direction
from src.generators.puzzle_generator import PuzzleGenerator

def test_generate_edge_values():
    """测试边缘值生成"""
    generator = PuzzleGenerator()
    edge_values = generator.generate_edge_values(2)
    assert len(edge_values) == 4  # [1, -1, 2, -2]
    assert 0 not in edge_values
    assert all(isinstance(v, int) for v in edge_values)
    assert set(abs(v) for v in edge_values) == {1, 2}
    assert all(v in edge_values for v in [1, -1, 2, -2])

def test_create_puzzle_piece():
    """测试创建拼图片"""
    generator = PuzzleGenerator()
    edges = {
        Direction.UP: 1,
        Direction.RIGHT: 2,
        Direction.DOWN: -1,
        Direction.LEFT: -2
    }
    piece = generator._create_puzzle_piece(1, edges, is_corner=True)
    assert piece.id == 1
    assert piece.get_edge(Direction.UP) == 1
    assert piece.is_corner
    assert piece.is_edge

def test_generate_solvable_puzzle():
    """测试生成可解的拼图"""
    generator = PuzzleGenerator()
    pieces = generator.generate_solvable_puzzle(2, 2, 2)
    
    assert len(pieces) == 4
    # 验证角落片
    corner_pieces = [p for p in pieces if p.is_corner]
    assert len(corner_pieces) == 4
    
    # 验证边缘匹配
    for row in range(2):
        for col in range(2):
            piece = pieces[row * 2 + col]
            # 检查外边缘是否为0
            if row == 0:
                assert piece.get_edge(Direction.UP) == 0
            if col == 0:
                assert piece.get_edge(Direction.LEFT) == 0
            if row == 1:
                assert piece.get_edge(Direction.DOWN) == 0
            if col == 1:
                assert piece.get_edge(Direction.RIGHT) == 0
                
            # 检查相邻片是否匹配
            if col > 0:  # 检查左边的片
                left_piece = pieces[row * 2 + col - 1]
                assert piece.matches(left_piece, Direction.LEFT)
            if row > 0:  # 检查上边的片
                up_piece = pieces[(row - 1) * 2 + col]
                assert piece.matches(up_piece, Direction.UP) 