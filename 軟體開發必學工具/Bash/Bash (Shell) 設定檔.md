各種 Shell 都會有設定檔，比如 zsh 所使用的設定檔叫做 `.zshrc`、git bash 使用的設定檔則叫做 `.bashrc`。

### `PATH`

一般情況下，若某個 path 底下有一個「執行檔」叫做 `mycommand`，那麼若要執行該檔案就要完整地在 terminal 打出 `<PATH>/mycommand`；不過若在設定檔中加入 `PATH=<PATH>`，那在 terminal 直接輸入 `mycommand` 就可以執行該檔案。

這是因為每次在 terminal 輸入指令並按下 enter 時，shell 都會「依序」搜尋所有列在設定檔中的 PATHs，直到找到有與輸入的指令同名的執行檔為止，若全部搜尋完了還是找不到，就會冒出下方錯誤訊息（以「在 zsh 執行 `mycommand`」為例）：

```plaintext
zsh: command not found: mycommand
```
