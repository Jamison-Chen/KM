# Process

-   Process 即執行中的 program
-   每一個 process 是互相獨立的（不共享 CPU time、RAM 等資源）
-   多個 processes 間的溝通，只能透過由 OS 提供的 **inter-process communication**
-   **Multitasking OS** 可以同時執行多個 processes，然而若使用的硬體是單核 CPU (single-core processor)，一次也只能執行一個 process，因此 multitasking OS 通常會搭載多核 CPU (**multi-core processor**)
-   Process 會佔用 RAM，因此如何排程 ([CPU scheduling](</Operating System/CPU Scheduling.draft.md>))，以及如何有效管理 RAM 是 OS 須關注的事

# Thread

- 一個 process 由多個 threads 組成，一個 thread 負責一項功能

    以聊天室 process 為例，可以同時接受對方傳來的訊息以及發送自己的訊息給對方，就是同個 process 中不同 threads 的功勞。

    ![[process-and-thread.jpg]]

-   同一個 process 底下的 threads 共享資源，如 RAM、CPU time 等，不同的 processes 間則否
-   進行 multi-threading 時，若多個 threads 若同時存取同一個全域變數，可能導致 **Synchronization Problem**
- 若 threads 間互搶資源，可能產生 [Deadlocks](</Operating System/Deadlocks.md>) 或 freezing
