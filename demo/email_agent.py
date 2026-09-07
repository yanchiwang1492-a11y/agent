from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

class EmailAgent:

    def __init__(self):
        self.model = MyModel.get_model()
        self.tools = self.get_tool()
        self.prompt = self.get_prompt()
        self.agent = self.get_agent()
    def get_tool(self):

        self.tools = [send_email_tool]
        return self.tools

    def get_prompt(self):
        self.prompt="""
            角色，你是一个邮件发送助手
        """
        return self.prompt

    def get_agent(self):
        self.agent = create_agent(
            model = self.model,
            tools = self.tools,
            system_prompt=self.prompt
        )
        return self.agent
    #异步流式问答
    async def get_astream(self,question:str,user_id:int):
        human_msg = {"messages": [HumanMessage(content=question)]}
        config = {"configurable": {"thread_id": user_id}}
        async for event in self.agent.astream_events(human_msg, config,version="v2"):
            # 获取事件内容
            event_name = event["event"]
            if event_name == "on_chain_start":
                yield f"\n邮件智能体开始运行\n"
            elif event_name == "on_chat_model_start":
                yield f"\n大模型开始思考\n"
            elif event_name == "on_chat_model_end":
                yield f"\n大模型思考结束\n"
            elif event_name == "on_chain_stream":
                yield f"\n大模型开始生成答案\n"
            elif event_name == "on_tool_start":
                # 获取工具名称
                tool_name = event["name"]
                if tool_name == "send_email_tool":
                    yield f"\n开始发送邮件\n"
            elif event_name == "on_tool_end":
                # 获取工具返回值
                tool_output = event["data"]["output"].content
                yield f"\n邮件工具执行完毕，返回值为：{tool_output}\n"
            elif event_name == "on_chat_model_stream":
                data = event["data"]["chunk"].content
                if data:
                    yield data

if __name__ =="__main__":
    agent = EmailAgent()