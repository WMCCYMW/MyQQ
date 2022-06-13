import queue

# 队列可以实现自加锁比较好用

mq = queue.Queue(maxsize=20)
