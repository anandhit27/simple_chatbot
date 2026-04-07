from typing import Optional, Dict, List
from langchain_core.messages import BaseMessage

class ThreadMemoryStore:
    """In-memory store for thread conversations"""
    
    def __init__(self):
        self.threads: Dict[str, List[BaseMessage]] = {}
    
    def save_messages(self, thread_id: str, messages: List[BaseMessage]):
        """Save messages for a thread"""
        self.threads[thread_id] = messages
        print(f"[STORE] Saved {len(messages)} messages for thread {thread_id}")
        print(f"[STORE] Threads in store: {list(self.threads.keys())}")
    
    def get_messages(self, thread_id: str) -> List[BaseMessage]:
        """Get messages for a thread"""
        messages = self.threads.get(thread_id, [])
        print(f"[STORE] Retrieved {len(messages)} messages for thread {thread_id}")
        return messages
    
    def add_message(self, thread_id: str, message: BaseMessage):
        """Add a single message to a thread"""
        if thread_id not in self.threads:
            self.threads[thread_id] = []
        self.threads[thread_id].append(message)
    
    def get_all_threads(self) -> List[str]:
        """Get all thread IDs"""
        return list(self.threads.keys())
    
    def thread_exists(self, thread_id: str) -> bool:
        """Check if a thread exists"""
        return thread_id in self.threads
    
    def clear_thread(self, thread_id: str):
        """Clear a specific thread"""
        if thread_id in self.threads:
            del self.threads[thread_id]


# Global instance
thread_store = ThreadMemoryStore()
