import asyncio
from typing import Optional

import aiohttp
import html2text
from duckduckgo_search import DDGS  # type: ignore
from loguru import logger
from pydantic import BaseModel

from sirocco.utils.common import require

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


class WebPage(BaseModel):
    title: str
    snippet: str
    link: str
    html_content: Optional[str] = None
    text_content: Optional[str] = None


async def search(query: str, max_results: int = 3) -> list[WebPage]:
    logger.info('Searching ...')
    web_pages = _search(query, max_results)

    logger.info('Loading pages ...')
    # TODO: I should test asyncio.TaskGroup() (requires python 3.11 ?) => Will properly canceled all tasks on failure
    await asyncio.gather(*[
        _load_content(web_page)
        for web_page in web_pages
    ])

    return web_pages


def _search(query: str, max_results: int = 3) -> list[WebPage]:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [
            WebPage(title=result['title'], link=result['href'], snippet=result['body'])
            for result in results
        ]


async def _load_content(web_page: WebPage):
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        async with session.get(web_page.link) as response:
            require(200 <= response.status < 300, f"Could not load {web_page.link} (status: {response.status})")
            web_page.html_content = await response.text()
            web_page.text_content = _extract_text_from_html(web_page.html_content)


def _extract_text_from_html(html_content: str):
    extractor = html2text.HTML2Text()
    extractor.ignore_images = True
    extractor.ignore_links = True
    text_content = extractor.handle(html_content)
    return text_content
