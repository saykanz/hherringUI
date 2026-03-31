import pytest
import yaml
from pathlib import Path
import allure

DATA_PATH = Path("data/test_data.yaml")
with open(DATA_PATH, encoding="utf-8") as f:
    TEST_DATA = yaml.safe_load(f)

@allure.feature("文章模块")
@allure.story("文章查看更多")
@allure.title("测试文章区『查看更多』功能")
def test_view_more_articles(article_page):
    article_page.load_home()
    with allure.step("点击查看更多"):
        article_page.click_view_more_articles()


@allure.feature("文章模块")
@allure.story("阅读全文")
@pytest.mark.parametrize("article", TEST_DATA["articles"])
@allure.title("点击阅读全文 - {article[title]}")
def test_read_full_article(article_page, article):
    article_page.load_home()
    with allure.step(f"点击文章 '{article['title']}' 的阅读全文"):
        article_page.click_read_full(article["title"])