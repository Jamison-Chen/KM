>A job is a set of processes, comprising a shell pipeline, and any processes descended from it, that are all in the same process group.

Job 是由 Shell 管理的 [process group](</Operating System/Process.draft.md#Process Group>)，所以一個 job 可以由一到多個 processes 組成，不同 Shell sessions 間無法知道彼此管理哪些 jobs。

原則上一個 Shell command 就是一個 job，但若使用 [Pipe](</Operating System/Shell/3 - Operators.md>) operator (`|`) 將多個 Shell commands 串接起來，那它們就會被視為一個 compound command，所以是一個 job，比如：

```bash
grep title somefile.txt | sort | less
```

Commands 用 `;`、`&&` 和 `||` 連接則仍然會被視為多個 commands/jobs。

# Foreground & Background

如果我們說一個 job「在前景運行」，指的是該 job 佔用著 terminal 且可以與使用這互動（會接收來自 terminal 的 standard input）；而「在背景運行」就是沒用佔用 terminal 也不會接收來自 terminal 的 standard input。

# Job ID

在一個 Shell session 中，每個 job 都有 unique job id，但不同 Shell session 間的 job ids 就有可能會重複了。須注意的是，通常 job id 只被用在 interactive Shell 中，不會用在 Shell script 中，在 Shell script 中通常會使用 PGID（Recall: 一個 job 就是一個 process group），因為用 PGID 來定位會比 job id 更精準。

# Job Status

- Running
- Suspended
- Queued
- Exit

# 列出所有當前 Shell 所管理的 Jobs

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

# 讓背景的 Suspended Job 在背景恢復運作

```bash
bg %{JOB_ID}
```

- 記得 job id 前有 `%`
- 此時指定的 job status 會從 suspended 變成 running。
- 若要在一開始執行 command 時就直接將它丟到背景，不是使用 `bg`，要用 `&`：

    ```bash
    {COMMAND} &
    ```

# 把背景的 Job 拉回前景

```bash
fg [%{JOB_ID}]
```

- 記得 job id 前有 `%`
- 如果背景目前只有一個 job，則可以不用寫 `{JOB_ID}`。
- 若指定的 job 的 status 原本是 suspended，那拉到前景後 status 就會變成 running。

# 讓 Job 脫離 Shell 管理

```bash
disown [%{JOB_ID}]
```

- 記得 job id 前有 `%`
- 如果背景目前只有一個 job，則可以不用寫 `{JOB_ID}`。
- Job 脫離 Shell 管理後，並不會停止，而是會變成 orphan process，此時若要停止該 process 就只能用 `kill {PID}`

若單純使用 `bg` 或 `&` 將 job 丟到背景，那當使用者離開 Shell 時，這些 job 都會因為收到 `SIGHUP` 而終止（詳見下一段：Unix Signal），若希望一個 job 在使用者離開 Shell 後仍能繼續運行，則須讓這個 job 脫離 Shell 管理。

e.g.

```bash
nc -l localhost 8000 & ; disown
```

# 參考資料

- <https://en.wikipedia.org/wiki/Job_control_(Unix)>
