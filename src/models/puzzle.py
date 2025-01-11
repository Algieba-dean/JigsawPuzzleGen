import random
from typing import List, Optional

from .direction import Direction
from .piece import JigsawPiece


class JigsawPuzzle:
    """表示整个拼图的类"""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board: List[List[Optional[JigsawPiece]]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]
        self.pieces: List[JigsawPiece] = []

    def __repr__(self) -> str:
        """返回拼图的字符串表示"""
        placed_pieces = sum(1 for row in self.board for piece in row if piece is not None)
        total_pieces = len(self.pieces)
        completion = f"{placed_pieces}/{total_pieces}"

        # 获取拼图片的详细信息
        pieces_info = []
        for piece in self.pieces:
            position = piece.position if piece.position else "未放置"
            pieces_info.append(f"ID={piece.id}(位置={position}, 旋转={piece.rotation}°)")
        pieces_str = ", ".join(pieces_info)

        return f"JigsawPuzzle(rows={self.rows}, cols={self.cols}, 已放置={completion}, pieces=[{pieces_str}])"

    def add_piece(self, piece: JigsawPiece) -> None:
        """添加拼图片到拼图中"""
        self.pieces.append(piece)

    def _check_adjacent_piece(
        self, piece: JigsawPiece, row: int, col: int, direction: Direction
    ) -> bool:
        """检查与指定方向相邻拼图片的匹配情况"""
        adjacent_row = row + (direction == Direction.DOWN) - (direction == Direction.UP)
        adjacent_col = col + (direction == Direction.RIGHT) - (direction == Direction.LEFT)

        if not (0 <= adjacent_row < self.rows and 0 <= adjacent_col < self.cols):
            return True

        adjacent_piece = self.board[adjacent_row][adjacent_col]
        return not adjacent_piece or piece.matches(adjacent_piece, direction)

    def place_piece(self, piece: JigsawPiece, row: int, col: int) -> bool:
        """在指定位置放置拼图片"""
        if not (0 <= row < self.rows and 0 <= col < self.cols) or self.board[row][col]:
            return False

        # 检查四个方向的匹配情况
        for direction in Direction:
            if not self._check_adjacent_piece(piece, row, col, direction):
                return False

        self.board[row][col] = piece
        piece.set_position(row, col)
        return True

    def is_complete(self) -> bool:
        """检查拼图是否完成"""
        return all(all(piece is not None for piece in row) for row in self.board)

    def print_board(self) -> None:
        """打印当前拼图状态"""
        for row in self.board:
            print(" ".join(str(piece.id) if piece else "X" for piece in row))

    def shuffle(self) -> None:
        """打乱拼图片的顺序和方向"""
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        random.shuffle(self.pieces)
        for piece in self.pieces:
            piece.rotate(random.choice([0, 90, 180, 270]))
            piece.position = (None, None)

    def get_solution(self) -> List[tuple[int, int, int, int]]:
        """获取当前拼图状态作为解决方案"""
        solution = []
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if piece:
                    solution.append((piece.id, row, col, piece.rotation))
        return solution
