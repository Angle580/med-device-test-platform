# 医疗器械生命体征监测系统 — 全流程自动化测试平台

针对医疗器械设备数据管理后端，基于 Python + pytest 搭建的自动化测试平台。

## 技术栈

- 被测系统: FastAPI + SQLAlchemy + MySQL 8.0
- 测试框架: pytest + Requests + Allure
- 质量门禁: flake8 (静态分析) + coverage (白盒覆盖率)
- CI/CD: GitHub Actions
- 提效工具: 数据生成器 / Mock Server / 质量看板

## 项目结构

```
├── sut/                    # 被测系统(FastAPI后端)
│   ├── main.py            # 入口
│   ├── models.py          # 数据模型
│   ├── report_engine.py    # 风险评级核心逻辑(白盒测试目标)
│   └── routers/           # 业务路由
├── autotest/              # 自动化测试框架
│   ├── common/            # 封装: HTTP/DB/日志/断言
│   ├── testcases/         # 接口测试用例
│   ├── tools/             # 提效工具
│   └── conftest.py        # pytest全局夹具
├── unit_tests/            # 单元测试(白盒覆盖)
├── .github/workflows/      # CI/CD流水线
└── pytest.ini
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt
pip install -r sut/requirements.txt

# 2. 启动MySQL并建库
# mysql> CREATE DATABASE med_device CHARACTER SET utf8mb4;

# 3. 启动被测系统
uvicorn sut.main:app --reload --port 8000

# 4. 跑接口自动化
pytest autotest/testcases/ -v

# 5. 跑单元测试+覆盖率
coverage run -m pytest unit_tests/ -v && coverage report -m

# 6. 静态检查
flake8 autotest/ --max-line-length=120
```

## 覆盖的测试能力

| 能力 | 实现 |
|---|---|
| 接口自动化 | pytest + Requests 封装 |
| 单元测试 | pytest + 参数化分支覆盖 |
| 白盒测试 | coverage.py 行/分支覆盖率 |
| 静态分析 | flake8 CI门禁 |
| CI/CD | GitHub Actions 自动流水线 |
| 数据库校验 | pymysql 断言数据落库正确性 |
| 提效工具 | Faker数据生成 / Mock Server / 质量看板 |
| Linux部署 | Ubuntu + systemctl + uvicorn |
