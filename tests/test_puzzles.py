import pytest
import yaml
from pathlib import Path
from utils.logger import logger
import allure

# 加载测试数据
DATA_PATH = Path("data/test_data.yaml")
with open(DATA_PATH, encoding="utf-8") as f:
    TEST_DATA = yaml.safe_load(f)


@allure.feature("谜题模块")  # Behaviors → Feature
@allure.story("精选谜题卡片展示")  # Behaviors → Story
@allure.severity(allure.severity_level.CRITICAL)  # 严重程度
@pytest.mark.regression
@pytest.mark.parametrize("puzzle", TEST_DATA["puzzles"])
@allure.title("验证谜题卡片可见性 - {puzzle[name]}")  # 自定义测试标题（支持参数化）
def test_puzzle_card_visibility(puzzle_page, puzzle):
    """数据驱动：验证多个精选谜题卡片是否可见"""
    with allure.step("加载首页"):
        puzzle_page.load_home()

    with allure.step(f"检查谜题 '{puzzle['name']}' 卡片是否可见"):
        card = puzzle_page.get_puzzle_card(puzzle["name"])
        assert card.is_visible(), f"谜题卡片 '{puzzle['name']}' 未显示"
        logger.info(f"✅ Puzzle card visible: {puzzle['name']}")

    puzzle_page.screenshot(f"puzzle_card_{puzzle['name'][:10]}")


@allure.feature("谜题模块")
@allure.story("谜题挑战功能")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.parametrize("puzzle", TEST_DATA["puzzles"])
@allure.title("点击立即挑战按钮 - {puzzle[name]}")
def test_click_challenge_button(puzzle_page, puzzle):
    """数据驱动：测试点击立即挑战按钮"""
    puzzle_page.load_home()
    puzzle_page.click_challenge_button(puzzle["name"])
    # 可根据实际页面继续添加断言


@allure.feature("谜题模块")
@allure.story("谜题信息校验")
@pytest.mark.parametrize("puzzle", TEST_DATA["puzzles"])
@allure.title("验证谜题难度与人数 - {puzzle[name]}")
def test_puzzle_info_validation(puzzle_page, puzzle):
    """数据驱动：验证难度标签和挑战人数"""
    puzzle_page.load_home()
    puzzle_page.verify_puzzle_info(
        puzzle["name"],
        puzzle["difficulty"],
        puzzle["challenges"]
    )