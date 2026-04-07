from src.agents.chat_agent.graph import create_chat_agent_graph
from langchain.messages import HumanMessage
from langchain_core.messages import BaseMessage
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from typing import Iterator
from src.services.thread_memory_store import thread_store


def convert_message_to_dict(msg: BaseMessage) -> dict:
    """Convert LangChain message to dictionary format for Streamlit"""
    msg_type = type(msg).__name__
    
    if msg_type == "HumanMessage":
        msg_type = "human"
    elif msg_type == "AIMessage":
        msg_type = "ai"
    else:
        msg_type = "ai"  # Default to AI
    
    return {
        "type": msg_type,
        "content": msg.content
    }



def chat_agent_handler(thread_id: str, message : str) -> ChatAgentState:
    """
    Non-streaming chat handler that saves messages to the thread store
    """
    from langchain_core.messages import AIMessage
    
    # Get existing messages
    existing_messages = thread_store.get_messages(thread_id)
    print(f"\n[AGENT] ===== Starting chat_agent_handler for thread {thread_id} =====")
    print(f"[AGENT] Existing messages: {len(existing_messages)}")
    
    # Create human message
    human_msg = HumanMessage(content=message)
    input_messages = existing_messages + [human_msg]
    
    # Get graph and invoke
    graph = create_chat_agent_graph()
    result = graph.invoke(
        input={'messages': input_messages},
        config={'configurable': {'thread_id': thread_id}}
    )
    
    # The result should have messages - extract the AI response
    print(f"[AGENT] Graph returned: {type(result)}")
    if 'messages' in result and result['messages']:
        # Combine: existing messages + human message + AI response messages
        ai_messages = result['messages']
        all_messages = existing_messages + [human_msg] + ai_messages
        thread_store.save_messages(thread_id, all_messages)
        print(f"[AGENT] Saved {len(all_messages)} total messages to store")
    else:
        print(f"[AGENT] No messages in result: {result}")
    
    return result

def chat_streaming_handler(thread_id : str, message : str) -> Iterator[str]:
    """
    Streaming chat handler that saves messages as they complete
    """
    from langchain_core.messages import AIMessage
    
    # Get existing messages
    existing_messages = thread_store.get_messages(thread_id)
    print(f"\n[STREAM] ===== Starting chat_streaming_handler for thread {thread_id} =====")
    print(f"[STREAM] Existing messages: {len(existing_messages)}")
    
    # Create human message
    human_msg = HumanMessage(content=message)
    input_messages = existing_messages + [human_msg]
    
    graph = create_chat_agent_graph()
    full_response = ""

    # Stream the response
    for chunk, metadata in graph.stream(
        input={'messages': input_messages},
        config={'configurable': {'thread_id': thread_id}},
        stream_mode='messages'
    ):
        chunk_text = chunk.content if hasattr(chunk, 'content') else str(chunk)
        full_response += chunk_text
        yield chunk_text
    
    # After streaming completes, save the full conversation
    if full_response:
        ai_msg = AIMessage(content=full_response)
        final_messages = existing_messages + [human_msg, ai_msg]
        thread_store.save_messages(thread_id, final_messages)
        print(f"[STREAM] Saved {len(final_messages)} total messages to store")
    else:
        print(f"[STREAM] No response generated")



def get_all_threads_handler() ->list[str | None]:
    """
    Docstring for get_all_threads_handler

    """
    # Return threads from memory store
    return thread_store.get_all_threads()

def chat_history_handler(thread_id: str) -> dict:
    """
    Docstring for chat_history_handler
    """
    messages = thread_store.get_messages(thread_id)
    print(f"[HISTORY] Thread {thread_id}: Retrieved {len(messages)} messages from store")
    converted_messages = [convert_message_to_dict(msg) for msg in messages]
    print(f"[HISTORY] Thread {thread_id}: Converted to {len(converted_messages)} dicts")
    result = {'messages': converted_messages}
    print(f"[HISTORY] Returning: {result}")
    return result