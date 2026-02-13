from fastapi import APIRouter, Depends
from app.agents.chat_agent import chat_reply
from app.agents.crm_sub_agent import crm_sub_agent
from app.core.security import authenticate
from app.core.database import SessionLocal
from app.schemas.chat_schema import ChatRequest
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    user=Depends(authenticate),
    db=Depends(get_db)
): 
    msg= request.msg
    # Main banking chatbot response
    reply = chat_reply(msg)

    #  CRM Sub-Agent (silent)
    crm_result = await crm_sub_agent(
        message=msg,
        user_id=user,  # adjust if your auth returns differently
        db=db
    )

    #  Append complaint confirmation if needed
    if crm_result:
        reply += (
            f"\n\n📌 Your complaint has been registered.\n"
            f"Category: {crm_result['category']}\n"
            f"Severity: {crm_result['severity']}\n"
            "Our support team will contact you shortly."
        )

    return {"reply": reply}
