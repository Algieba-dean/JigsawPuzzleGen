import pytest
from src.models.direction import Direction
from src.models.piece import JigsawPiece


@pytest.fixture
def piece():
    """创建一个基本的拼图片用于测试"""
    return JigsawPiece(1)


@pytest.fixture
def piece_with_edges():
    """创建一个设置了边值的拼图片"""
    piece = JigsawPiece(2)
    piece.set_edge(Direction.UP, 1)
    piece.set_edge(Direction.RIGHT, 2)
    piece.set_edge(Direction.DOWN, 3)
    piece.set_edge(Direction.LEFT, 4)
    return piece


def test_piece_initialization(piece):
    """测试拼图片初始化"""
    assert piece.id == 1
    assert piece.position == (None, None)
    assert piece.rotation == 0
    assert not piece.is_corner
    assert not piece.is_edge
    for direction in Direction:
        assert piece.get_edge(direction) == 0


def test_piece_edge_operations(piece):
    """测试边值操作"""
    piece.set_edge(Direction.UP, 1)
    assert piece.get_edge(Direction.UP) == 1
    
    piece.set_edge(Direction.RIGHT, -2)
    assert piece.get_edge(Direction.RIGHT) == -2


def test_piece_position(piece):
    """测试位置设置"""
    piece.set_position(2, 3)
    assert piece.position == (2, 3)
    assert piece.is_placed()


def test_piece_rotation(piece_with_edges):
    """测试旋转操作"""
    original_edges = {
        Direction.UP: piece_with_edges.get_edge(Direction.UP),
        Direction.RIGHT: piece_with_edges.get_edge(Direction.RIGHT),
        Direction.DOWN: piece_with_edges.get_edge(Direction.DOWN),
        Direction.LEFT: piece_with_edges.get_edge(Direction.LEFT)
    }
    
    # 测试90度旋转
    piece_with_edges.rotate(90)
    assert piece_with_edges.rotation == 90
    assert piece_with_edges.get_edge(Direction.UP) == original_edges[Direction.LEFT]
    assert piece_with_edges.get_edge(Direction.RIGHT) == original_edges[Direction.UP]
    assert piece_with_edges.get_edge(Direction.DOWN) == original_edges[Direction.RIGHT]
    assert piece_with_edges.get_edge(Direction.LEFT) == original_edges[Direction.DOWN]
    
    # 测试180度旋转
    piece_with_edges.rotate(90)  # 再旋转90度，总共180度
    assert piece_with_edges.rotation == 180
    assert piece_with_edges.get_edge(Direction.UP) == original_edges[Direction.DOWN]
    assert piece_with_edges.get_edge(Direction.RIGHT) == original_edges[Direction.LEFT]


def test_piece_matching(piece):
    """测试拼图片匹配"""
    other_piece = JigsawPiece(2)
    
    # 设置匹配的边
    piece.set_edge(Direction.RIGHT, 1)
    other_piece.set_edge(Direction.LEFT, -1)
    assert piece.matches(other_piece, Direction.RIGHT)
    
    # 设置不匹配的边
    piece.set_edge(Direction.UP, 2)
    other_piece.set_edge(Direction.DOWN, 2)
    assert not piece.matches(other_piece, Direction.UP)


def test_invalid_rotation(piece):
    """测试无效的旋转角度"""
    with pytest.raises(ValueError):
        piece.rotate(45)


def test_piece_string_representation(piece):
    """测试字符串表示"""
    piece.set_position(1, 2)
    piece.rotate(90)
    assert str(piece) == "JigsawPiece(id=1, pos=(1, 2), rotation=90°)" 