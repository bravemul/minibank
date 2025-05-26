自动化测试运行说明
# 1. 安装依赖
pip install pytest requests

# 2. 启动Flask服务
python main.py

# 3. 运行测试
pytest --maxfail=2 -v tests/

覆盖率统计说明
# 安装覆盖率插件
pip install pytest-cov

# 运行并查看覆盖率
pytest --cov=app --cov-report=html tests/

# 生成HTML报告
pytest --cov=app --cov-report=html tests/
# 浏览 htmlcov/index.html 查看图形报告

# MiniBank 迷你银行系统

## 项目简介
MiniBank 是基于 Flask + SQLAlchemy 的银行业务后端，支持注册、存取款、转账、流水查询、对账等核心功能，带自动化接口测试和CI/CD，适合测试开发/后端/AI方向项目展示。

## 技术栈
- Flask
- SQLAlchemy
- pytest + requests（自动化测试）
- GitHub Actions（持续集成）
- OpenAI大模型接口（可选AI扩展）

## 主要功能
- 用户注册与开户
- 存款、取款、转账
- 账户流水与对账
- 自动化接口测试
- 代码覆盖率统计
- CI自动化
- AI自然语言接口（可选）

## 快速体验
1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
2. 启动服务
   ```bash
   python main.py
   ```
3. 用 Postman 或 pytest 测试接口

## 自动化测试
```bash
pytest --cov=app --cov-report=term-missing tests/
```

## CI/CD
本项目配置了GitHub Actions，push后自动测试并输出覆盖率。
、
## 亮点总结
- 业务流程完整，接口文档齐全
- 自动化测试&覆盖率报告
- 持续集成，提升开发效率
、

