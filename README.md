# 拼图游戏

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

这是一个拼图游戏的 Python 实现，支持生成和求解任意大小的拼图。

## 功能特点

- 支持生成任意大小的拼图
- 智能拼图求解器，可以找到所有可能的解决方案
- 支持角落片、边缘片和普通片的自动识别
- 支持拼图片的旋转（0°, 90°, 180°, 270°）
- 提供完整的边缘匹配检查
- 支持打乱拼图和验证解决方案
- 提供详细的拼图状态展示

## 项目结构

```
jigsaw_puzzle/
├── src/
│   ├── models/
│   │   ├── direction.py   # 方向枚举
│   │   ├── piece.py       # 拼图片类
│   │   └── puzzle.py      # 拼图类
│   ├── solvers/
│   │   └── puzzle_solver.py  # 拼图求解器
│   └── generators/
│       └── puzzle_generator.py  # 拼图生成器
├── tests/                 # 测试用例
├── examples/             # 使用示例
└── requirements.txt      # 项目依赖
```

## 安装

```bash
git clone <repository-url>
cd jigsaw_puzzle
pip install -r requirements.txt
```

## 使用示例

### 1. 创建并求解拼图

```python
from src.models.puzzle import JigsawPuzzle
from src.solvers.puzzle_solver import PuzzleSolver

# 生成一个2x2的拼图
puzzle = JigsawPuzzle.generate_solvable_puzzle(rows=2, cols=2, edge_types=2)

# 打乱拼图
puzzle.shuffle()

# 创建求解器
solver = PuzzleSolver(puzzle)

# 查找解决方案
solutions = list(solver.find_all_solutions(max_solutions=1))
if solutions:
    # 应用第一个解决方案
    solver.apply_solution(solutions[0])
    # 打印结果
    puzzle.print_board()
```

### 2. 手动创建拼图

```python
from src.models.puzzle import JigsawPuzzle
from src.models.piece import JigsawPiece
from src.models.direction import Direction

# 创建2x2拼图
puzzle = JigsawPuzzle(2, 2)

# 添加拼图片（示例）
piece = JigsawPiece(1, {
    Direction.UP: 0,     # 0表示平边
    Direction.RIGHT: 1,  # 凸起
    Direction.DOWN: 2,   # 凸起
    Direction.LEFT: 0    # 平边
}, is_corner=True)

puzzle.add_piece(piece)
```

## 测试

运行所有测试：
```bash
pytest tests/
```

运行特定测试：
```bash
pytest tests/test_puzzle.py
pytest tests/test_solver.py
```

## 注意事项

- 拼图片的边缘值必须配对（正值表示凸起，负值表示凹陷）
- 边缘和角落的拼图片外侧必须是平边（值为0）
- 旋转角度必须是90度的倍数

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 