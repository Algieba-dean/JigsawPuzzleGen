安装指南
========

系统要求
--------

* Python 3.8 或更高版本
* pip 包管理器

通过 pip 安装
------------

推荐使用 pip 安装最新的稳定版本::

    pip install jigsawpuzzle

从源代码安装
-----------

你也可以从 GitHub 仓库直接安装最新的开发版本::

    git clone https://github.com/yourusername/JigsawPuzzle.git
    cd JigsawPuzzle
    pip install -e .

开发环境设置
-----------

如果你想参与开发，需要安装额外的开发依赖::

    pip install -r requirements.txt

验证安装
--------

安装完成后，你可以运行以下命令来验证安装是否成功::

    python -c "from src.models.puzzle import Puzzle; print('安装成功！')" 