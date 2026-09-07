from tool.send_email_tool import send_email_tool
from tool.add_tool import add_tool
from model.my_model import MyModel
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware

model = MyModel.get_model()
tools = [send_email_tool, add_tool]
prompt = """
   一 角色:  你是一个聊天助手
"""
# 定义摘要提示词
summary_prompt = """
任务：请根据下面提供的历史对话生成摘要。

历史对话：
{messages}

规则：
只保留用户本人姓名。

输出：
用户画像: xxx
"""

#定义摘要中间件配置
sumary = SummarizationMiddleware(
     model=model,
     # trigger=("tokens",10), #档token达到10个触发摘要，生成环境建议3000

    trigger=[
        {"tokens": 10, "messages": 1},   # 条件组1
        {"tokens": 3000, "messages": 50},   # 条件组2
    ],
    keep=("messages",2), #保留最近1轮的对话，生成环境建议保留20以上
    summary_prompt = summary_prompt, #可选
    # trim_tokens_to_summarize = 4000,
    # 可选，摘要总结的摘要信息限制在4000token
)

memory = InMemorySaver()

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt,
    checkpointer=memory,
    middleware=[sumary]
)

def print_memory(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    state = agent.get_state(config)
    messages = state.values.get("messages", [])
    print("\n================ 当前记忆状态 ================")
    print("消息数量：", len(messages))
    for i, message in enumerate(messages):
        print(f"\n--- Message {i + 1} ---")
        print("类型：", type(message))
        print("类型：", type(message).__name__)
        # 只打印前500个字符，避免输出太长
        content = str(message.content)
        print("内容：")
        print(content[:500])
    print("==============================================\n")
#演示智能体创建
def create_email_agent(q,user_id):


    #human_msg = {"messages":[{"role":"user","content":q}]}
    human_msg = {"messages": [HumanMessage(content=q)]}
    config = {"configurable":{"thread_id":user_id}}
    rs = agent.invoke(human_msg,config)
    return rs["messages"][-1].content

if __name__ =="__main__":

    q_list = [
        "1+1等于多少？",
        "用户的名字叫张三，我是一名Java程序员。",
        '我的第一个问题是啥？'
        # "我今年23岁，目前正在学习LangChain和LangGraph。",
        # "10+20等于多少？",
        # "我的第一个问题是什么？",  # 测试记忆保留
        # "我是谁？多少岁了，目前在学习什么"
    ]
    for i in range(len(q_list)):
        print(f"第{i+1}个问题:{q_list[i]}")
        rs =create_email_agent(q_list[i],1)
        print(f"第{i + 1}个的答案:{rs}")
    print("=============打印当前记忆信息=====================")
    print_memory(1)