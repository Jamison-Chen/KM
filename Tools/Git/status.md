```bash
git status
```

這個指令不只會顯示目前 repository 的狀態，還會提示你應該做什麼動作：

- Working directory 有一些檔案變動，且有一些 untracked files：

    ```plaintext
    On branch main
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git restore <file>..." to discard changes in working directory)
            modified:   .gitignore
    
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
            test1
    
    no changes added to commit (use "git add" and/or "git commit -a")
    ```

- Staging area 有一些變動尚未被 commit：

    ```plaintext
    On branch main
    Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
        modified:   hello
    ```

- 沒有任何未 commit 的變動

    ```plaintext
    On branch main
    nothing to commit, working tree clean
    ```

### 精簡一點

如果只是想大概看一下目前的狀態，也可以加上 `--short` (`-s`) 讓輸出精簡一點，通常建議也搭配 `--branch` (`-b`) 使用：

```bash
git status -sb
```

Example output:

```plaittext
## main
 M test1
```
