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
    
    # 创建四个拼图片，设置它们的边值使其能够正确匹配
    pieces = []
    # 左上角片
    pieces.append(JigsawPiece(1, {
        Direction.UP: 0,
        Direction.RIGHT: 1,
        Direction.DOWN: 2,
        Direction.LEFT: 0
    }, is_corner=True))
    
    # 右上角片
    pieces.append(JigsawPiece(2, {
        Direction.UP: 0,
        Direction.RIGHT: 0,
        Direction.DOWN: 3,
        Direction.LEFT: -1
    }, is_corner=True))
    
    # 左下角片
    pieces.append(JigsawPiece(3, {
        Direction.UP: -2,
        Direction.RIGHT: 4,
        Direction.DOWN: 0,
        Direction.LEFT: 0
    }, is_corner=True))
    
    # 右下角片
    pieces.append(JigsawPiece(4, {
        Direction.UP: -3,
        Direction.RIGHT: 0,
        Direction.DOWN: 0,
        Direction.LEFT: -4
    }, is_corner=True))
    
    # 添加所有拼图片
    for piece in pieces:
        puzzle.add_piece(piece)
    
    return puzzle


def test_puzzle_initialization(empty_puzzle):
    """测试拼图初始化"""
    assert empty_puzzle.rows == 2
    assert empty_puzzle.cols == 2
    assert len(empty_puzzle.pieces) == 0
    assert len(empty_puzzle.board) == 2
    assert len(empty_puzzle.board[0]) == 2
    assert all(cell is None for row in empty_puzzle.board for cell in row)


def test_add_piece(empty_puzzle):
    """测试添加拼图片"""
    piece = JigsawPiece(1, {
        Direction.UP: 0,
        Direction.RIGHT: 1,
        Direction.DOWN: 2,
        Direction.LEFT: 0
    }, is_corner=True)
    
    empty_puzzle.add_piece(piece)
    assert len(empty_puzzle.pieces) == 1
    assert empty_puzzle.pieces[0] == piece


def test_place_piece(puzzle_with_pieces):
    """测试放置拼图片"""
    piece = puzzle_with_pieces.pieces[0]  # 使用左上角片
    assert puzzle_with_pieces.place_piece(piece, 0, 0)
    assert puzzle_with_pieces.board[0][0] == piece
    assert piece.position == (0, 0)


def test_place_adjacent_pieces(puzzle_with_pieces):
    """测试放置相邻的拼图片"""
    piece1 = puzzle_with_pieces.pieces[0]  # 左上角片
    piece2 = puzzle_with_pieces.pieces[1]  # 右上角片
    
    assert puzzle_with_pieces.place_piece(piece1, 0, 0)
    assert puzzle_with_pieces.place_piece(piece2, 0, 1)
    assert puzzle_with_pieces.board[0][0] == piece1
    assert puzzle_with_pieces.board[0][1] == piece2


def test_is_complete(puzzle_with_pieces):
    """测试拼图完成状态检查"""
    assert not puzzle_with_pieces.is_complete()
    
    # 放置所有拼图片
    positions = [(0,0), (0,1), (1,0), (1,1)]
    for piece, (row, col) in zip(puzzle_with_pieces.pieces, positions):
        puzzle_with_pieces.place_piece(piece, row, col)
    
    assert puzzle_with_pieces.is_complete()


def test_get_solution(puzzle_with_pieces):
    """测试获取当前解决方案"""
    # 放置所有拼图片
    positions = [(0,0), (0,1), (1,0), (1,1)]
    for piece, (row, col) in zip(puzzle_with_pieces.pieces, positions):
        puzzle_with_pieces.place_piece(piece, row, col)
    
    solution = puzzle_with_pieces.get_solution()
    assert len(solution) == 4
    for piece_id, row, col, rotation in solution:
        piece = next(p for p in puzzle_with_pieces.pieces if p.id == piece_id)
        assert piece.position == (row, col)
        assert piece.rotation == rotation 