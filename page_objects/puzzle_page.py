from .base_page import BasePage
from utils.logger import logger
import allure

class PuzzlePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def load_home(self):
        """加载首页"""
        self.navigate()

    def get_puzzle_card(self, puzzle_name: str):
        """根据谜题名称定位卡片"""
        return self.page.locator(".puzzle-card").filter(has_text=puzzle_name)


    @allure.step("点击『立即挑战』按钮 - {puzzle_name}")
    def click_challenge_button(self, puzzle_name: str):
        """点击立即挑战按钮"""
        card = self.get_puzzle_card(puzzle_name)
        button = card.get_by_text("立即挑战").first
        if button.is_visible():
            button.click()
            logger.info(f"Clicked '立即挑战' for puzzle: {puzzle_name}")
            self.screenshot(f"challenge_{puzzle_name.replace('：', '_')}")
        else:
            logger.warning(f"Challenge button not found for {puzzle_name}")

    @allure.step("验证谜题信息: {puzzle_name} | 难度: {difficulty}")
    def verify_puzzle_info(self, puzzle_name: str, difficulty: str, challenges: int):
        """验证谜题卡片信息"""
        card = self.get_puzzle_card(puzzle_name)
        assert card.get_by_text(difficulty).is_visible(), f"难度 {difficulty} 未找到"
        # 挑战人数松散校验
        card_text = card.inner_text()
        assert any(str(challenges) in card_text for _ in [1]), f"挑战人数不匹配"
        logger.info(f"✅ Verified puzzle: {puzzle_name}")