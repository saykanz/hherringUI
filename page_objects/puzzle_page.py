from .base_page import BasePage
from utils.logger import logger
from datetime import datetime

class PuzzlePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def load_home(self):
        self.navigate()

    def get_puzzle_card(self, puzzle_name: str):
        """根据谜题名称定位卡片"""
        return self.page.get_by_text(puzzle_name).locator("..")  # 向上找卡片容器

    def click_challenge_button(self, puzzle_name: str):
        card = self.get_puzzle_card(puzzle_name)
        button = card.get_by_text("立即挑战", exact=True)
        if button.is_visible():
            button.click()
            logger.info(f"Clicked '立即挑战' for puzzle: {puzzle_name}")
            self.screenshot(f"challenge_{puzzle_name.replace('：', '_')}")
        else:
            logger.warning(f"Challenge button not found for {puzzle_name}")

    def verify_puzzle_info(self, puzzle_name: str, difficulty: str, challenges: int):
        card = self.get_puzzle_card(puzzle_name)
        assert card.get_by_text(difficulty).is_visible(), f"Difficulty {difficulty} not found"
        # 挑战人数可能动态，检查是否包含数字
        assert any(str(challenges) in text for text in card.inner_text().split()), f"Challenges count mismatch"
        logger.info(f"✅ Verified puzzle: {puzzle_name} | Difficulty: {difficulty}")