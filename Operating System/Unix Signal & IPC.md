# Unix Signal

>Signals are standardized messages sent to a running program to trigger specific behavior, such as quitting or error handling.

Unix signal 是 process 與 process 溝通的方式，主要功能是用來中斷 (interrupt) 運行中的 process，屬於 **IPC (inter-process communication)** 的一部份。

### 常見的 Signals

|Signal|Number|Action|Description|Keyboard Shortcut|
|:-:|:-:|---|---|:-:|
|`SIGHUP`|1|Terminate|Shell 被關閉時會發出這個 signal 給所有它管理的 jobs，平緩地中斷它們|無|
|`SIGINT`|2|Terminate|平緩地中斷目前 terminal 前景所運行的 job|`Ctrl` + `C`|
|`SIGQUIT`|3|Terminate + Core Dump|平緩地中斷目前 terminal 前景所運行的 job，並進行 core dump|`Ctrl` + `\`|
|`SIGKILL`|9|Terminate|==立即強制終止==目前 terminal 前景所運行的 job，==`SIGKILL` 無法被 catch 或 ignore==|無|
|`SIGTERM`|15|Terminate|效果同 `SIGINT`，但可以透過其他 process 發出，來終止另一個 job|無|
|`SIGTSTP`|20|Stop|==暫停==目前 terminal 前景所運行的 job，並將其丟到背景|`Ctrl` + `Z`|

### Signal Handling

==Signal is asynchronous==，當 signal 被送至指定的 process 後，process 會 handle signal，但大部分 signals 都不會馬上被 handle（`SIGKILL` 除外），process 會等到執行完當前正在執行的 **atomic instruction** 後才會 handle signal。

也因為 signal 是 asynchronous 的，所以有可能發生 race condition，也就是當 process 正在 handle 一個先來的 signal 時，另一個後到的 signal 也可以被 handle 且有可能先執行完。

Process handle signal 的方式有三種：

1. Default action：根據 signal 採取預設行為（即 terminate、core dump、stop 等）
2. Ignore：==`SIGKILL` 無法被 ignore==
3. Catch：客製化處理方式，不採取預設行為，==`SIGKILL` 無法被 catch==

# IPC

IPC 是 **inter-process communication** 的縮寫，泛指各種可以讓 process 間相互溝通的技術，常見用來實現 IPC 的方式包括以下幾種：

|Method|Description|
|---|---|
|File|將要溝通的訊息以檔案的型式存在 disk，這個檔案可以被多個 processes 存取|
|Signal|-|
|[[Socket & Port#Socket\|Socket]]|透過 network interface 傳遞訊息，可再細分為 Internet domain socket 和 Unix domain socket|
|[[Message-Queuing System\|Message Queue]]|-|
|[[3 - Operators\|Pipe]]|-|
|Shared Memory|一塊可以被多個 processes 存取的 memory|

# 參考資料

- <https://en.wikipedia.org/wiki/Job_control_(Unix)>
- <https://en.wikipedia.org/wiki/Signal_(IPC)>
- <https://faculty.cs.niu.edu/~hutchins/csci480/signals.htm>
- <https://en.wikipedia.org/wiki/Inter-process_communication>
