# 如何進入「被 Code Review」的流程

### Step1

在 GitHub 上開 Pull Request，主旨中須包含 Asana 上的對應 Task（以下簡稱 Main Task），成功開立後會看到此次 Pull Request 的 PR_number（會以 `#` 開頭）。

![[Screenshot 2023-03-19 at 1.43.39 PM.png]]

### Step2

在 Asana 上的 Main Task 下新增一個 Subtask，標題為 `Code Review <PR_number>`，舉例如下：

![[Screenshot 2023-03-19 at 1.45.14 PM.png]]

### Step3

在 Subtask 的 Description 中貼上 GitHub Pull Request 的連結。

### Step4

將 Asana Task 的 Project 設為 Backend（在 More actions 點擊 Add to project）

![[Screenshot 2023-03-20 at 8.26.10 PM.png]]

![[Screenshot 2023-03-19 at 1.38.52 PM.png]]

### Step5

將 Lead (ZihZih) 加入為 Collaborator，完成！

通過 Code Review 後，就可以 Deploy 到正式環境了，詳細步驟請見 [[發車 & Revert|此處]]。