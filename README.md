# hherringUI - 红鲱鱼 UI 自动化测试框架

基于 Playwright + Pytest 的企业级 UI 自动化框架，专用于 https://hherring.cn/ 推理社区。

## 快速启动
```bash
pip install -r requirements.txt
playwright install
# 清空旧结果并运行（推荐）
python -m pytest -n auto --alluredir=allure-results --clean-alluredir -q 
allure serve allure-results

##完整企业级目录
hherringUI/
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── test_data.yaml
│   └── test_users.yaml
├── logs/
├── page_objects/
│   ├── __init__.py
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── article_page.py
│   └── puzzle_page.py
├── reports/                  # Allure 报告输出目录（git ignore）
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_homepage.py
│   ├── test_login.py
│   ├── test_articles.py
│   └── test_puzzles.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── helpers.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── pytest.ini
├── README.md
└── requirements.txt