# 拼图游戏

这是一个拼图游戏的Python实现，支持生成和求解任意大小的拼图。

## 功能特点

- 支持生成任意大小的拼图
- 可以生成所有可能的拼图配置
- 支持查找所有可能的解决方案
- 提供拼图片旋转和匹配功能
- 支持边缘和角落拼图片的识别

## 项目结构

```
jigsaw_puzzle/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── direction.py
│   │   ├── piece.py
│   │   └── puzzle.py
│   ├── generators/
│   │   ├── __init__.py
│   │   └── puzzle_generator.py
│   └── solvers/
│       ├── __init__.py
│       └── puzzle_solver.py
├── tests/
│   ├── __init__.py
│   ├── test_piece.py
│   └── test_puzzle.py
├── examples/
│   └── basic_usage.py
├── requirements.txt
└── README.md
```

## 安装

```bash
pip install -r requirements.txt
```

## 使用示例

```python
from src.models.puzzle import JigsawPuzzle

# 生成2x2的拼图，有2种边的类型
puzzle = JigsawPuzzle.generate_solvable_puzzle(rows=2, cols=2, edge_types=2)

# 打乱拼图
puzzle.shuffle()

# 查找所有解决方案
solutions = puzzle.find_all_solutions()
```

## 运行测试

```bash
pytest tests/
``` 