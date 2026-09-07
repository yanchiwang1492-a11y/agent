from memory.save.window_memory import WindowMemory

class PromptBuilder:
     def __init__(self,session_id):
         self.window_memory = WindowMemory(session_id)
     #构建提示词
     def builder_prompt(self):
         prompt ="""
           一: 角色：你是一个记忆提取助手
           二: 任务：
                  - 理解用户需求
                  - 根据用户问题，提取相关记忆
         """
         #查询窗口记忆
         window_memory = self.window_memory.query()
         prompt += "短期记忆-窗口记忆"
         for i in window_memory:
             if i["role"]=="user":
                prompt+=f"用户提问：{i['content']}"
             else:
                prompt += f"AI回答：{i['content']}"
         return prompt