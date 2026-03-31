import pytest
import allure
from utils.logger import logger


@allure.feature("首页模块")
@allure.story("首页加载与文案校验")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("验证首页正常加载与每日挑战文案")
@pytest.mark.smoke
def test_homepage_load(home_page):
    with allure.step("加载首页"):
        home_page.load()

    with allure.step("校验『今日挑战』文案是否存在"):
        assert home_page.get_daily_challenge_title().is_visible()
        logger.info("✅ 首页加载成功，文案校验通过")

    home_page.screenshot("homepage")