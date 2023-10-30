### 什麼是分支？

#TODO 

### 列出所有分支

```bash
# 只列出 local branches
git branch

# 只列出有 fetch 至 local 的 remote branches
git branch -r

# 將上面兩種皆列出
git branch -a
```

Example output:

```plantext
  bar
  foo
* master
```

- 有 `*` 的是目前所在的分支

### 新增分支

#TODO 

### 切換分支

#TODO 

### 重新命名分支

```sh
git branch -m <OLD_NAME> <NEW_NAME>
```

### 刪除分支

```sh
git branch -d <BRANCH>
```

- 不能刪除目前所在的分支
- 如果欲刪除的分支有一些目前所在的分支沒有的 commits，則 git 會提示：

    ```plaintext
    error: The branch foo is not fully merged.
    If you are sure you want to delete it, run 'git branch -D foo'.
    ```

    - 使用 `-D` option 就可以強制刪除
    - 若 merge 時使用 squash merge，則因為 squash merge 是一個全新的 commit，所以還是會出現上面的錯誤提示（`foo` squash merge `bar` 後，`foo` 上還是找不到 `bar` 上多出來的 commits）
