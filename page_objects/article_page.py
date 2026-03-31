from .base_page import BasePage
from utils.logger import logger

class ArticlePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def click_view_more_articles(self):
        self.get_by_text("查看更多", exact=True).click()
        logger.info("Clicked '查看更多' in articles section")
        self.screenshot("articles_more")

    def click_read_full(self, article_title: str):
        card = self.page.get_by_text(article_title).locator("..")
        read_btn = card.get_by_text("阅读全文", exact=True)
        if read_btn.is_visible():
            read_btn.click()
            logger.info(f"Clicked '阅读全文' for: {article_title}")
            self.screenshot(f"article_{article_title[:10]}")