import pytest
from loguru import logger

from sirocco.utils import duckduckgo


@pytest.mark.asyncio
async def test_search():
    query = 'Wikipedia LLM Generative AI'
    pages = await duckduckgo.search(query, max_results=5)

    assert len(pages) == 5
    assert all([
        len(page.title) > 0 and
        len(page.link) > 0 and
        len(page.snippet) > 0 and
        len(page.html_content) > 0 and
        len(page.text_content) > 0
        for page in pages
    ])
    logger.info([page.title for page in pages])
    logger.debug(f'1rst: Page: {pages[0]}')
