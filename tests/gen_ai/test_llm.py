import pytest
from loguru import logger

from sirocco.gen_ai import llm
from sirocco.gen_ai.parser import JSONArrayOutputParser


@pytest.mark.asyncio
async def test_instruct():
    response = await llm.instruct("""
        You are a calculator, compute the result of the given input.
        Input: 41 + 1
        Output: 
    """)
    assert response == "42"


@pytest.mark.asyncio
async def test_batch_instruct():
    prompts = [
        f"""
        You are a calculator, compute the result of the given input.
        Input: 41 + {i}
        Output: 
        """
        for i in range(3)
    ]

    responses = await llm.batch_instruct(prompts)
    assert responses == ["41", "42", "43"]


@pytest.mark.asyncio
async def test_rag():
    response = await llm.rag("What's a LLM?")
    logger.info("What's a LLM?:\n", response)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_rag_with_custom_prompts():
    extract_table_of_contents_prompt = """
    Act as an assistant to kickstart the creation of a new online course.
    Your task : 
    - Write a concise summary ({nb_characters} characters) of the following text delimited by triple backquotes.
    - Return your response in bullet points which only includes a plan (table of contents) for a course about NoSQL.
    
    ```{content}```
    """
    create_table_of_contents_prompt = """
    Act as an assistant to kickstart the creation of a new online course.
    Your task : 
    - Generate 5-7 chapter titles for the new course.
    - Get inspiration from the following tables of contents delimited by triple backquotes
    
    ```{contents}```

    Use language: french
    {format_instructions}
    """

    output_parser = JSONArrayOutputParser(example='["Header title 1", "Header title 2", "Header title 3"]')

    result = await llm.rag(
        "Course Introduction to NoSQL",
        summary_prompt=extract_table_of_contents_prompt,
        combine_prompt=create_table_of_contents_prompt,
        output_parser=output_parser
    )
    logger.info("RAG", result)
    assert len(result) > 0


def test_truncate():
    content = 'tiktoken is great !'
    max_tokens = 5
    result = llm.truncate(content, max_tokens)
    assert result == 'tiktoken is gr'
