from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.handlers.handler import chat_agent_handler, get_all_threads_handler, chat_history_handler
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from fastapi.responses import StreamingResponse
from src.handlers.handler import chat_streaming_handler
from src.services.thread_memory_store import thread_store

router = APIRouter()


@router.post("/chat/{thread_id}")
def chat_agent_route(thread_id: str, message: str)-> ChatAgentState:
    """
    """
    return chat_agent_handler(thread_id=thread_id, message=message)

@router.get("/chat/threads")
def get_all_threads() -> list[str | None]:
    """
    Docstring for get_all_threads
    """
    return get_all_threads_handler()

@router.get('/chat/history/{thread_id}')
def get_chat_history(thread_id: str) -> ChatAgentState | dict[None, None]:
    """
    Docstring for get_chat_history
    
    :param thread_id: Description
    :type thread_id: str
    """
    return chat_history_handler(thread_id = thread_id)

@router.get("/chat/stream/{thread_id}")
def chat_stream(thread_id: str, message: str):
    return StreamingResponse(
        chat_streaming_handler(thread_id, message),
        media_type="text/plain"
    )

@router.get("/debug/store")
def debug_store():
    """Debug endpoint to check store status"""
    all_threads = thread_store.get_all_threads()
    store_data = {}
    for thread_id in all_threads:
        messages = thread_store.get_messages(thread_id)
        store_data[thread_id] = {
            "count": len(messages),
            "messages": [{"type": msg.__class__.__name__, "content": msg.content[:50]} for msg in messages]
        }
    return {"total_threads": len(all_threads), "threads": store_data}