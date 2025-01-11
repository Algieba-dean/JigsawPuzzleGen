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
    
    for piece in pieces:
        puzzle.add_piece(piece)
    
    return puzzle


def test_solver_initialization(simple_puzzle):
    """测试求解器初始化"""
    solver = PuzzleSolver(simple_puzzle)
    assert len(solver._corner_pieces) == 4
    assert len(solver._edge_pieces) == 0
    assert len(solver._inner_pieces) == 0


def test_check_edge_compatibility(simple_puzzle):
    """测试边缘兼容性检查"""
    solver = PuzzleSolver(simple_puzzle)
    current_solution = [[None, None], [None, None]]
    
    # 测试角落片在角落位置
    corner_piece = next(p for p in simple_puzzle.pieces if p.is_corner)
    assert solver._check_edge_compatibility(corner_piece, 0, 0, current_solution)
    assert not solver._check_edge_compatibility(corner_piece, 0, 1, current_solution)


def test_check_placement(simple_puzzle):
    """测试放置检查"""
    solver = PuzzleSolver(simple_puzzle)
    current_solution = [[None, None], [None, None]]
    
    # 测试左上角片的放置
    piece = simple_puzzle.pieces[0]  # 左上角片
    assert solver._check_placement(piece, 0, 0, current_solution)
    
    # 放置第一个片
    current_solution[0][0] = piece
    
    # 测试右上角片的放置
    piece = simple_puzzle.pieces[1]  # 右上角片
    assert solver._check_placement(piece, 0, 1, current_solution)


def test_find_all_solutions(simple_puzzle):
    """测试查找所有解决方案"""
    # 首先验证拼图的合法性
    test_simple_puzzle_validity(simple_puzzle)
    # 然后尝试查找解决方案
    solver = PuzzleSolver(simple_puzzle)
    solutions = list(solver.find_all_solutions())
    
    assert len(solutions) > 0
    # 验证第一个解决方案
    solution = solutions[0]
    assert len(solution) == 4
    
    # 应用解决方案并验证
    assert solver.apply_solution(solution)
    assert simple_puzzle.is_complete()


def test_solution_limit(simple_puzzle):
    """测试解决方案数量限制"""
    solver = PuzzleSolver(simple_puzzle)
    max_solutions = 2
    solutions = list(solver.find_all_solutions(max_solutions=max_solutions))
    assert len(solutions) <= max_solutions 


def test_simple_puzzle_validity(simple_puzzle):
    """验证测试拼图的合法性"""
    pieces = simple_puzzle.pieces
    
    # 1. 验证拼图片数量
    assert len(pieces) == 4
    
    # 2. 验证每个拼图片的属性
    for piece in pieces:
        assert piece.is_corner  # 2x2的拼图所有片都是角落片
        
    # 3. 验证外边缘值
    # 左上角片(1)
    assert pieces[0].get_edge(Direction.UP) == 0
    assert pieces[0].get_edge(Direction.LEFT) == 0
    
    # 右上角片(2)
    assert pieces[1].get_edge(Direction.UP) == 0
    assert pieces[1].get_edge(Direction.RIGHT) == 0
    
    # 左下角片(3)
    assert pieces[2].get_edge(Direction.LEFT) == 0
    assert pieces[2].get_edge(Direction.DOWN) == 0
    
    # 右下角片(4)
    assert pieces[3].get_edge(Direction.RIGHT) == 0
    assert pieces[3].get_edge(Direction.DOWN) == 0
    
    # 4. 验证相邻边的匹配
    # 水平匹配
    assert pieces[0].get_edge(Direction.RIGHT) + pieces[1].get_edge(Direction.LEFT) == 0  # 上边两片
    assert pieces[2].get_edge(Direction.RIGHT) + pieces[3].get_edge(Direction.LEFT) == 0  # 下边两片
    
    # 垂直匹配
    assert pieces[0].get_edge(Direction.DOWN) + pieces[2].get_edge(Direction.UP) == 0  # 左边两片
    assert pieces[1].get_edge(Direction.DOWN) + pieces[3].get_edge(Direction.UP) == 0  # 右边两片
    
    # 5. 打印所有边缘值用于调试
    print("\n拼图片边缘值:")
    for i, piece in enumerate(pieces, 1):
        print(f"片{i}:")
        print(f"  上: {piece.get_edge(Direction.UP)}")
        print(f"  右: {piece.get_edge(Direction.RIGHT)}")
        print(f"  下: {piece.get_edge(Direction.DOWN)}")
        print(f"  左: {piece.get_edge(Direction.LEFT)}") 