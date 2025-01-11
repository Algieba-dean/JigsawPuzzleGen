from src.generators.puzzle_generator import PuzzleGenerator
from src.models.puzzle import JigsawPuzzle
from src.solvers.puzzle_solver import PuzzleSolver


def main():
    # 生成一个2x2的拼图，有2种边的类型
    puzzle = PuzzleGenerator.generate_solvable_puzzle(rows=2, cols=2, edge_types=2)
    print("初始拼图状态：")
    puzzle.print_board()

    # 打乱拼图
    puzzle.shuffle()
    print("\n打乱后的拼图状态：")
    puzzle.print_board()

    # 创建求解器并查找所有解决方案
    solver = PuzzleSolver(puzzle)
    solutions = solver.find_all_solutions()
    print(f"\n共找到 {len(solutions)} 个解决方案")

    # 打印第一个解决方案
    if solutions:
        print("\n应用第一个解决方案：")
        solver.apply_solution(solutions[0])
        puzzle.print_board()

    # 生成所有可能的拼图配置
    print("\n生成所有可能的拼图配置：")
    all_puzzles = PuzzleGenerator.generate_all_possible_puzzles(
        rows=2, cols=2, edge_types=2, max_combinations=5
    )
    print(f"生成了 {len(all_puzzles)} 种不同的拼图配置")


if __name__ == "__main__":
    main()
