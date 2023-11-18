當開發端有新的 Feature 要更新到上線中的產品時，可能會有以下考量：

1. 新 Feature 是否有 Bug?
2. 用戶對新 Feature 的接受度如何？

比較理想的做法應該是選擇先讓部分用戶體驗新 Feature，蒐集 feedbacks 一陣子，確認沒問題後再逐步 apply 到所有用戶上。

Canary Deployment 可以說正是為了實現這個流程而生。

# Canary Deployment 的種類

依照實現方式，大致可以把 Canary Deployment 分為以下兩種：

### Rolling Deployment

若 Production Environment 上平時有多個 Servers 分擔工作，此時可以只在少數幾個 Severs 上部署新的 Feature（程式碼）。

把使用者依照某種規則（比如 id）分為實驗組與對照組，當實驗組的 client 請求服務時，會被導向裝有新 Feature 的 Server，對照組則會被導向安裝著原先版本的 Server。

![[rolling-deployment.png]]

### Side-by-Side Deployment

建立另一個 Production Environment，部署上有新 Feature 的程式碼。

一樣把使用者依照某種規則分為實驗組與對照組，當實驗組的 client 請求服務時，會被導向裝有新 Feature 的 Production Environment，對照組則會被導向安裝著原先版本的 Environment。

![[side-by-side-deployment.png]]

# 參考資料

關於 Canary Deployment 的好處、逐步 Apply 的方法，以及其他 Canary Deployment 細節，請參考[這篇文章](https://semaphoreci.com/blog/what-is-canary-deployment)
