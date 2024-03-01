#Command 

### `man <COMMAND>`

顯示指定指令的使用說明 (manual)。

>[!Info]
>社群上有另一個 program 叫 [tldr](https://formulae.brew.sh/formula/tldr)，功能也是解釋各種指令的使用方式，且會附上很多範例。

### `!!`

再次執行前一個指令。

常被使用到的情境是：當你輸入一個指令後，發現須要有 `root` 權限才能執行這個指令，此時可以直接輸入 `sudo !!`。

### `alias`

列出所有 alias。

關於 alias 的設定方式，請見[[Operating System/Shell/Introduction#Alias|這篇文章]]。

### `clear`

清空目前終端機內的文字，也可以使用快捷鍵：`Control` + `l`。

### `date`

顯示目前時間。

### `exit [<EXIT_CODE>]`

以指定的 [[Operating System/Shell/Introduction#Exit Codes|exit code]] 離開目前的 shell session，exit code 預設為 0。

### `echo <STR>`

Stdout 指定字串。

e.g.

```bash
echo hello
echo "hello world"
```

- `echo` 搭配 [[Shell Script (1) - Overview#Output Redirection - >|output redirection]] 可以將文字寫入檔案
- 當字串中間含有空格時，不能直接寫在指令後面（比如 `echo hello world`），否則會被視為多個參數，有兩種方法可以處理有空格的字串：
    - 使用 `""` 將字串包起來，比如 `echo "hello world"`
    - 在每個空格前方加上 `\`，讓空格變成跳脫字元，比如 `echo hello\ world`

### `history [<OPTIONS>]`

搭配不同 options 可以達到不同效果，比如：

- `-p`：清除過去執行過的指令的歷史紀錄

### `pbcopy < <FILE>`

將檔案的內容複製到剪貼簿。

效果等同於「打開檔案 → 全選檔案內容 → 複製」這個流程。

這個指令中使用到 `<` operator，這個動作稱為 [[Shell Script (1) - Overview#Input Redirection - <|input redirection]]。

### `shred [<OPTIONS>] <FILE>`

#TODO 

### `awk`

請見：<https://ithelp.ithome.com.tw/articles/10268041>

### `sed`

#TODO 

### 重啟 Shell

```bash
exec "$SHELL"
```

# `systemctl`

# `timedatectl`

# 快捷鍵

|快捷鍵|功能|
|:-:|:-:|
|方向鍵 $\uparrow$|顯示上一次輸入的指令|
|`Tab`|自動補齊未打完的 command/directory/file 名稱|
|`Control` + `c`|送出 `SIGINT` 訊號，打斷目前 terminal 前景執行中的指令|
|`Control` + `d`|送出 `EOF` 訊號。<br/>若本來在 input mode 則離開 input mode<br/>若本來在 shell 則離開 shell session（效果同 `exit` 指令）|
|`Control` + `l`|清空目前的 terminal|
|`Control` + `w`|刪除游標前方的單字|
|`Control` + `z`|將執行中的命令丟到背景執行|
|`Control` + `Shift` + `c`|複製文字|
|`Control` + `Shift` + `v`|貼上文字|

# Linux-Windows 指令對照表

|Linux|Windows|
|:-:|:-:|
|`cd`|`cd`|
|`pwd`|`cd`|
|`ls`|`dir`|
|`mkdir`|`mkdir`|
|`cp`|`copy`|
|`mv`|`move`|
|`rm`|`del`|
|`clear`|`cls`|

# 參考資料

- <https://www.macupdate.com/how-to/mac-terminal-commands-list>
- <https://kinsta.com/blog/linux-commands/>
