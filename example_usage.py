from client import MiniEventLoop

loop = MiniEventLoop()
fut = loop.Future()
log = []

def step1():
    log.append("Started Step 1")
    loop.call_later(0.01, step2)

def step2():
    log.append("Completed Step 2")
    fut.set_result(log)

loop.call_soon(step1)
res = loop.run_until_complete(fut)
print("Event Loop Execution Trace:", res)
