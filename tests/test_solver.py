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


@pytest.fixture
def edge_test_puzzle():
    """创建一个3x3拼图用于测试边缘兼容性"""
    puzzle = JigsawPuzzle(3, 3)
    
    # 创建一个角落片
    corner_piece = JigsawPiece(1, {
        Direction.UP: 0,
        Direction.RIGHT: 1,
        Direction.DOWN: 2,
        Direction.LEFT: 0
    }, is_corner=True)
    
    # 创建一个边缘片（非角落）
    edge_piece = JigsawPiece(2, {
        Direction.UP: 0,
        Direction.RIGHT: 3,
        Direction.DOWN: 4,
        Direction.LEFT: -1
    }, is_edge=True)
    
    puzzle.add_piece(corner_piece)
    puzzle.add_piece(edge_piece)
    
    return puzzle


@pytest.fixture
def complex_puzzle():
    """创建一个3x3的拼图用于测试更复杂的情况"""
    puzzle = JigsawPuzzle(3, 3)
    
    pieces = []
    # 左上角片
    pieces.append(JigsawPiece(1, {
        Direction.UP: 0,
        Direction.RIGHT: 1,
        Direction.DOWN: 2,
        Direction.LEFT: 0
    }, is_corner=True))
    
    # 上边缘片
    pieces.append(JigsawPiece(2, {
        Direction.UP: 0,
        Direction.RIGHT: 3,
        Direction.DOWN: 4,
        Direction.LEFT: -1
    }, is_edge=True))
    
    # 右上角片
    pieces.append(JigsawPiece(3, {
        Direction.UP: 0,
        Direction.RIGHT: 0,
        Direction.DOWN: 5,
        Direction.LEFT: -3
    }, is_corner=True))
    
    # 左边缘片
    pieces.append(JigsawPiece(4, {
        Direction.UP: -2,
        Direction.RIGHT: 6,
        Direction.DOWN: 7,
        Direction.LEFT: 0
    }, is_edge=True))
    
    # 中心片
    pieces.append(JigsawPiece(5, {
        Direction.UP: -4,
        Direction.RIGHT: 8,
        Direction.DOWN: 9,
        Direction.LEFT: -6
    }))
    
    # 右边缘片
    pieces.append(JigsawPiece(6, {
        Direction.UP: -5,
        Direction.RIGHT: 0,
        Direction.DOWN: 10,
        Direction.LEFT: -8
    }, is_edge=True))
    
    # 左下角片
    pieces.append(JigsawPiece(7, {
        Direction.UP: -7,
        Direction.RIGHT: 11,
        Direction.DOWN: 0,
        Direction.LEFT: 0
    }, is_corner=True))
    
    # 下边缘片
    pieces.append(JigsawPiece(8, {
        Direction.UP: -9,
        Direction.RIGHT: 12,
        Direction.DOWN: 0,
        Direction.LEFT: -11
    }, is_edge=True))
    
    # 右下角片
    pieces.append(JigsawPiece(9, {
        Direction.UP: -10,
        Direction.RIGHT: 0,
        Direction.DOWN: 0,
        Direction.LEFT: -12
    }, is_corner=True))
    
    for piece in pieces:
        puzzle.add_piece(piece)
    
    return puzzle


