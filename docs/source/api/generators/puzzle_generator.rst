拼图生成器（PuzzleGenerator）
==========================

.. automodule:: src.generators.puzzle_generator
   :members:
   :undoc-members:
   :show-inheritance:

类图
----

.. code-block:: text

   +------------------+
   | PuzzleGenerator  |
   +------------------+
   | - config         |
   +------------------+
   | + generate()     |
   | + validate()     |
   +------------------+

示例
----

.. code-block:: python

    from src.generators.puzzle_generator import PuzzleGenerator
    
    # 创建生成器
    generator = PuzzleGenerator(
        min_edge_value=1,
        max_edge_value=100
    )
    
    # 生成 3x3 的拼图
    puzzle = generator.generate(
        width=3,
        height=3,
        ensure_solvable=True  # 确保生成的拼图可解
    )
    
    # 验证生成的拼图
    if generator.validate(puzzle):
        print("生成的拼图有效") 