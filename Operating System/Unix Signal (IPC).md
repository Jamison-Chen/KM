>**Signals** are standardized messages sent to a running program to trigger specific behavior, such as quitting or error handling.

Signal 是 asynchronous 的，當 signal 送出至指定的 process 後，OS 會中斷該 process，但大部分 signals 並無法馬上中斷 process，而是須等到 process 執行完當前正在執行的 atomic instruction 後才會中斷。

# 常見的 Signal

|Signal|Meaning|Action|Keyboard Shortcut|
|:-:|:-:|:-:|:-:|
|**SIGINT**|Interrupt|平緩地中斷|`Control` + `c`|
|**SIGTERM**|Terminate|效果同 SIGINT||
|**SIGQUIT**|Quit|平緩地中斷並進行 core dump|`Control` + `\`|
|**SIGKILL**|Kill|立即強制終止||

# 參考資料

- <https://en.wikipedia.org/wiki/Signal_(IPC)>
