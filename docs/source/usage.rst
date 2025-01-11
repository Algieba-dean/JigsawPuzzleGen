使用指南
========

基本概念
--------

JigsawPuzzle 库主要包含三个核心组件：

1. **拼图块（Piece）**：表示单个拼图块
2. **拼图（Puzzle）**：整个拼图的数据结构
3. **求解器（Solver）**：实现拼图的解决算法

基础用法
--------

创建拼图
--------

.. code-block:: python

    from src.models.puzzle import Puzzle
    from src.models.piece import Piece

    # 创建拼图块
    pieces = [
        Piece(id=1, edges=[1, 2, 3, 4]),
        Piece(id=2, edges=[4, 5, 6, 1]),
        # ... 更多拼图块
    ]

    # 创建拼图
    puzzle = Puzzle(pieces=pieces, width=3, height=3)

解决拼图
--------

.. code-block:: python

    from src.solvers.puzzle_solver import PuzzleSolver

    # 创建求解器
    solver = PuzzleSolver(puzzle)

    # 解决拼图
    solution = solver.solve()

    # 检查解决方案
    if solution:
        print("拼图已解决！")
        print(solution)
    else:
        print("未找到解决方案")

生成拼图
--------

.. code-block:: python

    from src.generators.puzzle_generator import PuzzleGenerator

    # 创建生成器
    generator = PuzzleGenerator()

    # 生成 3x3 的拼图
    puzzle = generator.generate(width=3, height=3)

高级用法
--------

自定义求解策略
------------

您可以通过继承 `PuzzleSolver` 类来实现自己的求解策略：

.. code-block:: python

    class MyCustomSolver(PuzzleSolver):
        def solve(self):
            # 实现您的求解算法
            pass

性能优化
--------

1. 使用多线程求解：

.. code-block:: python

    solver = PuzzleSolver(puzzle, use_threads=True)
    solution = solver.solve()

2. 使用缓存：

.. code-block:: python

    solver = PuzzleSolver(puzzle, use_cache=True)
    solution = solver.solve()

错误处理
--------

.. code-block:: python

    try:
        solution = solver.solve()
    except ValueError as e:
        print(f"输入错误: {e}")
    except RuntimeError as e:
        print(f"求解错误: {e}")

最佳实践
--------

1. 总是验证拼图块的完整性
2. 使用适当的拼图大小
3. 考虑使用缓存提高性能
4. 正确处理异常情况
5. 在处理大型拼图时使用多线程 