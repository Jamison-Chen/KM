# 查看版本間的差異

看目前 working directory 有哪些更動還沒放到 staging area：

```bash
git diff
```

看目前的 staging area 有哪些更動還沒 commit 到 repo：

```bash
git diff --staged
```

看最近一次 commit 做了什麼：

```bash
git diff HEAD HEAD^
```

# 取得單個物件的詳細資訊

```sh
git show [<OPTIONS>] [<OBJECT>]
```

- `<OBJECT>` 可以是 commit、blob、tree 或 tag，預設值為 `HEAD`
- 所以最簡單的 `git show` 指令就是查看 HEAD commit 的詳細資訊
- 當 `<OBJECT>` 是一個 commit hash 時，顯示的資訊除了 hash、message、date、author 以外，也包括該次 commit 對內容所做的改動（也就是 `git diff HEAD HEAD^` 會拿到的東西）
# 依序取得多個 Commits 的詳細資訊

```bash
git log
```

Output 會依照 commit 的順序==由新到舊==依序列出:

```plaintext
commit d26358f4984d3bfab006a341788e61468c44dc10
Author: Jamison-Chen <jamison.chen@gmail.com>
Date:   Tue May 23 09:28:59 2023 +0800

    I add a new file, cool

commit d400b1af48a94d7a7ecdfda175193a4d5816673b
Author: Jamison-Chen <jamison.chen@gmail.com>
Date:   Tue May 23 09:27:47 2023 +0800

    this is my first commit
```

>[!Info]
>此指令列出的是目前所在的 [[#Branch]] 的 commits。

### 簡化 Log

可以加上 `--oneline` option 讓 log 看起來簡潔乾淨一點：

```bash
git log --oneline
```

Example output:

```plaintext
d26358f (HEAD -> main) I add a new file, cool
d400b1a this is my first commit
```

Commit hash value 本來全長是 40，但由於 hash 發生 collision 的機率極低，所以可以只用前 7 碼來 identify 一個 commit（詳見[[Tools/Git/L1 - Introduction#Git 如何確保 Data Integrity?|本文]]）。

`--oneline` 搭配 `--graph` 還可以得到類似 graph 的 log：

```bash
git log --oneline --graph
```

Example output:

```plaintext
* b781873c63e (HEAD -> after_paid_noti) add new cf ids
* 8ec1691658e Asia Fest seller coupons (#13648)
* fd87058ca06 adjust test& black format
*   cb6d870fb5b Merge branch 'dev'
|\  
| *   35c6e861f68 Merge branch 'dev'
| |\  
| * | c594e1b98ba add comment for HACK
* | | 22550f89f48 Fix test_listing_keyword_suggestion
| |/  
|/|   
* |   45527e60417 Merge branch 'upsert_payment_request_log' into dev
.
.
.
```

### 指定要從哪個 Commit 開始看起

```sh
git log <COMMIT>
```

### 限制 Log 的數量

e.g.

```bash
# show the last 10 commits
git log -10
```

### 看每一個 Commit 與它的前一個 Commit 的差異

```bash
git log -p

# or

git log --patch
```

這就等同於對所有 commits 依序做 `git show <COMMIT>`。

### 看每一個 Commit 修改了哪些檔案、修改了多少

```bash
git log --stat
```

`--stat` 的 output 是 `--patch` 的精簡版，最主要的差異是 `--patch` 會顯示實際更改的內容，`--stat` 只會用 +/- 來表示修改的量。

Example output:

```plainext
commit cb2b6050f1ce03d1cc75bfd58bf7f96760e11dae (HEAD -> main)
Author: Jamison Chen <jamison.chen@gmail.com>
Date:   Tue May 21 11:36:25 2024 +0800

    add try except

 models2/account.py    | 10 +++++++---
 models2/guest_cart.py |  8 +++++---
 2 files changed, 12 insertions(+), 6 deletions(-)
 
 ...
```

### 只列出某個人提交的 Commits

e.g.

```bash
git log --author="Bob"
```

### 只看與指定檔案相關的 Commits

e.g.

```bash
git log -- model/user.py
```

### 只看有新增或刪除指定字串的 Commits

e.g.

```bash
git log -S "hello world"
```

---

### 相同效果的 Commands

- `git show -s` = `git log -1`
- `git show` = `git log -1 -p`
- `git show <COMMIT>` = `git log -1 -p <COMMIT>`
