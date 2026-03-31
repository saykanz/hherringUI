import pytest
from playwright.sync_api import sync_playwright
from page_objects.home_page import HomePage
from config.settings import BROWSER, HEADLESS, TIMEOUT
from utils.logger import logger

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
    page = context.new_page()
    page.set_default_timeout(TIMEOUT)
    yield page
    context.close()

@pytest.fixture(scope="function")
def home_page(page):
    return HomePage(page)

# 可继续添加 login_page fixture 等

@pytest.fixture(scope="function")
def puzzle_page(page):
    from page_objects.puzzle_page import PuzzlePage
    return PuzzlePage(page)

@pytest.fixture(scope="function")
def article_page(page):
    from page_objects.article_page import ArticlePage
    return ArticlePage(page)