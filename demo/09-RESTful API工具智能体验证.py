from model import my_model
from model.my_model import MyModel
from tool.amap_driver_tool import driver_tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
#演示智能体创建

def create_email_agent(q):
    model = MyModel.get_local_model()
    tools=[driver_tool]
    prompt = """
       一 角色:  你是一个路径规划助手
       二 任务： 请根据用户输入问题，完成汽车路线规则
       三 规则：
              - 根据工具返回的结果，生成详细的汽车路线
    """
    agent =create_agent(
        model =model,
        tools =tools,
        system_prompt=prompt,
        debug=True
    )

    human_msg = {"messages": [HumanMessage(content=q)]}
    rs = agent.invoke(human_msg)
    print(rs["messages"][-1].content)

if __name__ =="__main__":
    q="请给767920412@qq.com 发送一封邮件，通知他来上课"
    q1="开车从成都到绵阳怎么走"
    create_email_agent(q1)