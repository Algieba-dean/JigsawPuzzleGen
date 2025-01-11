拼图（Puzzle）
=============

.. automodule:: src.models.puzzle
   :members:
   :undoc-members:
   :show-inheritance:

类图
----

.. code-block:: text

   +-------------+
   |   Puzzle    |
   +-------------+
   | - pieces    |
   | - width     |
   | - height    |
   +-------------+
   | + solve()   |
   | + validate()|
   +-------------+

示例
----

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
    
    # 验证拼图
    if puzzle.validate():
        print("拼图有效") 