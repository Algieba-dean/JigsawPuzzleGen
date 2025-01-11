from typing import Dict, List, Tuple

import pytest

from src.models.direction import Direction
from src.models.piece import JigsawPiece
from src.models.puzzle import JigsawPuzzle
from src.solvers.puzzle_solver import PuzzleSolver


def create_puzzle(rows: int, cols: int) -> JigsawPuzzle:
    """创建指定大小的拼图"""
    puzzle = JigsawPuzzle(rows, cols)
    piece_id = 1

    # 创建一个二维数组来存储边的值
    horizontal_edges = [
        [i + j * cols for j in range(cols - 1)] for i in range(1, rows * cols, cols)
    ]
    vertical_edges = [[i + rows * cols for i in range(cols)] for _ in range(rows - 1)]

    for row in range(rows):
        for col in range(cols):
            # 确定拼图片类型
            is_corner = row in (0, rows - 1) and col in (0, cols - 1)
            is_edge = (row in (0, rows - 1) or col in (0, cols - 1)) and not is_corner

            # 创建边缘值
            edges = {
                Direction.UP: 0 if row == 0 else -vertical_edges[row - 1][col],
                Direction.RIGHT: 0 if col == cols - 1 else horizontal_edges[row][col],
                Direction.DOWN: 0 if row == rows - 1 else vertical_edges[row][col],
                Direction.LEFT: 0 if col == 0 else -horizontal_edges[row][col - 1],
            }

            piece = JigsawPiece(piece_id, edges, is_corner=is_corner, is_edge=is_edge)
            puzzle.add_piece(piece)
            piece_id += 1

    return puzzle


@pytest.fixture(params=[(1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3), (3, 4), (4, 4)])
def puzzle_with_size(request) -> Tuple[JigsawPuzzle, int, int]:
    """创建不同大小的拼图"""
    rows, cols = request.param
    return create_puzzle(rows, cols), rows, cols


def test_different_sizes(puzzle_with_size: Tuple[JigsawPuzzle, int, int]):
    """测试不同大小拼图的解决方案查找"""
    puzzle, rows, cols = puzzle_with_size
    solver = PuzzleSolver(puzzle)

    # 获取一个解决方案
    solutions = list(solver.find_all_solutions(max_solutions=1))

    # 基本验证
    assert len(solutions) > 0, f"{rows}x{cols} 拼图无法找到解决方案"
    solution = solutions[0]

    # 验证拼图片数量
    assert len(solution) == rows * cols, f"{rows}x{cols} 拼图解决方案中拼图片数量不正确"

    # 验证位置覆盖
    positions = set((row, col) for _, row, col, _ in solution)
    expected_positions = {(r, c) for r in range(rows) for c in range(cols)}
    assert positions == expected_positions, f"{rows}x{cols} 拼图位置覆盖不完整"

    # 验证拼图片唯一性
    piece_ids = set(piece_id for piece_id, _, _, _ in solution)
    assert len(piece_ids) == rows * cols, f"{rows}x{cols} 拼图存在重复使用的拼图片"

    # 验证解决方案可应用性
    assert solver.apply_solution(solution), f"{rows}x{cols} 拼图解决方案无法应用"
    assert puzzle.is_complete(), f"{rows}x{cols} 拼图未完成"


def test_solution_count_by_size(puzzle_with_size: Tuple[JigsawPuzzle, int, int]):
    """测试不同大小拼图的解决方案数量"""
    puzzle, rows, cols = puzzle_with_size
    solver = PuzzleSolver(puzzle)

    # 根据拼图大小设置合适的最大解决方案数量
    max_solutions = min(10, 2 ** (rows * cols))  # 避免大拼图时搜索太多解决方案
    solutions = list(solver.find_all_solutions(max_solutions=max_solutions))

    # 验证找到解决方案
    assert len(solutions) > 0, f"{rows}x{cols} 拼图无法找到解决方案"

    # 验证所有解决方案都是有效的
    for solution in solutions:
        # 重置拼图
        puzzle.board = [[None for _ in range(cols)] for _ in range(rows)]
        # 应用并验证解决方案
        assert solver.apply_solution(solution), f"{rows}x{cols} 拼图解决方案无法应用"
        assert puzzle.is_complete(), f"{rows}x{cols} 拼图未完成"


