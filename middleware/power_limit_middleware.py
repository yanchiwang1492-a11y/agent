from langchain.agents.middleware import before_agent,AgentState,after_agent
from tool.mysql_tool import mysql_tool
from langgraph.runtime import  Runtime
import ast
from langchain_core.messages import AIMessage
import redis

#链接redis服务
client = redis.StrictRedis(host='localhost', port=6379, db=0, password='root')
# 权限校验
@before_agent
def power_limit_middleware(state:AgentState,time:Runtime):
    # 用户id
    user_id = time.execution_info.thread_id
    #演示案例，在数据库里查询
    rs = mysql_tool.invoke({
        "sql":f"select department from user_info where user_id = '{user_id}'"
    })
    #类型转换
    data = ast.literal_eval(rs)
    #获取部门
    d = data[0][0]
    #假如这个智能体允许事业部访问
    if d != "事业部":
        raise Exception("您没有权限访问")
    # return {'你有权限哦！！！'}
    return {}


# 统计 token消耗
@after_agent
def count_token_middleware(state:AgentState,time:Runtime):
    print(state["messages"])
    msg = state["messages"]
    input_token =0
    output_token = 0
    total_token = 0
    if msg[1].usage_metadata :
        input_token += msg[1].usage_metadata["input_tokens"]
        output_token += msg[1].usage_metadata["output_tokens"]
        total_token += msg[1].usage_metadata["total_tokens"]
        return {
            "messages":[AIMessage(content=f"输入token:{input_token}，输出token:{output_token}，总token:{total_token}")]
        }
    return {}


# 统计 token消耗
@after_agent
def count_token_redis_middleware(state: AgentState, time: Runtime):
    print(state)
    print(state["messages"])
    # 用户id
    user_id = time.execution_info.thread_id
    key = f"countToken:{user_id}"
    #获取键名的值
    v = client.hgetall(key)
    msg = state["messages"]
    if not v:
        print('开始折腾Redis')
        input_tokens=0
        output_tokens=0
        total_tokens=0
        client.hset(key,"input_tokens",input_tokens)
        client.hset(key, "output_tokens", output_tokens)
        client.hset(key, "total_tokens", total_tokens)
    else:
        print("开始取值")
        input_tokens = client.hget(key, "input_tokens").decode()
        print(f"获取redis的输入token:{input_tokens}")
        print(f"获取redis的输出token:{type(input_tokens)}")
        output_tokens = client.hget(key, "output_tokens").decode()
        total_tokens = client.hget(key, "total_tokens").decode()

    if msg[1].usage_metadata:
        print(f"=={type(msg[1].usage_metadata["input_tokens"])}")
        input_token01 = msg[1].usage_metadata["input_tokens"]+int(input_tokens)
        output_token01 = msg[1].usage_metadata["output_tokens"]+int(output_tokens)
        total_token01 = msg[1].usage_metadata["total_tokens"]+int(total_tokens)
        #存入redis
        client.hset(key, "input_tokens", input_token01)
        client.hset(key, "output_tokens", output_token01)
        client.hset(key, "total_tokens", total_token01)

        return {
            "messages": [AIMessage(content=f"输入token:{input_token01}，输出token:{output_token01}，总token:{total_token01}")]
        }
    return {}