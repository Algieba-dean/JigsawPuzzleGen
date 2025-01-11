class JigsawPiece:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    X_POS = "x_position"
    Y_POS = "y_position"

    def __init__(self):
        # pattern on each side
        self.patterns = {
            self.UP: None,
            self.DOWN: None,
            self.LEFT: None,
            self.RIGHT: None
        }
        # position
        self.position = {
            self.X_POS: None,
            self.Y_POS: None
        }
        # filled condition
        self.filled_condition = {
            self.UP: False,
            self.DOWN: False,
            self.LEFT: False,
            self.RIGHT: False,
        }

    def is_matched(self, other, toward_direction: str):
        match toward_direction:
            case JigsawPiece.LEFT:
                return self.patterns[JigsawPiece.LEFT] == other.patterns[JigsawPiece.RIGHT]
            case JigsawPiece.RIGHT:
                return self.patterns[JigsawPiece.RIGHT] == other.patterns[JigsawPiece.LEFT]
            case JigsawPiece.UP:
                return self.patterns[JigsawPiece.UP] == other.patterns[JigsawPiece.DOWN]
            case JigsawPiece.DOWN:
                return self.patterns[JigsawPiece.DOWN] == other.patterns[JigsawPiece.UP]
            case _:
                raise ValueError(f"wrong toward direction {toward_direction} value in {__name__}")