from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.services.saathi_router import saathi_router
from app.schemas.all_schemas import ChatRequest, ChatResponse
from app.models.all_models import ChatMessage, ChatSession

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
def chat_with_saathi(
    req: ChatRequest,
    auth_data = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, farmer = auth_data
    farm = farmer.farms[0] if (farmer and farmer.farms) else None

    # Fetch recent conversation history for multi-turn context
    history_msgs = []
    if farmer:
        query_filter = ChatMessage.farmer_id == farmer.id
        if req.session_id:
            query_filter = (ChatMessage.session_id == req.session_id) & query_filter
        recent = db.query(ChatMessage).filter(query_filter).order_by(ChatMessage.created_at.desc()).limit(6).all()
        recent.reverse()
        history_msgs = [{"sender": m.sender, "text": m.text} for m in recent]

    # Process query through Saathi Intelligence Router
    result = saathi_router.route_and_process(req.message, db, farmer, farm, history=history_msgs)

    # Save to history database if authenticated
    if farmer:
        # Create default session if missing
        session_id = req.session_id
        if not session_id:
            active_session = db.query(ChatSession).filter(ChatSession.farmer_id == farmer.id).order_by(ChatSession.created_at.desc()).first()
            if not active_session:
                active_session = ChatSession(farmer_id=farmer.id, title=req.message[:30])
                db.add(active_session)
                db.commit()
                db.refresh(active_session)
            session_id = active_session.id

        user_msg = ChatMessage(
            session_id=session_id,
            farmer_id=farmer.id,
            sender="user",
            text=req.message
        )
        saathi_msg = ChatMessage(
            session_id=session_id,
            farmer_id=farmer.id,
            sender="assistant",
            text=result["answer"],
            intent=result.get("intent"),
            sources=result.get("sources"),
            structured_data=result.get("structured"),
            is_what_if=result.get("is_what_if", False)
        )
        db.add(user_msg)
        db.add(saathi_msg)
        db.commit()

        result["session_id"] = session_id

    return result

@router.get("/history")
def get_chat_history(session_id: Optional[int] = None, auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return []
    
    query = db.query(ChatMessage).filter(ChatMessage.farmer_id == farmer.id)
    if session_id:
        query = query.filter(ChatMessage.session_id == session_id)
    
    msgs = query.order_by(ChatMessage.created_at.asc()).all()
    return [
        {
            "id": m.id,
            "session_id": m.session_id,
            "sender": m.sender,
            "text": m.text,
            "intent": m.intent,
            "sources": m.sources or [],
            "structured": m.structured_data,
            "is_what_if": m.is_what_if,
            "timestamp": m.created_at.isoformat()
        } for m in msgs
    ]

@router.post("/sessions")
def create_chat_session(title: Optional[str] = "New Chat", auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        raise HTTPException(status_code=401, detail="Authentication required")
    session = ChatSession(farmer_id=farmer.id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "title": session.title, "created_at": session.created_at.isoformat()}

@router.get("/sessions")
def get_chat_sessions(auth_data = Depends(get_current_user), db: Session = Depends(get_db)):
    user, farmer = auth_data
    if not farmer:
        return []
    sessions = db.query(ChatSession).filter(ChatSession.farmer_id == farmer.id).order_by(ChatSession.created_at.desc()).all()
    return [
        {"id": s.id, "title": s.title, "created_at": s.created_at.isoformat()} for s in sessions
    ]
