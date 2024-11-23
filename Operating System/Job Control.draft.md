# What is a Job?

- Job 是由 Shell 管理的 process 或 **process group**。
    - 一個 job 可以由一個 process 或多個 processes 組成。
- 不同 Shell sessions 間無法知道彼此管理哪些 jobs。
- Shell session 會分配 unique job ID 每個給自己所管理的 job

### Job vs. Process

- 一個 job 可能由一個或多個 processes 組成。
- Job 是由 Shell 管理的，不同 Shell sessions 間無法知道彼此管理哪些 jobs；process 則是由 OS 管理的。

### 列出所有當前 Shell 所管理的 Job

```bash
jobs
```

Example output:

```plaintext
```

**Options**

#TODO 

# Unix Signal (IPC)

>**Signals** are standardized messages sent to a running program to trigger specific behavior, such as quitting or error handling.

Signal 是 asynchronous 的，當 signal 送出至指定的 process 後，OS 會中斷該 process，但==大部分 signals 並無法馬上中斷 process，而是須等到 process 執行完當前正在執行的 atomic instruction 後才會中斷==。

### 常見的 Signal

|Signal|Meaning|Action|Keyboard Shortcut|
|:-:|---|---|:-:|
|`SIGINT`|Interrupt|平緩地中斷目前 terminal 前景所運行的 job|`Ctrl` + `C`|
|`SIGTERM`|Terminate|效果同 SIGINT，但可以透過其他 process 發出，來終止另一個 process/job|無|
|`SIGTSTP`|Terminal Stop|暫停目前 terminal 前景所運行的 job|`Ctrl` + `Z`|
|`SIGQUIT`|Quit|平緩地中斷目前 terminal 前景所運行的 job，並進行 core dump|`Ctrl` + `\`|
|`SIGKILL`|Kill|立即強制終止目前 terminal 前景所運行的 job|無|

>[!Note]
>所謂一個 job「在前景運行」，指的是該 job 佔用著 terminal 且會接收來自 terminal 的 standard input；而「在背景運行」就是沒用佔用 terminal 也不會接收來自 terminal 的 standard input。

- **SIGINT & SIGTERM**

    #TODO 

- **SIGTSTP**

    `SIGTSTP` 會暫停目前 terminal 前景所運行的 job，使這個 job 進入 "suspended" 的狀態，並將它==丟到 background==，此時使用者就可以拿回 terminal 的控制權。

    須注意的是，suspended 狀態下的 job 並不是完全終止，只是被暫停。

    可以使用指令 `fg [{JOB_ID}]` 把指定的 job 從 background 拉回 foreground。

- **SIGKILL**



# 參考資料

- <https://en.wikipedia.org/wiki/Signal_(IPC)>
