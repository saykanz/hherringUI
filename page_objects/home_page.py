from .base_page import BasePage
from config.settings import BASE_URL

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = BASE_URL

    def load(self):
        self.navigate()

    def get_daily_challenge_title(self):
        return self.get_by_text("今日挑战等你来解")

    def click_puzzle_challenge(self):
        self.page.get_by_text("立即挑战", exact=True).first.click()