def test_edge_piece_placement(puzzle_with_size: Tuple[JigsawPuzzle, int, int]):
    """测试边缘和角落拼图片的放置"""
    puzzle, rows, cols = puzzle_with_size
    solver = PuzzleSolver(puzzle)

    solutions = list(solver.find_all_solutions(max_solutions=1))
    assert len(solutions) > 0
    solution = solutions[0]

    # 验证角落片放置
    corner_positions = {(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)}
    for piece_id, row, col, _ in solution:
        piece = next(p for p in puzzle.pieces if p.id == piece_id)
        if piece.is_corner:
            assert (row, col) in corner_positions, f"{rows}x{cols} 拼图角落片放置位置错误"
        elif piece.is_edge:
            assert row in (0, rows - 1) or col in (
                0,
                cols - 1,
            ), f"{rows}x{cols} 拼图边缘片放置位置错误"
        else:
            assert row not in (0, rows - 1) and col not in (
                0,
                cols - 1,
            ), f"{rows}x{cols} 拼图普通片放置位置错误"


def test_find_solution_2x2(simple_2x2_puzzle: JigsawPuzzle):
    """测试2x2拼图的解决方案查找"""
    solver = PuzzleSolver(simple_2x2_puzzle)
    solutions = list(solver.find_all_solutions(max_solutions=1))

    # 验证找到了解决方案
    assert len(solutions) > 0

    # 验证解决方案的格式
    solution = solutions[0]
    assert len(solution) == 4  # 2x2拼图应该有4个位置

    # 验证每个位置都有一个拼图片
    positions = set((row, col) for _, row, col, _ in solution)
    assert positions == {(0, 0), (0, 1), (1, 0), (1, 1)}

    # 验证每个拼图片只使用一次
    piece_ids = set(piece_id for piece_id, _, _, _ in solution)
    assert len(piece_ids) == 4
    assert piece_ids == {1, 2, 3, 4}

    # 验证解决方案可以被应用
    assert solver.apply_solution(solution)
    assert simple_2x2_puzzle.is_complete()


def test_find_multiple_solutions(simple_2x2_puzzle: JigsawPuzzle):
    """测试查找多个解决方案"""
    solver = PuzzleSolver(simple_2x2_puzzle)
    solutions = list(solver.find_all_solutions(max_solutions=10))

    # 验证找到了多个解决方案
    assert len(solutions) > 1

    # 验证所有解决方案都是有效的
    for solution in solutions:
        # 重置拼图
        simple_2x2_puzzle.board = [[None for _ in range(2)] for _ in range(2)]
        # 应用解决方案
        assert solver.apply_solution(solution)
        # 验证拼图完整性
        assert simple_2x2_puzzle.is_complete()


def test_solution_limit(simple_2x2_puzzle: JigsawPuzzle):
    """测试解决方案数量限制"""
    solver = PuzzleSolver(simple_2x2_puzzle)
    max_solutions = 2
    solutions = list(solver.find_all_solutions(max_solutions=max_solutions))

    # 验证解决方案数量不超过限制
    assert len(solutions) <= max_solutions


@pytest.fixture
def simple_2x2_puzzle() -> JigsawPuzzle:
    """创建一个简单的2x2拼图用于测试"""
    puzzle = JigsawPuzzle(2, 2)

    # 创建四个拼图片
    pieces = [
        # 左上角片
        JigsawPiece(
            1,
            {Direction.UP: 0, Direction.RIGHT: 1, Direction.DOWN: 2, Direction.LEFT: 0},
            is_corner=True,
        ),
        # 右上角片
        JigsawPiece(
            2,
            {Direction.UP: 0, Direction.RIGHT: 0, Direction.DOWN: 3, Direction.LEFT: -1},
            is_corner=True,
        ),
        # 左下角片
        JigsawPiece(
            3,
            {Direction.UP: -2, Direction.RIGHT: 4, Direction.DOWN: 0, Direction.LEFT: 0},
            is_corner=True,
        ),
        # 右下角片
        JigsawPiece(
            4,
            {Direction.UP: -3, Direction.RIGHT: 0, Direction.DOWN: 0, Direction.LEFT: -4},
            is_corner=True,
        ),
    ]

    # 添加所有拼图片
    for piece in pieces:
        puzzle.add_piece(piece)

    return puzzle
