import pytest
import allure
import yaml
from pathlib import Path
from utils.logger import logger
from playwright.sync_api import expect

DATA_PATH = Path("data/test_data.yaml")
with open(DATA_PATH,encoding="utf-8") as f:
    TEST_DATA = yaml.safe_load(f)

@allure.feature("【最新内容】板块")
@allure.story("最新内容的卡片展示")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.parametrize("latest",TEST_DATA["latests"])
@allure.title("验证卡片可见性")
def test_latest_card_visibility(latest, latest_content):
    latest_content.load_home()

    latest_content.tab_switch(latest["tab"])

    title = latest.get("name") or latest.get("title")

    card = latest_content.get_card(title)

    expect(card).to_be_visible()









