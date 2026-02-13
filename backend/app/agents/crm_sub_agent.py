import uuid
from app.chains.complaint_chain import complaint_chain
from app.models.crm_table import CRMComplaint
from app.models.account import Account
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain
# Output schema
response_schemas = [
    ResponseSchema(name="is_complaint", description="true if message is a complaint"),
    ResponseSchema(name="category", description="PRICE, SERVICE, PRODUCT, or NONE"),
    ResponseSchema(name="severity", description="LOW, MEDIUM, or HIGH"),
    ResponseSchema(name="sentiment_score", description="number between -1 and 1")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()


async def crm_sub_agent(message: str, user_id: str, db):
    analysis = complaint_chain.invoke({
        "message": message,
        "format_instructions": format_instructions
    })

    print("CRM ANALYSIS RAW:", analysis)

    parsed = analysis.get("text", {})
    print("CRM PARSED:", parsed)

    is_complaint = parsed.get("is_complaint", "").lower() == "true"
    if not is_complaint:
        return None

    customer = db.query(Account).filter(
        Account.user_id == user_id   
    ).first()

    if not customer:
        print("Customer not found")
        return None

    complaint = CRMComplaint(
    complaint_id=str(uuid.uuid4()),
    customer_id=customer.user_id,   
    account_id=customer.id,         
    complaint_text=message,
    complaint_category=parsed["category"],
    severity=parsed["severity"],
    sentiment_score=float(parsed["sentiment_score"]),
    status="OPEN"
)
    db.add(complaint)
    db.commit()

    return {
        "category": parsed["category"],
        "severity": parsed["severity"]
    }
