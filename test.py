async test():  # 1个用法 新*
    print("开始")
    yield "你好"
    print("结束")

if __name__ == "__main__":
    # gen = test()
    # print(next(gen))
    # print(next(gen))

    a = test()
    async for b in a:
        print(b)