import pytest
import yaml
from pathlib import Path
from utils.logger import logger

DATA_PATH = Path("data/test_data.yaml")
with open(DATA_PATH, encoding="utf-8") as f:
    TEST_DATA = yaml.safe_load(f)

@pytest.mark.regression
def test_view_more_articles(article_page):
    """测试文章区 '查看更多' 功能"""
    article_page.load_home()  # 或直接 navigate 到首页
    article_page.click_view_more_articles()
    # 可添加断言：检查 URL 变化或新内容出现

@pytest.mark.parametrize("article", TEST_DATA["articles"])
def test_read_full_article(article_page, article):
    """数据驱动：点击具体文章的 '阅读全文'"""
    article_page.load_home()
    article_page.click_read_full(article["title"])
    logger.info(f"Tested read full for article: {article['title']}")