.git folder 就是所謂的 repo，.git 是 Git 用來達成版本控制的唯一資料夾。

# 擁有 .git 就幾乎擁有整個專案

若要將 local 的一個專案複製一份（一樣在 local），除了直接 `Command c` → `Command v` 外，也可以使用 Git 指令來耍帥一下，耍帥步驟如下：

- Step1: 新增一個新的 folder，這個 folder 就是複製後的專案
- Step2: 將原專案的 .git folder 複製一份到 Step1 的 folder 裡
- Step3: 現在是見證奇蹟的時刻，在新 folder 中使用以下指令：

    ```bash
    git checkout .
    ```

現在你會看到原本空蕩蕩的 folder 已將變得跟原專案「幾乎」一樣了，甚至連 commit 的紀錄都有！也就是說你也可以像在原專案中一樣在版本間切換。

為什麼要強調「幾乎」呢？這是因為 **untracked** 與 **ignored** 的檔案由於不在 Git 的管控內，所以也就無法透過 .git 重現。
