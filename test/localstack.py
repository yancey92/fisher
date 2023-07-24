import threading

from werkzeug.local import LocalStack

# 创建线程本地栈对象
local_stack = LocalStack()


# 在每个线程中操作线程本地栈
def worker():
    local_stack.push(1)
    print(local_stack.top)
    local_stack.pop()
    print(id(local_stack))


# 创建多个线程并运行
threads = []
for _ in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# 等待所有线程执行完毕
for t in threads:
    t.join()
