欢迎使用 JigsawPuzzle 文档
==========================

JigsawPuzzle 是一个用于解决和生成拼图问题的 Python 库。

.. toctree::
   :maxdepth: 2
   :caption: 目录:

   installation
   usage
   api/index
   contributing
   changelog

功能特点
--------

* 支持任意大小的拼图问题
* 高效的解题算法
* 灵活的拼图生成器
* 完整的测试覆盖
* 类型提示支持

快速开始
--------

安装::

    pip install jigsawpuzzle

基本使用::

    from src.models.puzzle import Puzzle
    from src.solvers.puzzle_solver import PuzzleSolver

    # 创建拼图
    puzzle = Puzzle(...)
    
    # 解决拼图
    solver = PuzzleSolver(puzzle)
    solution = solver.solve()

索引和表格
----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 