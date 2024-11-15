#Command

# 擷取快照

```bash
ps [{OPTIONS}]
```

`ps` 是 process status 的縮寫。

### Options

- `-a`：顯示由所有使用者觸發的所有執行中的 processes，但不包含沒有 terminal 可以控制的 processes
- `-x`：無論有沒有 terminal 可以控制的 processes 都顯示
- `-A`：等同 `-ax`，也就是顯示由所有使用者所觸發的所有執行中的 processes，且包含沒有 terminal 可以控制的

### 完整顯視所有執行中的 Processes

```bash
ps aux
```

`ps aux` 比 `ps -A` 或 `ps -ax` 顯示的資訊更完整。

### 只顯示部分欄位

e.g. 只顯示 pid 與指令

```bash
ps axo pid,args
```

### 與其它指令搭配

e.g. 列出所有跟 Gunicorn 相關的 processes:

```bash
ps aux | grep gunicorn
```

# 觀察即時動態

```bash
top
# or
htop
```

`ps` 只能在下指令的當下取一張 snapshot，若要動態監控系統資源使用狀況的即時狀態，就需要使用 `top`。

`htop` 與 `top` 的功能幾乎相同，只是 `htop` 長得比較漂亮，要使用的話須另外安裝（`brew install htop`）。

# 查詢 Processes

```bash
lsof [{OPTIONS}] [{PATH_TO_DIR}]
```

`lsof` 是 "**l**i**s**t **o**pen **f**ile" 的縮寫。

在 Linux 中，所有執行中的 processes 都有一個對應的「檔案」，processes 也會開啟一些檔案，這些檔案會被放在 /proc 底下，而 `lsof` 的功能就是列出這些被 processes 開啟的檔案，所以可以用來得知執行中的 processes 使用了哪些系統資源。

### 常用來篩選的 Options

- `-c {PROGRAM_NAME}|{APP_NAME}[,...]`

    列出所有與指定應用程式相關的 process files。

- `-u {USERNAME}[,...]`

    列出所有指定 user 觸發的 process files。

- `-p {PID}[,...]`

    列出所有與指定 pid 有關的 process files。

- `-i [4|6][TCP|UDP][@{HOSTNAME}|{HOSTADDR}][:{SERVICE}|{PORT}]`

    列出所有與指定網路位置有關的 process files。

    `[4|6]` 用來指定 IP version，分別代表 IPv4 與 IPv6，不填就代表都要。

使用多個 options 做為篩選 process files 的條件時，預設的行為是將這些條件的結果進行 "OR" 運算（取聯集），==若要取交集則要在最前面加上 `-a` options==。

# 終止 Process

```bash
kill [{SIGNAL}] {PID}
```

|Signal|效果|
|:-:|:-:|
|`-15`|Gracefully terminate a process，這是預設值。|
|`-2`|Gracefully terminate a process running in the foreground，效果等同於在正在執行該 process 的終端機上使用鍵盤 `Ctrl` + `C` 進行 interrupt。|
|`-9`|強制終止 process。|

### 與其它指令搭配

e.g. Gracefully restart Gunicorn:

```bash
ps aux | grep gunicorn | grep projectname | awk '{ print $2 }' | xargs kill -HUP
```

### 一次刪除多個 Processes

```bash
killall [{OPTIONS}] [{PROCESS_NAME_PATTERN}]
```

這個指令是用 process name 而非 pid 來指定要刪除的 processes。

通常這個指令用來一次刪除多個「符合條件」的 processes，比如下面這個例子就是刪除所有「名字以 `System` 開頭的 processes」：

```bash
killall System
```

**Options**

- `-e` (`--exact`)：名稱須完全比對成功才會終止
- `-I` (`--ignore-case`)：忽略名稱的大小寫
- `-i` (`--interactive`)：終止 process 之前先詢問
- `-l` (`--list`)：列出所有的 signal 名稱
- `-r` (`--regexp`)：使用 regex 指定 process 名稱
- `-s` (`--signal`)：指定終止 processes 的 signal
- `-u` (`--user`)：終止指定使用者所執行的 processes
- `-o` (`--older-than`)：開始執行的時間點在指定時間點之前的 processes 都刪除
- `-y` (`--younger-than`)：開始執行的時間點在指定時間點之後的 processes 都刪除

# Process Priority

在 Linux 系統中，各個 processes 可能會有不同的執行優先度（priority/niceness），優先度越高的 process 會被分配到越多比例的 [CPU time](</Operating System/CPU Scheduling.draft.md>)，優先度以整數 -20~19 表示，==數字越小優先度越高==。

### 先設置 Priority 再執行指令

使用 `nice` 可以在一個 command (process)「尚未開始執行前」先為其設置 priority，然後再執行 command：

```bash
nice -n {NICENESS} {COMMAND}
```

舉例而言，若準備要執行 `wget https://wordpress.org/latest.zip`，但想先將這個指令的 priority 設為 5，可以這樣寫：

```bash
nice -n 5 wget https://wordpress.org/latest.zip
```

若想將 priority 設為小於 0 的數字，則須擁有 root 權限：

```bash
sudo nice -n -1 wget https://wordpress.org/latest.zip
```

一旦 process 開始執行後就不能再用 `nice` 設置 priority，若想要在 process 執行的過程中調整 priority，則須使用 `renice`。

### 調整 Process Priority

```bash
# 調整指定 pid
sudo renice -n {NICENES} -p {PID}

# 調整由指定 user 所觸發的 processes
sudo renice -n {NICENESS} -u {USERNAME}

# 調整由指定 group 中的任一 user 所觸發的 processes
sudo renice -n {NICENESS} -g {GROUP}
```

- 若要使用 `renice` 調整 process priority，須先取得 `root` 的權限

### 查看 Priority

```bash
ps -l
# or
top
```

# 參考資料

- <https://ithelp.ithome.com.tw/articles/10247211>
- <https://blog.gtwang.org/linux/linux-lsof-command-list-open-files-tutorial-examples/>
- <https://linuxhint.com/linux-nice-renice-command-with-examples/>
