import sys
import json
from client import MiniEventLoop

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-async-event-loop-reactor-scheduler-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "schedule_async_tasks",
                        "description": "Execute a chain of asynchronous microtasks and timers via MiniEventLoop",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_names": {"type": "array", "items": {"type": "string"}},
                                "delays_ms": {"type": "array", "items": {"type": "number"}}
                            },
                            "required": ["task_names"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "schedule_async_tasks":
            names = args.get("task_names", ["TaskA", "TaskB"])
            delays = args.get("delays_ms", [5.0, 5.0])
            loop = MiniEventLoop()
            fut = loop.Future()
            trace = []
            
            def run_chain(idx=0):
                if idx < len(names):
                    trace.append(f"Exec: {names[idx]}")
                    delay_s = (delays[idx] if idx < len(delays) else 1.0) / 1000.0
                    loop.call_later(delay_s, run_chain, idx + 1)
                else:
                    fut.set_result(trace)
                    
            loop.call_soon(run_chain, 0)
            res = loop.run_until_complete(fut)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"trace": res, "tasks_completed": len(res)})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
