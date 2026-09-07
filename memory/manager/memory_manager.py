from memory.retrieval.SummaryAgent import SummaryAgent
from memory.manager.session_mananger import SessionManager

"""
记忆管理器，管理记忆的更新
"""
class MemoryManager:

   def __init__(self,sessionManger:SessionManager):
       #摘要智能体
       self.summary_agent = SummaryAgent(sessionManger.summary_memory)
       #获取窗口记忆对象
       self.window_memory = sessionManger.window_memory

   def update(self):
       #获取查询的窗口记忆
       query_window = self.window_memory.query()
       if len(self.window_memory.query()) >=2:
           self.summary_agent.update(query_window)