import pytest
from utils.logger import logger

@pytest.mark.smoke
def test_homepage_load(home_page):
    home_page.load()
    assert home_page.get_daily_challenge_title().is_visible()
    logger.info("✅ 首页加载成功，文案校验通过")
    home_page.screenshot("homepage")