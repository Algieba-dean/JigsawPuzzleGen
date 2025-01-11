拼图求解器（PuzzleSolver）
========================

.. automodule:: src.solvers.puzzle_solver
   :members:
   :undoc-members:
   :show-inheritance:

类图
----

.. code-block:: text

   +------------------+
   |   PuzzleSolver   |
   +------------------+
   | - puzzle         |
   | - use_threads    |
   | - use_cache      |
   +------------------+
   | + solve()        |
   | + validate()     |
   | + get_solution() |
   +------------------+

示例
----

.. code-block:: python

    from src.models.puzzle import Puzzle
    from src.solvers.puzzle_solver import PuzzleSolver
    
    # 创建拼图
    puzzle = Puzzle(pieces=pieces, width=3, height=3)
    
    # 创建求解器
    solver = PuzzleSolver(
        puzzle=puzzle,
        use_threads=True,  # 使用多线程
        use_cache=True     # 使用缓存
    )
    
    # 解决拼图
    solution = solver.solve()
    
    if solution:
        print("找到解决方案！")
        print(solver.get_solution()) 