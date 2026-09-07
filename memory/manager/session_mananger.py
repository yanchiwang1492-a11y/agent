from memory.save.window_memory import WindowMemory
from memory.manager.prompt_builder import PromptBuilder
from langchain_core.messages import SystemMessage
from memory.save.summary_memory import SummaryMemory
"""
 会话管理器:主要负责四层记忆的对象创建和提示词的生成
"""
class SessionManager:

     def __init__(self,session_id:str):
         self.window_memory = WindowMemory(session_id)
         self.session_id = session_id
         self.prompt_builder = PromptBuilder(self.session_id)
         self.summary_memory = SummaryMemory(self.session_id)
         # self.agent = SummaryAgent(elf.summary_memory )
     #添加窗口记忆
     def save(self,role:str,content:str):
         self.window_memory.save(role,content)
     #构建提示词
     def build_prompt(self):
         prompt = self.prompt_builder.builder_prompt()
         return {"role":"system","content":prompt}
