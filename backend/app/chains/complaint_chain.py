from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Output schema
response_schemas = [
    ResponseSchema(name="is_complaint", description="true if message is a complaint"),
    ResponseSchema(name="category", description="PRICE, SERVICE, PRODUCT, or NONE"),
    ResponseSchema(name="severity", description="LOW, MEDIUM, or HIGH"),
    ResponseSchema(name="sentiment_score", description="number between -1 and 1")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# Prompt
prompt = ChatPromptTemplate.from_template("""
You are a banking CRM classification engine.
You MUST classify the message.
DO NOT answer the user.
ONLY return structured JSON.

Rules:
- If user expresses dissatisfaction, anger, loss, delay, wrong charge → is_complaint = true
- Requests, greetings, questions → is_complaint = false

User message:
{message}

{format_instructions}
""")

complaint_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=output_parser
)
