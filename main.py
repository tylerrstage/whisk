from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_openai_functions_agent

load_dotenv()

class Response(BaseModel):
    request_type: str # "recipe", "meal_plan", "cooking_tip"
    summary: str
    recipe_name: str | None = None
    ingredients: list[str] = []
    dietary_tags: list[str] = []
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    servings: int | None = None
    difficulty: str | None = None
    tips: list[str] = []
    substitutions: list[str] = []
    sources: list[str]
    tools_used: list[str]

llm = ChatOpenAI(model="gpt-5.4-mini")
parser = PydanticOutputParser(pydantic_object=Response)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "System",
            "You are a helpful assistant that provides cooking advice, recipes, and meal plans. "
            "You will receive a user's request and respond with a structured JSON object containing the relevant information."
            "Wrap the output in this format and provide no other text\n{format_instructions}",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())
