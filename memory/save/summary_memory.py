from psycopg_pool import ConnectionPool

#配置连接池
pool = ConnectionPool(
    conninfo="host=127.0.0.1 port=5432 dbname=postgres user=postgres password=1",
    max_size=20,#最大连接数，生成环境是20个
    min_size=10,#最小连接数，生成环境是10个
)
class SummaryMemory:

    def __init__(self,session_id:str):
        self.session_id = session_id
    #保存
    def save(self,summary:str):
        with pool.connection() as con:
            with con.cursor() as cur:
                sql =(f"INSERT INTO conversation_summary(session_id, summary) "
                      f"VALUES('{self.session_id}','{summary}') "
                      f"ON CONFLICT(session_id) DO UPDATE SET summary=EXCLUDED.summary,update_time=NOW()")
                # sql = (f"INSERT INTO conversation_summary(session_id, summary) VALUES('{self.session_id}','{summary}') ")
                cur.execute(sql)
                #提交事务

                con.commit()
    #查询
    def query(self):
        with pool.connection() as con:
            with con.cursor() as cur:
                sql = f"select summary from conversation_summary where session_id ='{self.session_id}'"
                cur.execute(sql)
                #查询单个值
                rs = cur.fetchone()
                # rs = cur.fetchall()

                if rs:
                    return rs[0]
                    # return rs[0][0]
                else:
                    return ""
if __name__ =="__main__":
    s = SummaryMemory("002")
    print(s.query())
    s.save('我眼睛好干111111111111！')