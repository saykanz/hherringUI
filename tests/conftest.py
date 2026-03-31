import pytest
import allure
import os
from playwright.sync_api import sync_playwright
from config.settings import BROWSER, HEADLESS, TIMEOUT, BASE_URL
from utils.logger import logger
from datetime import datetime


# ====================== Allure 环境信息自动生成 ======================
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时，自动生成 environment.properties，让 Allure 概览页显示环境信息"""
    if not hasattr(session.config.option, 'allure_report_dir') or not session.config.option.allure_report_dir:
        return

    report_dir = session.config.option.allure_report_dir
    env_file = os.path.join(report_dir, 'environment.properties')

    env_content = f"""Browser={BROWSER}
Headless={HEADLESS}
Base_URL={BASE_URL}
Python=3.11+
Playwright_Version=1.51.0
Tester=你自己的名字或 saykanz
Run_Time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    try:
        os.makedirs(report_dir, exist_ok=True)
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        logger.info(f"Allure 环境信息已生成: {env_file}")
    except Exception as e:
        logger.warning(f"生成 Allure 环境文件失败: {e}")


# ====================== Fixtures ======================
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = getattr(p, BROWSER)
        browser = browser_type.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN"
    )
    page_obj = context.new_page()
    page_obj.set_default_timeout(TIMEOUT)
    yield page_obj
    context.close()


@pytest.fixture(scope="function")
def home_page(page):
    from page_objects.home_page import HomePage
    return HomePage(page)


@pytest.fixture(scope="function")
def puzzle_page(page):
    from page_objects.puzzle_page import PuzzlePage
    return PuzzlePage(page)


@pytest.fixture(scope="function")
def article_page(page):
    from page_objects.article_page import ArticlePage
    return ArticlePage(page)