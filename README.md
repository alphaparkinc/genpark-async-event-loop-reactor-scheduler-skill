# genpark-async-event-loop-reactor-scheduler-skill

Agent Skill implementing a **Cooperative Asynchronous Event Loop & Reactor Scheduler** with dual queues (ready microtask deque + min-heap timer priority queue), Futures, and completion callbacks.

## Architectural Overview
```mermaid
flowchart TD
    Submit["Submit Task / Timer"] --> Queue{"Is Delayed Timer?"}
    Queue -- Yes --> Heap["Min-Heap Timer Queue (timestamp, id, callback)"]
    Queue -- No --> Ready["Ready Microtask Deque (FIFO)"]
    Heap --> TimerCheck{"Timer Expired?"}
    TimerCheck -- Yes --> Ready
    Ready --> Loop["Event Loop Dispatcher"]
    Loop --> Callback["Execute Callback Function"]
    Callback --> Future["Resolve Future / Set Result"]
```
