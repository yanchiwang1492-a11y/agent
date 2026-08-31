def test02():
    print("开始")
    yield "你好"
    print("结束")


if __name__=="__main__":
    # for c in test02():
    #     print(f"返回值是:{c}")
    rs = test02()
    print(f"生成器{rs}")
    g = next(rs)
    print(f"返回值是:{g}")
    d =next(rs)
    print(d)
