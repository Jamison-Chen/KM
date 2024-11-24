# Job Control

### What is a Job?

- Job 是由 Shell 管理的 process 或 **process group**。
    - 一個 job 可以由一個 process 或多個 processes 組成。
- 不同 Shell sessions 間無法知道彼此管理哪些 jobs。
- Shell session 會分配 unique job ID 每個給自己所管理的 job
- Job 是由 Shell 管理的，不同 Shell sessions 間無法知道彼此管理哪些 jobs；process 則是由 OS 管理的。

### 列出所有當前 Shell 所管理的 Jobs

```bash
jobs
```

Example output:

```plaintext
[1]  - suspended  python -m http.server 8000
[2]  + running    nc -l localhost 3000
```

- 輸出的內容包含 job id、job status 與當初觸發 job 的指令。
- 只能列出「當前 Shell 所管理」的 jobs

**常用的 Options**

|Option|Description|
|:-:|---|
|`-l`|額外列出 job 的 pid|
|`-r`|只列出 status 為 running 的 jobs|
|`-s`|只列出 status 為 suspended 的 jobs|

### Job Status

- Running
- Suspended
- Queued
- Exit

### 讓背景的 Suspended Job 在背景繼續運作

```bash
bg %{JOB_ID}
```

- 記得 job id 前有 `%`
- 此時指定的 job status 會從 suspended 變成 running。

### 把背景的 Job 拉回前景

```bash
fg [%{JOB_ID}]
```

- 記得 job id 前有 `%`
- 如果背景目前只有一個 job，則可以不用寫 `{JOB_ID}`。
- 若指定的 job 的 status 原本是 suspended，那拉到前景後 status 就會變成 running。

>[!Note]
>所謂一個 job「在前景運行」，指的是該 job 佔用著 terminal 且會接收來自 terminal 的 standard input；而「在背景運行」就是沒用佔用 terminal 也不會接收來自 terminal 的 standard input。

# Unix Signal (IPC)

>**Signals** are standardized messages sent to a running program to trigger specific behavior, such as quitting or error handling.

Unix signal 是 process 與 process 間溝通的方式，因此又叫做 **inter-process communication (IPC)**。

Signal 是 asynchronous 的，當 signal 送出至指定的 process 後，OS 會中斷該 process，但==大部分 signals 並無法馬上中斷 process，而是須等到 process 執行完當前正在執行的 atomic instruction 後才會中斷==。

**常見的 Signals**

|Signal|Number|Action|Description|Keyboard Shortcut|
|:-:|:-:|---|---|:-:|
|`SIGINT`|2|Terminate|平緩地中斷目前 terminal 前景所運行的 job|`Ctrl` + `C`|
|`SIGQUIT`|3|Terminate + Core Dump|平緩地中斷目前 terminal 前景所運行的 job，並進行 core dump|`Ctrl` + `\`|
|`SIGKILL`|9|Terminate|立即強制終止目前 terminal 前景所運行的 job|無|
|`SIGTERM`|15|Terminate|效果同 SIGINT，但可以透過其他 process 發出，來終止另一個 process/job|無|
|`SIGTSTP`|20|Stop|暫停目前 terminal 前景所運行的 job|`Ctrl` + `Z`|

- **SIGINT & SIGTERM**

    #TODO 

- **SIGTSTP**

    `SIGTSTP` 會「暫停」（不是完全終止）目前 terminal 前景所運行的 job，==使這個 job 進入 suspended 狀態，並將它丟到背景==，此時使用者就可以拿回 terminal 的控制權。

    可以使用指令 `fg [{JOB_ID}]` 把指定的 job 從 background 拉回 foreground。

    可以使用指令 `jobs` 查看當前的 Shell session 中的所有 jobs。

- **SIGKILL**

# Thread

### Thread vs. Process

- Process 是放在 memory 中執行的 program
    - 因為 process 會佔用 memory，因此如何排程 ([CPU scheduling](</Operating System/CPU Scheduling.draft.md>))，以及如何有效管理 memory 是 OS 須關注的事
- 各個 process 間是互相獨立的（有自己的 virtual memory space）；但同一個 process 中的多個 threads 是共享同一個 virtual memory space，也共享其所屬 process 被分配到的 CPU time
- **Multitasking OS** 可以同時執行多個 processes，然而若使用的硬體是單核 CPU (single-core processor)，那同一時間點下還是只能執行一個 process，因此 multitasking OS 通常會搭載多核 CPU (**multi-core processor**)
- Process 是 thread 的容器：

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/process-and-thread.jpg>)

- 進行 multi-thread programming 時，若多個 threads 若同時存取同一個全域變數，可能導致 **Synchronization Problem**
- 若 threads 間互搶資源，可能產生 [Deadlocks](</Operating System/Deadlocks.md>) 或 freezing

### Thread Pooling

Thread pooling 是一種系統設計的 design pattern，

#TODO 

# 延伸閱讀

- [與 Process 相關的指令](</Operating System/Shell/8 - 與 Process 相關的指令.md>)

# 參考資料

- <https://en.wikipedia.org/wiki/Signal_(IPC)>
- <https://en.wikipedia.org/wiki/Process_(computing)>
- <https://en.wikipedia.org/wiki/Process_management_(computing)>
- <https://en.wikipedia.org/wiki/Thread_(computing)>
