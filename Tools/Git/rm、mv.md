# 刪除檔案

```sh
git rm <FILE>
git commit -m "<COMMIT_MESSAGE>"
```

>[!Danger]
>這個指令真的會把檔案刪除！

- `git rm <FILE>` = `rm <FILE>` + `git add <FILE>`
- `git rm <FILE>` 會讓該檔案的狀態變成 "Deleted - Staged"；`rm <FILE>` 只會讓檔案的狀態變成 "Deleted - Unstaged"

### 強制刪除

只有當指定檔案原本的狀態是 "Committed/Unmodified" 時，才可以直接對該檔案做 `git rm`，若指定檔案本來的狀態是 "Modified" 或 "Staged"，則須加上 `-f` option。

```sh
git rm -f <FILE>
```

若檔案原本的狀態是 "Untracked" 或 "Ignored"，則無法對其做 `git rm`。

### 讓檔案脫離 Git 版控

在介紹 [Ignore](</Tools/Git/L4 - Ignore.md#已經被管控的檔案怎麼脫身？>) 時有提過，若有一個已經被 Git 管理的檔案想脫離 Git 版控，除了須要將它加進 .gitignore 外還須要讓 Git 遺忘它，使用的是這個指令：

```sh
git rm --cached <FILE>
```

加上 `--cached` option 的 `git rm` 會讓某個檔案的狀態變成 "Deleted - Staged, and Untracked"，此時這個==檔案並沒有被刪除==。

另一個與單純 `git rm` 不同的是：`git rm --cached` 不只可以對本來狀態為 "Committed/Unmodified" 的檔案做，也可以對 "Modified" 或 "Staged" 的檔案直接做，不須要加上 `-f` option。

# 移動 & 重新命名檔案／目錄

```sh
git mv <OLD/PATH> <NEW/PATH>
```

- 若改動前後的 paths 完全相同，就代表是在重新命名
- Path 的最後若不是 file name 而是 directory name，就代表是在移動／重新命名 directory

`git mv <OLD/PATH> <NEW/PATH>` = `mv <OLD/PATH> <NEW/PATH>` + `git add <NEW/PATH>`

`git mv` 後（無論是重新命名或是移動），檔案狀態皆會是 "Renamed"。`git status` 的 output 如下：

```plaintext
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        renamed:    hello -> world
```
