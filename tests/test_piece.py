import pytest
from src.models.direction import Direction
from src.models.piece import JigsawPiece


@pytest.fixture
def piece():
    """创建一个基本的拼图片用于测试"""
    edges = {
        Direction.UP: 1,
        Direction.RIGHT: 2,
        Direction.DOWN: -1,
        Direction.LEFT: -2
    }
    return JigsawPiece(1, edges)


@pytest.fixture
def piece_with_edges():
    """创建一个设置了边值的拼图片"""
    edges = {
        Direction.UP: 3,
        Direction.RIGHT: 4,
        Direction.DOWN: -3,
        Direction.LEFT: -4
    }
    return JigsawPiece(2, edges)


def test_piece_initialization(piece):
    """测试拼图片初始化"""
    assert piece.id == 1
    assert piece.get_edge(Direction.UP) == 1
    assert piece.get_edge(Direction.RIGHT) == 2
    assert piece.get_edge(Direction.DOWN) == -1
    assert piece.get_edge(Direction.LEFT) == -2
    assert piece.position is None
    assert piece.rotation == 0


def test_piece_edge_operations(piece):
    """测试边缘值操作"""
    assert piece.get_edge(Direction.UP) == 1
    assert piece.get_edge(Direction.RIGHT) == 2
    assert piece.get_edge(Direction.DOWN) == -1
    assert piece.get_edge(Direction.LEFT) == -2


def test_piece_rotation(piece_with_edges):
    """测试拼图片旋转"""
    original_up = piece_with_edges.get_edge(Direction.UP)
    original_right = piece_with_edges.get_edge(Direction.RIGHT)
    
    # 旋转90度
    piece_with_edges.rotation = 90
    assert piece_with_edges.get_edge(Direction.UP) == piece_with_edges._edges[Direction.LEFT]
    assert piece_with_edges.get_edge(Direction.RIGHT) == piece_with_edges._edges[Direction.UP]
    
    # 旋转180度
    piece_with_edges.rotation = 180
    assert piece_with_edges.get_edge(Direction.UP) == piece_with_edges._edges[Direction.DOWN]
    assert piece_with_edges.get_edge(Direction.RIGHT) == piece_with_edges._edges[Direction.LEFT]
    
    # 旋转270度
    piece_with_edges.rotation = 270
    assert piece_with_edges.get_edge(Direction.UP) == piece_with_edges._edges[Direction.RIGHT]
    assert piece_with_edges.get_edge(Direction.RIGHT) == piece_with_edges._edges[Direction.DOWN]
    
    # 恢复原位
    piece_with_edges.rotation = 0
    assert piece_with_edges.get_edge(Direction.UP) == original_up
    assert piece_with_edges.get_edge(Direction.RIGHT) == original_right


def test_piece_matching(piece, piece_with_edges):
    """测试拼图片匹配"""
    # 创建一个匹配的拼图片
    matching_edges = {
        Direction.UP: -1,  # 匹配piece的DOWN
        Direction.RIGHT: -2,  # 匹配piece的LEFT
        Direction.DOWN: 1,  # 匹配piece的UP
        Direction.LEFT: 2  # 匹配piece的RIGHT
    }
    matching_piece = JigsawPiece(3, matching_edges)
    
    assert piece.matches(matching_piece, Direction.UP)
    assert piece.matches(matching_piece, Direction.RIGHT)
    assert matching_piece.matches(piece, Direction.DOWN)
    assert matching_piece.matches(piece, Direction.LEFT)
    
    # 测试不匹配的情况
    assert not piece.matches(piece_with_edges, Direction.UP)


def test_piece_string_representation(piece):
    """测试拼图片的字符串表示"""
    expected = "JigsawPiece(id=1, pos=None, rotation=0°)"
    assert str(piece) == expected 