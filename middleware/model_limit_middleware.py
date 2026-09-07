from langchain.agents.middleware import before_model, AgentState, after_model

from langgraph.runtime import  Runtime
import re
from langchain_core.messages import AIMessage
import redis

#链接redis服务
client = redis.StrictRedis(host='localhost', port=6379, db=0, password='root')



@before_model
def model_limit_before_middleware(state:AgentState,time:Runtime):
    print('5555555555555',time)
    user_id = time.execution_info.thread_id
    print(f"用户id:{user_id}")
    num =2
    #自定义键名
    # key = f"limit:{user_id}"
    key = user_id
    #获取值
    data = client.get(key)
    print('11111111111111111111',data)
    if data is None:
      return {}
    else:
      data = int(data.decode())
      if data >= num:
          raise ValueError("'###############,'用户模型使用次数超过限制")
@after_model
def model_limit_after_middleware(state: AgentState, time: Runtime):
    user_id = time.execution_info.thread_id
    print(f"用户id:{user_id}")
    #自定义键名
    # key = f"limit:{user_id}"
    key = user_id
    #设置自增,相当于i++
    client.incr(key, 1)
    data = client.get(key)
    data = int(data.decode())
    if data == 1:
    #设置失效时间,单位是秒，2分钟
        client.expire(key, 120)
    print(f"(&&&&&&&&&&&&&&&&&&&用户{user_id}模型使用次数增加1")
    return {}