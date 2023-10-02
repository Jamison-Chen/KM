#Command 

### `man <COMMAND>`

顯示指定指令的使用說明 (manual)。

### `!!`

再次執行前一個指令。

比較被使用到的情境是：當你輸入一個指令後，發現須要有 `root` 權限才能執行這個指令，此時可以直接輸入 `sudo !!`。

### `alias`

列出所有 alias。

關於 alias 的設定方式，請見[[Operating System/Shell/Introduction#Alias|這篇文章]]。

### `date`

顯示目前時間。

### `exit`

離開目前的 shell session。

### `clear`

清空目前終端機內的文字，也可以使用快捷鍵：`Control` + `l`。

### `echo <STR>`

輸出指定文字。

e.g.

```bash
echo hello
echo "hello world"
```

- `echo` 搭配 [[Shell Script#Output Redirection - >|output redirection]] 可以將文字寫入檔案
- 當字串中間含有空格時，不能直接寫在指令後面（比如 `echo hello world`），否則會被視為多個參數，有兩種方法可以處理有空格的字串：
    - 使用 `""` 將字串包起來，比如 `echo "hello world"`
    - 在每個空格前方加上 `\`，讓空格變成跳脫字元，比如 `echo hello\ world`

### `pbcopy < <FILE>`

將檔案的內容複製到剪貼簿。

效果等同於打開檔案 $\rightarrow$ 全選檔案內容 $\rightarrow$ 複製。

這個指令中使用到 `<` operator，這個動作稱為 [[Shell Script#Input Redirection - <|input redirection]]。

### `history [<OPTIONS>]`

搭配不同 options 可以達到不同效果，比如：

- `-p`：清除 command 歷史紀錄

### `shred [<OPTIONS>] <FILE>`

#TODO 

### `awk`

請見：<https://ithelp.ithome.com.tw/articles/10268041>

### `sed`

#TODO 

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
