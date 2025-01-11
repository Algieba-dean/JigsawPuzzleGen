"""共享的测试fixture"""
import pytest

from src.models.direction import Direction
from src.models.piece import JigsawPiece
from src.models.puzzle import JigsawPuzzle


@pytest.fixture
def simple_2x2_puzzle():
    """创建一个简单的2x2拼图用于测试"""
    puzzle = JigsawPuzzle(2, 2)

    # 创建四个拼图片，设置它们的边值使其只有一个解
    pieces = []
    # 左上角片
    pieces.append(
        JigsawPiece(
            1,
            {Direction.UP: 0, Direction.RIGHT: 1, Direction.DOWN: 2, Direction.LEFT: 0},
            is_corner=True,
        )
    )

    # 右上角片
    pieces.append(
        JigsawPiece(
            2,
            {Direction.UP: 0, Direction.RIGHT: 0, Direction.DOWN: 3, Direction.LEFT: -1},
            is_corner=True,
        )
    )

    # 左下角片
    pieces.append(
        JigsawPiece(
            3,
            {Direction.UP: -2, Direction.RIGHT: 4, Direction.DOWN: 0, Direction.LEFT: 0},
            is_corner=True,
        )
    )

    # 右下角片
    pieces.append(
        JigsawPiece(
            4,
            {Direction.UP: -3, Direction.RIGHT: 0, Direction.DOWN: 0, Direction.LEFT: -4},
            is_corner=True,
        )
    )

    for piece in pieces:
        puzzle.add_piece(piece)

    return puzzle 