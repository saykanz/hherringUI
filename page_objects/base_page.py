import os
from datetime import datetime
from config.settings import BASE_URL
from utils.logger import logger
import allure
from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger

    def navigate(self, url: str = ""):
        """导航到指定页面"""
        full_url = f"{BASE_URL}{url}" if not url.startswith("http") else url
        with allure.step(f"导航到页面: {full_url}"):
            self.page.goto(full_url, wait_until="networkidle")
            self.logger.info(f"Navigate to {full_url}")
            allure.attach(
                self.page.screenshot(type='png'),
                name="导航后截图",
                attachment_type=allure.attachment_type.PNG
            )

    def get_by_text(self, text: str, exact: bool = True) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def screenshot(self, name: str = "screenshot"):
        """截图并自动附加到 Allure 报告（失败时特别有用）"""
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        filename = f"{screenshot_dir}/{name}_{datetime.now().strftime('%H%M%S')}.png"

        self.page.screenshot(path=filename)
        self.logger.info(f"截图已保存: {filename}")

        # 自动附加到 Allure（即使测试通过也可看到）
        with open(filename, "rb") as f:
            allure.attach(
                f.read(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        return filename