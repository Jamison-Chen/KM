Shell 是 OS 的最外層，是使用者與 OS 互動的介面，這個介面可以用來執行／轉譯一種 shell 專用的程式語言（這種程式語言就叫做 shell script）。

### 使用者如何透過 Shell 與 OS 互動？

```mermaid
flowchart
    id1("顯示輸入框接收使用者的 shell script")
    id2("使用者輸入指令")
    id3("Shell")
```

Shell 會透過輸入框接收使用者的指令，並將指令轉譯為 OS 看得懂的指令請 OS 執行，最後將 OS 的執行結果印在介面上

各種 shell 都可以透過設定檔進行設定，設定檔有三種，有不同用途，比如 zsh 所使用的設定檔叫做 `.zshrc`、bash 使用的設定檔叫做 `.bashrc`。

### `PATH`

一般情況下，若某個 path 底下有一個「執行檔」叫做 `mycommand`，那麼若要執行該檔案就要完整地在 terminal 打出 `<PATH>/mycommand`；不過若在設定檔中加入 `PATH=<PATH>`，那在 terminal 直接輸入 `mycommand` 就可以執行該檔案。

這是因為每次在 terminal 輸入指令並按下 enter 時，shell 都會「依序」搜尋所有列在設定檔中的 PATHs，直到找到有與輸入的指令同名的執行檔為止，若全部搜尋完了還是找不到，就會冒出下方錯誤訊息（以「在 zsh 執行 `mycommand`」為例）：

```plaintext
zsh: command not found: mycommand
```

# 參考資料

- <https://ss64.com/osx/syntax-profile.html>
