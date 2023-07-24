import threading
import time

ct = threading.current_thread()
print(ct.name, threading.get_ident())


def worker(a, b):
    thread = threading.current_thread()
    print(thread.name, threading.get_ident())
    print(f"a is {a}, b is {b}")  # a is 1, b is 2


new_ct = threading.Thread(target=worker, args=[1, 2])
new_ct.start()
new_ct.join()
