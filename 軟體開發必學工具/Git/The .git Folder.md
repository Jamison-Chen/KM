在 [[CH1 - 簡介#常用術語|CH1 進行常用名詞的解釋]] 時有寫道：「repo 是一個版本控制系統所控制的最大單位」，其實幾乎可以說 `.git` directory 才是所謂的 repo，一個 repo 就對應到一個 `.git`，`.git` 是 Git 用來達成版本控制的唯一 folder。

# 深入 `.git` Folder

#TODO 

# 擁有 `.git` Folder 就幾乎擁有整個專案

若要將 local 的一個專案複製一份（一樣在 local），除了直接 `Command C` `Command V` 外，也可以使用 git 指令來耍帥一下，步驟如下：

- Step1: 新增一個新的 folder，這個 folder 就是複製後的專案
- Step2: 將原專案的 `.git` folder 複製一份到 Step1 的 folder 裡
- Step3: 現在是見證奇蹟的時刻，請在新 folder 中使用以下指令：

    ```bash
    git checkout .
    ```

    現在你會看到原本空蕩蕩的 folder 已將變得跟原專案「幾乎」一樣了，甚至連 commit 的紀錄都有！也就是說你也可以像在原專案中一樣在版本間切換。

等等，為什麼要強調「幾乎」呢？

這是因為列在 `.gitignore` 的檔案由於不在 Git 的管控內，當然就無法透過 `.git` 重現。
