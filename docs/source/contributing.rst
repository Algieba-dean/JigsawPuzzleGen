贡献指南
========

我们欢迎所有形式的贡献，包括但不限于：

* 代码贡献
* 文档改进
* Bug 报告
* 功能建议

开发环境设置
-----------

1. 克隆仓库：

.. code-block:: bash

    git clone https://github.com/yourusername/JigsawPuzzle.git
    cd JigsawPuzzle

2. 创建虚拟环境：

.. code-block:: bash

    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate

3. 安装依赖：

.. code-block:: bash

    pip install -r requirements.txt

代码规范
--------

我们使用以下工具来确保代码质量：

* **black**：代码格式化
* **isort**：导入语句排序
* **pylint**：代码质量检查
* **mypy**：类型检查

所有代码都必须通过这些工具的检查。你可以手动运行这些工具：

.. code-block:: bash

    # 格式化代码
    black .
    
    # 排序导入
    isort .
    
    # 代码质量检查
    pylint src tests
    
    # 类型检查
    mypy src tests

提交代码
--------

1. 创建新分支：

.. code-block:: bash

    git checkout -b feature/your-feature-name

2. 提交更改：

.. code-block:: bash

    git add .
    git commit -m "feat: 添加新功能"

我们使用 `约定式提交 <https://www.conventionalcommits.org/zh-hans/v1.0.0/>`_ 规范。

3. 推送更改：

.. code-block:: bash

    git push origin feature/your-feature-name

4. 创建 Pull Request

测试
----

所有新代码都必须包含测试。运行测试：

.. code-block:: bash

    pytest

文档
----

更新文档：

1. 修改 RST 文件
2. 构建文档：

.. code-block:: bash

    cd docs
    make html

3. 检查 build/html/index.html

发布流程
--------

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建发布标签
4. 发布到 PyPI

问题反馈
--------

* 使用 GitHub Issues 报告 bug
* 使用 GitHub Discussions 讨论新功能
* 通过 Pull Request 提交改进 