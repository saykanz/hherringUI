import pytest
import yaml
from pathlib import Path
from utils.logger import logger

# 加载测试数据
DATA_PATH = Path("data/test_data.yaml")
with open(DATA_PATH, encoding="utf-8") as f:
    TEST_DATA = yaml.safe_load(f)

@pytest.mark.regression
@pytest.mark.parametrize("puzzle", TEST_DATA["puzzles"])
def test_puzzle_card_visibility(puzzle_page, puzzle):
    """数据驱动：验证多个精选谜题卡片可见性"""
    puzzle_page.load_home()
    card = puzzle_page.get_puzzle_card(puzzle["name"])
    assert card.is_visible(), f"Puzzle card '{puzzle['name']}' not visible"
    logger.info(f"✅ Puzzle card visible: {puzzle['name']}")
    puzzle_page.screenshot(f"puzzle_card_{puzzle['name'][:10]}")

@pytest.mark.smoke
@pytest.mark.parametrize("puzzle", TEST_DATA["puzzles"])
def test_click_challenge_button(puzzle_page, puzzle):
    """数据驱动：点击“立即挑战”按钮（仅点击，不提交答案）"""
    puzzle_page.load_home()
    puzzle_page.click_challenge_button(puzzle["name"])
    # 可根据实际页面添加断言（如跳转或弹窗出现）
    logger.info(f"Tested challenge button for: {puzzle['name']}")

@pytest.mark.parametrize("puzzle", TEST_DATA["puzzles"])
def test_puzzle_info_validation(puzzle_page, puzzle):
    """数据驱动：验证难度和挑战人数等信息"""
    puzzle_page.load_home()
    puzzle_page.verify_puzzle_info(
        puzzle["name"],
        puzzle["difficulty"],
        puzzle["challenges"]
    )