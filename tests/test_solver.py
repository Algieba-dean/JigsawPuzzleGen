import pytest
from src.models.direction import Direction
from src.models.piece import JigsawPiece
from src.models.puzzle import JigsawPuzzle
from src.solvers.puzzle_solver import PuzzleSolver


@pytest.fixture
def simple_puzzle():
    """创建一个简单的2x2拼图用于测试"""
    puzzle = JigsawPuzzle(2, 2)
    
    # 创建四个拼图片，设置它们的边值使其只有一个解
    pieces = [JigsawPiece(i+1) for i in range(4)]
    
    # 左上角片
    pieces[0].set_edge(Direction.RIGHT, 1)
    pieces[0].set_edge(Direction.DOWN, 2)
    pieces[0].is_corner = True
    pieces[0].is_edge = True
    
    # 右上角片
    pieces[1].set_edge(Direction.LEFT, -1)
    pieces[1].set_edge(Direction.DOWN, 3)
    pieces[1].is_corner = True
    pieces[1].is_edge = True
    
    # 左下角片
    pieces[2].set_edge(Direction.RIGHT, 4)
    pieces[2].set_edge(Direction.UP, -2)
    pieces[2].is_corner = True
    pieces[2].is_edge = True
    
    # 右下角片
    pieces[3].set_edge(Direction.LEFT, -4)
    pieces[3].set_edge(Direction.UP, -3)
    pieces[3].is_corner = True
    pieces[3].is_edge = True
    
    for piece in pieces:
        puzzle.add_piece(piece)
    
    return puzzle


def test_solver_initialization(simple_puzzle):
    """测试求解器初始化"""
    solver = PuzzleSolver(simple_puzzle)
    assert solver.puzzle == simple_puzzle
    assert len(solver._corner_pieces) == 4
    assert len(solver._edge_pieces) == 0
    assert len(solver._inner_pieces) == 0


def test_check_edge_compatibility(simple_puzzle):
    """测试边缘兼容性检查"""
    solver = PuzzleSolver(simple_puzzle)
    piece = simple_puzzle.pieces[0]  # 角落片
    
    # 测试角落位置
    assert solver._check_edge_compatibility(piece, 0, 0, [[None]*2]*2)
    assert not solver._check_edge_compatibility(piece, 0, 1, [[None]*2]*2)
    
    # 测试非角落位置
    assert not solver._check_edge_compatibility(piece, 1, 1, [[None]*2]*2)


def test_check_placement(simple_puzzle):
    """测试放置检查"""
    solver = PuzzleSolver(simple_puzzle)
    current_solution = [[None]*2 for _ in range(2)]
    
    piece1 = simple_puzzle.pieces[0]
    piece2 = simple_puzzle.pieces[1]
    
    # 测试有效放置
    assert solver._check_placement(piece1, 0, 0, current_solution)
    
    # 放置第一个片
    current_solution[0][0] = piece1
    
    # 测试匹配的相邻片
    assert solver._check_placement(piece2, 0, 1, current_solution)
    
    # 测试不匹配的放置
    piece2.rotate(90)
    assert not solver._check_placement(piece2, 0, 1, current_solution)


def test_find_all_solutions(simple_puzzle):
    """测试查找所有解决方案"""
    solver = PuzzleSolver(simple_puzzle)
    solutions = list(solver.find_all_solutions())
    
    # 验证找到的解决方案
    assert len(solutions) > 0
    
    # 验证第一个解决方案
    solution = solutions[0]
    assert len(solution) == 4
    
    # 应用解决方案并验证
    assert solver.apply_solution(solution)
    assert simple_puzzle.is_complete()
    
    # 验证所有片都在正确的位置
    for piece_id, row, col, rotation in solution:
        piece = next(p for p in simple_puzzle.pieces if p.id == piece_id)
        assert piece.position == (row, col)


def test_apply_invalid_solution(simple_puzzle):
    """测试应用无效的解决方案"""
    solver = PuzzleSolver(simple_puzzle)
    
    # 创建一个无效的解决方案
    invalid_solution = [(1, 0, 0, 0), (2, 0, 1, 90),
                       (3, 1, 0, 180), (99, 1, 1, 270)]  # 使用不存在的piece_id
    
    assert not solver.apply_solution(invalid_solution)


def test_solution_limit(simple_puzzle):
    """测试解决方案数量限制"""
    solver = PuzzleSolver(simple_puzzle)
    max_solutions = 2
    solutions = list(solver.find_all_solutions(max_solutions=max_solutions))
    assert len(solutions) <= max_solutions 