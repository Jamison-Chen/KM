### 刪除檔案

```bash
git rm <FILE>
git commit -m "<COMMIT_MESSAGE>"
```

`git rm <FILE>` 等價於 `rm <FILE>` + `git add <FILE>`。

>[!Danger]
>這個指令真的會把檔案刪除！

### 移動 & 重新命名 File/Directory

```sh
git mv <OLD/PATH/TO/FILE> <NEW/PATH/TO/FILE>
```

- 若改動前後的 path 完全相同，就代表是在重新命名
- Path 的最後若不是 file name 而是 directory name，就代表是在移動／重新命名 directory

`git mv <OLD/PATH/TO/FILE> <NEW/PATH/TO/FILE>` 效果等同於 `mv <OLD/PATH/TO/FILE> <NEW/PATH/TO/FILE>` + `git add <NEW/PATH/TO/FILE>`，此時 `git status` 所顯示的檔案狀態會是 "renamed"：

```plaintext
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        renamed:    test1 -> test11
```
