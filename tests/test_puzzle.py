import pytest
from src.models.direction import Direction
from src.models.piece import JigsawPiece
from src.models.puzzle import JigsawPuzzle


@pytest.fixture
def empty_puzzle():
    """创建一个空的2x2拼图"""
    return JigsawPuzzle(2, 2)


@pytest.fixture
def puzzle_with_pieces():
    """创建一个包含拼图片的2x2拼图"""
    puzzle = JigsawPuzzle(2, 2)
    
    # 创建四个拼图片
    pieces = [JigsawPiece(i+1) for i in range(4)]
    
    # 设置边值使它们能够匹配
    # 第一行
    pieces[0].set_edge(Direction.RIGHT, 1)
    pieces[0].set_edge(Direction.DOWN, 2)
    
    pieces[1].set_edge(Direction.LEFT, -1)
    pieces[1].set_edge(Direction.DOWN, 3)
    
    # 第二行
    pieces[2].set_edge(Direction.RIGHT, 4)
    pieces[2].set_edge(Direction.UP, -2)
    
    pieces[3].set_edge(Direction.LEFT, -4)
    pieces[3].set_edge(Direction.UP, -3)
    
    # 添加拼图片
    for piece in pieces:
        puzzle.add_piece(piece)
    
    return puzzle


def test_puzzle_initialization(empty_puzzle):
    """测试拼图初始化"""
    assert empty_puzzle.rows == 2
    assert empty_puzzle.cols == 2
    assert len(empty_puzzle.pieces) == 0
    assert all(all(piece is None for piece in row) for row in empty_puzzle.board)


def test_add_piece(empty_puzzle):
    """测试添加拼图片"""
    piece = JigsawPiece(1)
    empty_puzzle.add_piece(piece)
    assert len(empty_puzzle.pieces) == 1
    assert empty_puzzle.pieces[0] == piece


def test_place_piece(puzzle_with_pieces):
    """测试放置拼图片"""
    piece = puzzle_with_pieces.pieces[0]
    
    # 测试有效放置
    assert puzzle_with_pieces.place_piece(piece, 0, 0)
    assert puzzle_with_pieces.board[0][0] == piece
    assert piece.position == (0, 0)
    
    # 测试无效位置
    assert not puzzle_with_pieces.place_piece(piece, -1, 0)
    assert not puzzle_with_pieces.place_piece(piece, 0, puzzle_with_pieces.cols)


def test_place_adjacent_pieces(puzzle_with_pieces):
    """测试放置相邻的拼图片"""
    piece1 = puzzle_with_pieces.pieces[0]
    piece2 = puzzle_with_pieces.pieces[1]
    
    # 放置第一个拼图片
    assert puzzle_with_pieces.place_piece(piece1, 0, 0)
    
    # 放置匹配的相邻拼图片
    assert puzzle_with_pieces.place_piece(piece2, 0, 1)
    
    # 验证位置
    assert puzzle_with_pieces.board[0][0] == piece1
    assert puzzle_with_pieces.board[0][1] == piece2


def test_is_complete(puzzle_with_pieces):
    """测试拼图完成状态检查"""
    assert not puzzle_with_pieces.is_complete()
    
    # 放置所有拼图片
    for i, piece in enumerate(puzzle_with_pieces.pieces):
        row = i // 2
        col = i % 2
        puzzle_with_pieces.place_piece(piece, row, col)
    
    assert puzzle_with_pieces.is_complete()


def test_shuffle(puzzle_with_pieces):
    """测试拼图打乱"""
    # 先放置所有拼图片
    for i, piece in enumerate(puzzle_with_pieces.pieces):
        row = i // 2
        col = i % 2
        puzzle_with_pieces.place_piece(piece, row, col)
    
    # 记录原始状态
    original_positions = [(p.position, p.rotation) for p in puzzle_with_pieces.pieces]
    
    # 打乱拼图
    puzzle_with_pieces.shuffle()
    
    # 验证打乱后的状态
    shuffled_positions = [(p.position, p.rotation) for p in puzzle_with_pieces.pieces]
    assert original_positions != shuffled_positions
    assert all(p.position == (None, None) for p in puzzle_with_pieces.pieces)
    assert all(all(piece is None for piece in row) for row in puzzle_with_pieces.board)


def test_get_solution(puzzle_with_pieces):
    """测试获取解决方案"""
    # 放置所有拼图片
    for i, piece in enumerate(puzzle_with_pieces.pieces):
        row = i // 2
        col = i % 2
        puzzle_with_pieces.place_piece(piece, row, col)
    
    solution = puzzle_with_pieces.get_solution()
    assert len(solution) == 4
    for piece_id, row, col, rotation in solution:
        assert 1 <= piece_id <= 4
        assert 0 <= row < 2
        assert 0 <= col < 2
        assert rotation in [0, 90, 180, 270] 