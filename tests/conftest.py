import pytest
import os
import allure
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
        Tester= saykanz
        Run_Time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    try:
        os.makedirs(report_dir, exist_ok=True)
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        logger.info(f"Allure 环境信息已生成: {env_file}")
    except Exception as e:
        logger.warning(f"生成 Allure 环境文件失败: {e}")



# ====================== 失败时自动截图并附加到allure中 ======================
@pytest.hookimpl(tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport(item,call):
    """pytest 核心钩子：测试执行后判断是否失败，失败时自动截图并附加到allure"""
    outcome = yield
    rep = outcome.get_result()
    #旨在call阶段（测试主体执行）且失败时处理
    if rep.when == "call" and rep.failed:
        try:
            # 从item中获取page fixture
            page = item.funcargs.get("page")
            if page:
                screenshot_bytes = page.screenshot()
                allure.attach(
                    screenshot_bytes,
                    name = f"失败截图_{item.name}",
                    attachment_type = allure.attachment_type.PNG
                )
                logger.info(f"失败自动截图已附加到 Allure:{item.name}")
        except Exception as e:
            logger.warning(f"自动附件失败截图失败：{e}")

# ====================== Fixtures ======================
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = getattr(p, BROWSER)
        browser = browser_type.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    page_obj = context.new_page()
    page_obj.set_default_timeout(TIMEOUT)
    yield page_obj
    context.tracing.stop(path="trace.zip")
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

@pytest.fixture(scope="function")
def latest_content(page):
    from page_objects.latest_content_page import LatestContent
    return LatestContent(page)

# ==================== 2. 响应式设计 + 分辨率适配 ====================
with sync_playwright() as p:
    devices = p.devices

    viewports = [
    {"name": "Desktop_FullHD", "viewport": {"width": 1920, "height": 1080}},
    {"name": "Desktop_1366x768", "viewport": {"width": 1366, "height": 768}},
    {"name": "Tablet_iPad", "viewport": devices["iPad Pro 11"]["viewport"]},
    {"name": "Mobile_iPhone14", "viewport": devices["iPhone 14"]["viewport"]},
    {"name": "Mobile_Small", "viewport": {"width": 375, "height": 667}},
]

@pytest.fixture(params=viewports,ids=lambda x: f"viewport_{x}")
def responsive_page(page,request):
    viewport_config = request.param["viewport"]
    page.set_viewport_size(viewport_config)
    with allure.step(f"切换视口：{request.param['name']}({viewport_config})"):
        yield page

