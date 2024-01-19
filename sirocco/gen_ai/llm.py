import asyncio
import math
from textwrap import dedent
from typing import Optional

import tiktoken
from loguru import logger
from openai import AsyncOpenAI

from sirocco.gen_ai.parser import GenAIOutputParser
from sirocco.utils import duckduckgo

client = AsyncOpenAI()

SUMMARY_PROMPT = """
    Write a concise summary ({nb_characters} characters) of the following:
    "{content}"
    CONCISE SUMMARY:
"""

COMBINE_PROMPT = """
The following is set of contents:
=====
{contents}
=====

Take these and distill it into a final, consolidated content containing the main information. 
Summary:
"""


async def ask_gpt_35_turbo_instruct(prompt: str, max_tokens: int = 4096):
    response_max_tokens = 1000
    prompt = cleanup_prompt(prompt, max_tokens=max_tokens-response_max_tokens)
    completion = await client.completions.create(
        model='gpt-3.5-turbo-instruct',
        prompt=prompt,
        max_tokens=response_max_tokens
    )
    response = completion.choices[0].text
    return response


async def ask_gpt_35_turbo_16k(prompt: str, max_tokens: int = 16384):
    prompt = cleanup_prompt(prompt, max_tokens=max_tokens-2048)
    messages = [{"role": "system", "content": prompt}]
    completion = await client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=messages,  # type: ignore
        # max_tokens=max_tokens
    )
    response = completion.choices[0].message.content
    return response


MODELS = {
    "gpt-3.5-turbo-instruct": ask_gpt_35_turbo_instruct,
    "gpt-3.5-turbo-16k": ask_gpt_35_turbo_16k,
}


def cleanup_prompt(prompt: str, max_tokens: int = 4096) -> str:
    prompt = dedent(prompt).strip('\n')
    prompt = truncate(prompt, max_tokens)
    return prompt


async def instruct(prompt: str, model: str = "gpt-3.5-turbo-instruct") -> str:
    llm = MODELS[model]
    response = await llm(prompt)
    response = response.strip()
    return response


async def batch_instruct(prompts: list[str], model: str = "gpt-3.5-turbo-instruct") -> list[str]:
    results = await asyncio.gather(*[
        instruct(prompt, model=model)
        for prompt in prompts
    ])
    return results


async def summarize(content: str, nb_characters: int = 1000) -> str:
    prompt = SUMMARY_PROMPT.format(content=content, nb_characters=nb_characters)
    summary = await instruct(prompt, model="gpt-3.5-turbo-16k")
    return summary


async def combine(contents: list[str]) -> str:
    combined_contents = "\n=====\n".join(contents)
    prompt = COMBINE_PROMPT.format(contents=combined_contents)
    result = await instruct(prompt, model="gpt-3.5-turbo-16k")
    return result


async def rag(search_query: str,
              summary_prompt: str = SUMMARY_PROMPT,
              combine_prompt: str = COMBINE_PROMPT,
              output_parser: Optional[GenAIOutputParser] = None,
              max_search_results: int = 3):
    logger.info(f'Searching with {search_query} ...')
    web_pages = await duckduckgo.search(search_query, max_search_results)

    logger.info(f'Summarizing {len(web_pages)} pages ...')
    summary_prompts = [
        summary_prompt.format(content=web_page.text_content, nb_characters=1000)
        for web_page in web_pages
    ]
    summaries = await batch_instruct(summary_prompts, model="gpt-3.5-turbo-16k")
    combined_summaries = "\n=====\n".join(summaries)
    logger.info(f'Summaries:\n{combined_summaries}')
    logger.info(f'Combining summaries (length: {len(combined_summaries)}) ...')
    format_instructions = output_parser.get_format_instructions() if output_parser else None
    combine_prompt = combine_prompt.format(contents=combined_summaries, format_instructions=format_instructions)
    result = await instruct(combine_prompt, model="gpt-3.5-turbo-16k")

    if output_parser:
        result = output_parser.parse(result)

    return result


def get_num_tokens(content: str, encoding_name: str = 'cl100k_base') -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(content))
    return num_tokens


def truncate(content: str, max_tokens: int) -> str:
    num_tokens = get_num_tokens(content)
    ratio = num_tokens / max_tokens

    while ratio > 1.0:
        new_length = math.ceil(len(content) / ratio)
        content = content[:new_length]
        num_tokens = get_num_tokens(content)
        ratio = num_tokens / max_tokens

    return content
