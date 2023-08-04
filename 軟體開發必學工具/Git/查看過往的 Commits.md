```bash
git log
```

Output 會依照 commit 的順序==由新到舊==依序列出:

```plaintext
commit d26358f4984d3bfab006a341788e61468c44dc10
Author: Jamison-Chen <jamison.chen@pinkoi.com>
Date:   Tue May 23 09:28:59 2023 +0800

    I add a new file, cool

commit d400b1af48a94d7a7ecdfda175193a4d5816673b
Author: Jamison-Chen <jamison.chen@pinkoi.com>
Date:   Tue May 23 09:27:47 2023 +0800

    this is my first commit
```

從上面的 output 可見，每個 commit 都會有一個 40 碼的 hash value 做為它的 id（詳見 [[CH1 - Intro to Git#Git 如何確保 Data Integrity?]]），由於 hash value 發生 collision 的機率極低，所以甚至可以只看前 7 碼就知道是哪個 commit。

>[!Info]
>列出的是目前所處的 [[#Branch]] 的 commit。

### 簡化 Log

可以加上 `--oneline` option 讓 log 看起來簡潔乾淨一點：

```bash
git log --oneline
```

Output:

```plaintext
d26358f (HEAD -> main) I add a new file, cool
d400b1a this is my first commit
```

之後開始用到 branch 後，`--oneline` 搭配 `--graph` option 就可以 stdout 類似 graph 的 log：

```bash
git log --oneline --graph
```

Output:

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

### 指定要從哪個 commit 開始看起

```bash
git log <COMMIT_ID>
```

### `-<N>` 限制 log 的數量

```bash
git log -<N>
```

### `--stat` 看每一個 commit 修改了哪些檔案

```bash
git log --stat
```

### `--patch` 看每一個 commit 與它的前一個 commit 的差異

```bash
git log -p
# or
git log --patch
```

### `--` 只看與指定檔案相關的 commits

```bash
git log -- <PATH_TO_FILE>
```

### `--author` 只列出某個 author 提交的 commits

```bash
git log --author="<AUTHOR_NAME>"
```
