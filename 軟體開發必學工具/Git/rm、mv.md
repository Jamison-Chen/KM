### 刪除檔案

```bash
git rm <FILE>
git commit -m "<COMMIT_MESSAGE>"
```

`git rm <FILE>` 等價於 `rm <FILE>` + `git add <FILE>`。

>[!Danger]
>這個指令真的會把檔案刪除！

### 移動檔案 & 重新命名

```bash
git mv [<OLD_PATH>/]<FILE> [<NEW_PATH>/]<FILE>
```

若 `[<OLD_PATH>/]` 等於 `[<NEW_PATH>/]` 則其實是在將檔案重新命名。

`git mv [<OLD_PATH>/]<FILE> [<NEW_PATH>/]<FILE>` 效果等同於 `mv [<OLD_PATH>/]<FILE> [<NEW_PATH>/]<FILE>` + `git add [<NEW_PATH>/]<FILE>`，此時 `git status` 所顯示的檔案狀態會是 "renamed"：

```plaintext
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        renamed:    test1 -> test11
```
