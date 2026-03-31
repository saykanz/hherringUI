from .base_page import BasePage
from utils.logger import logger
import re

class ArticlePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_view_more_articles(self):
        self.page.locator("div").filter(has_text=re.compile(r"^📖 精选文章查看更多$")).get_by_role("button").click()
        logger.info("Clicked '查看更多' in articles section")
        self.screenshot("articles_more")

    def click_read_full(self, article_title: str):
        card = self.page.get_by_text(article_title).locator("..")
        read_btn = card.get_by_text("阅读全文", exact=True)
        if read_btn.is_visible():
            read_btn.click()
            logger.info(f"Clicked '阅读全文' for: {article_title}")
            self.screenshot(f"article_{article_title[:10]}")

    def load_home(self):
        # 加载首页
        self.navigate()
