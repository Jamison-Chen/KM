Program 被存在 disk 裡，而 process 是被放在 memory 中執行的 program。

一個 OS 中的每個 process 都會有一個唯一的 PID。

# Process 的結構

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/process-structure.png>)

一個 process 在 memory 中包括以下幾個區塊（按順序）：

|Section|Description|Size|
|---|---|---|
|Text|程式的 machine code instructions|固定|
|Data|放 global variables 與 static attributes|固定|
|Heap|在程式的 run time 期間動態分配|不固定|
|Stack|放一些暫時的資料，比如 local variables、傳進 function 的參數、function 的 return address 等|不固定|

# Process States

下圖為 process 的 FSM diagram：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/process-state-fsm.png>)

# Thread

- Process 是 thread 的容器：

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/process-and-thread.jpg>)

- 各個 process 間是互相獨立的（有自己的 virtual memory space）；但同一個 process 中的多個 threads 是共享同一個 virtual memory space，也共享其所屬 process 被分配到的 CPU time
- 進行 multi-thread programming 時，若多個 threads 若同時存取同一個全域變數，可能導致 **Synchronization Problem**
- 若 threads 間互搶資源，可能產生 [Deadlocks](</Operating System/Deadlocks.md>) 或 freezing

### Thread Pooling

Thread pooling 是一種系統設計的 design pattern，由於建立 thread 與消滅 thread 對 OS 來說都是相對昂貴（耗時）的操作，所以 thread pooling 的做法是預先建立好一定數量的 threads，等待著 task 進來，執行完 task 後 thread 也不會被消滅，而是會繼續在 pool 裡等著執行下一個被分配到的 task。

# Child Process

- Zombie process

#TODO 

# Process Group

- 一個 process group 由一到多個 processes 組成。
- 每個 process group 會有自己的 PGID。
- Child process 與 parent process 並不會擁有相同的 PGID。

# Context Switch

#TODO 

# Multiprogramming OS

Multiprogramming OS（又叫做 multitasking OS）可以同時執行多個 processes，然而若使用的硬體是單核 CPU (single-core processor)，那同一時間點下還是只能執行一個 process，因此 multitasking OS 通常會搭載多核 CPU (**multi-core processor**)

# 延伸閱讀

- [與 Process 相關的指令](</Operating System/Shell/8 - 與 Process 相關的指令.md>)
- [Job Control](</Operating System/Job Control.md>)
- [CPU Scheduling](</Operating System/CPU Scheduling.draft.md>)

# 參考資料

- <https://en.wikipedia.org/wiki/Process_(computing)>
- <https://en.wikipedia.org/wiki/Child_process>
- <https://en.wikipedia.org/wiki/Process_group>
- <https://en.wikipedia.org/wiki/Process_management_(computing)>
- <https://www.geeksforgeeks.org/introduction-of-process-management/>
- <https://en.wikipedia.org/wiki/Thread_(computing)>
- <https://en.wikipedia.org/wiki/Thread_pool>