@pytest.fixture
def multi_solution_puzzle():
    """创建一个2x2的拼图，该拼图有多个有效解"""
    puzzle = JigsawPuzzle(2, 2)
    
    pieces = []
    # 左上角片 - 可以和右上角片互换位置
    pieces.append(JigsawPiece(1, {
        Direction.UP: 0,
        Direction.RIGHT: 1,
        Direction.DOWN: 1,
        Direction.LEFT: 0
    }, is_corner=True))
    
    # 右上角片 - 可以和左上角片互换位置
    pieces.append(JigsawPiece(2, {
        Direction.UP: 0,
        Direction.RIGHT: 0,
        Direction.DOWN: 1,
        Direction.LEFT: -1
    }, is_corner=True))
    
    # 左下角片
    pieces.append(JigsawPiece(3, {
        Direction.UP: -1,
        Direction.RIGHT: 2,
        Direction.DOWN: 0,
        Direction.LEFT: 0
    }, is_corner=True))
    
    # 右下角片
    pieces.append(JigsawPiece(4, {
        Direction.UP: -1,
        Direction.RIGHT: 0,
        Direction.DOWN: 0,
        Direction.LEFT: -2
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


def test_check_edge_compatibility(edge_test_puzzle):
    """测试边缘兼容性检查"""
    solver = PuzzleSolver(edge_test_puzzle)
    current_solution = [[None, None, None], [None, None, None], [None, None, None]]
    
    # 获取角落片和边缘片
    corner_piece = next(p for p in edge_test_puzzle.pieces if p.is_corner)
    edge_piece = next(p for p in edge_test_puzzle.pieces if p.is_edge and not p.is_corner)
    
    # 测试角落片
    assert solver._check_edge_compatibility(corner_piece, 0, 0, current_solution)  # 角落位置
    assert not solver._check_edge_compatibility(corner_piece, 0, 1, current_solution)  # 边缘位置
    
    # 测试边缘片
    assert solver._check_edge_compatibility(edge_piece, 0, 1, current_solution)  # 边缘位置
    assert not solver._check_edge_compatibility(edge_piece, 0, 0, current_solution)  # 角落位置


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


def test_solver_piece_classification(complex_puzzle):
    """测试求解器对拼图片的分类"""
    solver = PuzzleSolver(complex_puzzle)
    assert len(solver._corner_pieces) == 4
    assert len(solver._edge_pieces) == 4
    assert len(solver._inner_pieces) == 1



def test_partial_solution(complex_puzzle):
    """测试部分解决方案的情况"""
    solver = PuzzleSolver(complex_puzzle)
    current_solution = [[None] * 3 for _ in range(3)]
    
    # 放置第一个角落片（左上角片）
    corner_piece = next(p for p in complex_puzzle.pieces if p.is_corner)
    assert solver._check_placement(corner_piece, 0, 0, current_solution)
    current_solution[0][0] = corner_piece
    
    # 尝试放置不匹配的片（选择右下角片，它不应该能放在上边缘位置）
    non_matching_piece = next(p for p in complex_puzzle.pieces 
                            if p.is_corner and p.get_edge(Direction.UP) != -1)  # 确保上边缘不匹配
    non_matching_piece.rotation = 0  # 设置为默认旋转
    assert not solver._check_placement(non_matching_piece, 0, 1, current_solution)


def test_invalid_solutions(complex_puzzle):
    """测试无效解的处理"""
    solver = PuzzleSolver(complex_puzzle)
    
    # 创建一个无效的解决方案
    invalid_solution = [(1, 0, 0, 0), (2, 0, 1, 90), (3, 0, 2, 180)]  # 不完整的解决方案
    assert not solver.apply_solution(invalid_solution)
    
    # 测试使用不存在的拼图片ID
    invalid_solution = [(999, 0, 0, 0)]  # 使用不存在的ID
    assert not solver.apply_solution(invalid_solution)


def test_complex_puzzle_validity(complex_puzzle):
    """验证复杂测试拼图的合法性"""
    pieces = complex_puzzle.pieces
    
    # 1. 验证拼图片数量和类型
    assert len(pieces) == 9  # 3x3拼图
    corner_pieces = [p for p in pieces if p.is_corner]
    edge_pieces = [p for p in pieces if p.is_edge and not p.is_corner]
    inner_pieces = [p for p in pieces if not p.is_edge]
    assert len(corner_pieces) == 4
    assert len(edge_pieces) == 4
    assert len(inner_pieces) == 1
    
    # 2. 验证外边缘值
    for piece in pieces:
        if piece.is_corner:
            # 每个角落片应该有两个0值的边
            zero_edges = sum(1 for d in Direction if piece.get_edge(d) == 0)
            assert zero_edges == 2, f"角落片 {piece.id} 应该有两个0值的边，但有 {zero_edges} 个"
        elif piece.is_edge:
            # 每个边缘片应该有一个0值的边
            zero_edges = sum(1 for d in Direction if piece.get_edge(d) == 0)
            assert zero_edges == 1, f"边缘片 {piece.id} 应该有一个0值的边，但有 {zero_edges} 个"
    
    # 3. 打印所有边缘值用于调试
    print("\n复杂拼图片边缘值:")
    for piece in pieces:
        print(f"片{piece.id} ({'角落片' if piece.is_corner else '边缘片' if piece.is_edge else '内部片'}):")
        print(f"  上: {piece.get_edge(Direction.UP)}")
        print(f"  右: {piece.get_edge(Direction.RIGHT)}")
        print(f"  下: {piece.get_edge(Direction.DOWN)}")
        print(f"  左: {piece.get_edge(Direction.LEFT)}")
    
    # 4. 验证边缘值的匹配关系
    # 检查每个非零边缘值是否有对应的匹配值
    all_edges = {}  # {value: [(piece_id, direction)]}
    for piece in pieces:
        for direction in Direction:
            value = piece.get_edge(direction)
            if value != 0:
                if value not in all_edges:
                    all_edges[value] = []
                all_edges[value].append((piece.id, direction))
                
    # 检查每个边缘值是否有且仅有一个匹配的相反值
    for value, occurrences in all_edges.items():
        matching_value = -value
        if matching_value in all_edges:
            assert len(all_edges[matching_value]) == 1, \
                f"边缘值 {value} 应该只有一个匹配值 {matching_value}"
            assert len(occurrences) == 1, \
                f"边缘值 {value} 在拼图中出现了多次"
        else:
            assert False, f"边缘值 {value} 没有找到匹配的值 {matching_value}"


def test_solution_validation(complex_puzzle):
    """测试解决方案的验证"""
    # 首先验证拼图的合法性
    test_complex_puzzle_validity(complex_puzzle)
    
    solver = PuzzleSolver(complex_puzzle)
    solutions = list(solver.find_all_solutions(max_solutions=1))
    
    assert len(solutions) > 0
    solution = solutions[0]
    
    # 验证解决方案的完整性
    assert len(solution) == 9  # 3x3拼图应该有9个片
    
    # 验证每个位置都被使用了一次
    positions = set((row, col) for _, row, col, _ in solution)
    assert len(positions) == 9
    
    # 验证每个拼图片都被使用了一次
    piece_ids = set(piece_id for piece_id, _, _, _ in solution)
    assert len(piece_ids) == 9


def test_multiple_solutions_limit(complex_puzzle):
    """测试多个解决方案的限制"""
    solver = PuzzleSolver(complex_puzzle)
    
    # 测试不同的解决方案数量限制
    limits = [1, 2, 5]
    for limit in limits:
        solutions = list(solver.find_all_solutions(max_solutions=limit))
        assert len(solutions) <= limit
        
        # 验证每个解决方案都是有效的
        for solution in solutions:
            assert solver.apply_solution(solution)
            assert complex_puzzle.is_complete()
            
            # 重置拼图状态
            complex_puzzle.board = [[None] * 3 for _ in range(3)] 


def test_multiple_valid_solutions(multi_solution_puzzle):
    """测试具有多个有效解的情况"""
    solver = PuzzleSolver(multi_solution_puzzle)
    solutions = list(solver.find_all_solutions())
    
    # 验证找到了多个解
    assert len(solutions) > 1
    
    # 验证所有解都是有效的
    for solution in solutions:
        assert solver.apply_solution(solution)
        assert multi_solution_puzzle.is_complete()
        
        # 验证每个解都使用了所有拼图片
        used_pieces = set(piece_id for piece_id, _, _, _ in solution)
        assert len(used_pieces) == 4
        
        # 重置拼图状态
        multi_solution_puzzle.board = [[None] * 2 for _ in range(2)]


def test_solution_uniqueness(multi_solution_puzzle):
    """测试解的唯一性（确保没有重复的解）"""
    solver = PuzzleSolver(multi_solution_puzzle)
    solutions = list(solver.find_all_solutions())
    
    # 将解转换为可哈希的形式以检查唯一性
    solution_tuples = [tuple(sorted((piece_id, row, col, rot) 
                     for piece_id, row, col, rot in solution))
                     for solution in solutions]
    unique_solutions = set(solution_tuples)
    
    # 验证没有重复的解
    assert len(solutions) == len(unique_solutions)


def test_solution_symmetry(multi_solution_puzzle):
    """测试解的对称性"""
    solver = PuzzleSolver(multi_solution_puzzle)
    solutions = list(solver.find_all_solutions())
    
    # 找到包含特定片在不同位置的解
    piece_positions = {}
    for solution in solutions:
        for piece_id, row, col, rot in solution:
            if piece_id not in piece_positions:
                piece_positions[piece_id] = set()
            piece_positions[piece_id].add((row, col))
    
    # 验证某些片可以出现在多个位置
    pieces_with_multiple_positions = [piece_id for piece_id, positions 
                                    in piece_positions.items() 
                                    if len(positions) > 1]
    assert len(pieces_with_multiple_positions) > 0


def test_solution_rotation_variants(multi_solution_puzzle):
    """测试解的旋转变体"""
    solver = PuzzleSolver(multi_solution_puzzle)
    solutions = list(solver.find_all_solutions())
    
    # 检查同一个片在不同解中的不同旋转
    piece_rotations = {}
    for solution in solutions:
        for piece_id, row, col, rot in solution:
            if piece_id not in piece_rotations:
                piece_rotations[piece_id] = set()
            piece_rotations[piece_id].add(rot)
    
    # 验证至少有一个片有多个有效的旋转角度
    pieces_with_multiple_rotations = [piece_id for piece_id, rotations 
                                    in piece_rotations.items() 
                                    if len(rotations) > 1]
    assert len(pieces_with_multiple_rotations) > 0 