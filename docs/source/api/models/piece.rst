拼图块（Piece）
==============

.. automodule:: src.models.piece
   :members:
   :undoc-members:
   :show-inheritance:

类图
----

.. code-block:: text

   +-------------+
   |    Piece    |
   +-------------+
   | - id: int   |
   | - edges: [] |
   +-------------+
   | + rotate()  |
   | + match()   |
   +-------------+

示例
----

.. code-block:: python

    from src.models.piece import Piece
    
    # 创建一个拼图块
    piece = Piece(id=1, edges=[1, 2, 3, 4])
    
    # 旋转拼图块
    piece.rotate(90)
    
    # 检查两个拼图块是否匹配
    is_match = piece.match(other_piece, direction='right') 