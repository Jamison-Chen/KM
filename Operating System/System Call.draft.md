System call 簡稱 syscall，是 **user program** 用來與 [OS kernel](</Operating System/Kernel.draft.md>) 溝通的方式，當 user program 需要較高的系統權限進行一些操作（比如存取硬體資源）時，就須要透過 system call 來操控 OS kernel，再由 OS kernel 來進行想要的操作。

>[!Info] User Program?
>OS 會將 [virtual memory](</Operating System/Memory Management.draft.md#Virtual Memory>) 切分成管制較鬆的 **user space** 與被嚴格保護的 **kernel space**，這麼做可以提升系統的安全性。
>
>Kernel space 只會被用來運行 OS kernel、kernel extensions 以及 device drivers；user space 則用來運行其它各種程式 (program)，因此一般的 program 又會被稱為 user program。

# System Call 的運作流程

```mermaid
flowchart LR
    id1(Invocation) --> id2(Mode Switch)
    id2 --> id3(Execution)
    id3 --> id4(Return)
```

- **Invocation**: User program 透過 ==OS 提供的 API (OS-level API)== 發出 system call 給 OS kernel
- **Mode Switch**: CPU 從 **User Mode** 切換為 **Kernel Mode**（詳見 [Protection Ring](</Operating System/Memory Management.draft.md#Protection Ring>)）
- **Execution**: Kernel 執行 system call
- **Return**: 控制權交還給 user program，CPU 切換回 user mode

### OS-Level API

OS-level APIs 通常是 C library 的一部份，或者倒過來說：C library 中有一些 functions 屬於 OS-level 的 API。比如 `execve` 這個 C library function 就是一個會進一步觸發 `exec` system call 的 OS-level API。

>[!Note]
>當我們使用 Shell 的 `exec`、`exit`、`kill` 等指令時，Shell 是幫我們呼叫 OS-level APIs，並不是直接發出 system call。

# System Call 的種類

|Type|Description|Related Calls|
|---|---|---|
|**Process Control**|-|`fork`, `exec`, `wait`, `exit`, `kill`, ...|
|**File Management**|-|`open`, `read`, `write`, `close`, ...|
|**Device Management**|-|`ioctl`, ...|
|**Information Maintenance**|取得或設定系統參數|`getpid`, `settimeofday`, ...|
|**Communication**|用於 [IPC](</Operating System/Unix Signal & IPC.md>)|`pipe`, `socket`, ...|
|**Protection**|取得或設定檔案的存取權限|-|

# 參考資料

- <https://en.wikipedia.org/wiki/System_call>
- <https://en.wikipedia.org/wiki/User_space_and_kernel_space>
- [從零開始的開源地下城 - System Call](https://hackmd.io/@combo-tw/BJPoAcqQS)
