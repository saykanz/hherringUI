from playwright.sync_api import Page, Locator
from utils.logger import logger
from config.settings import BASE_URL
from datetime import datetime

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger

    def navigate(self, url: str = ""):
        full_url = f"{BASE_URL}{url}" if not url.startswith("http") else url
        self.page.goto(full_url, wait_until="networkidle")
        self.logger.info(f"Navigate to {full_url}")

    def get_by_text(self, text: str, exact: bool = True) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def screenshot(self, name: str = "screenshot"):
        path = f"reports/{name}_{datetime.now().strftime('%H%M%S')}.png"
        self.page.screenshot(path=path)
        self.logger.info(f"Screenshot saved: {path}")