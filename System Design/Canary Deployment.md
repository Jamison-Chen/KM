當開發端有新的 Feature 要更新到上線中的產品時，可能會有以下考量：

- 新 feature 是否有 bug?
- 用戶對新 feature 的接受度如何？

比較理想的做法應該是選擇先讓部分用戶體驗新 feature，蒐集 feedbacks 一陣子，確認沒問題後再逐步 apply 到所有用戶上。

Canary deployment 正是為了實現這個流程而生。

# Canary Deployment 的種類

依照實現方式，大致可以把 canary deployment 分為以下兩種：

##### Rolling Deployment

若 production environment 上平時有多個 servers 分擔工作，此時可以只在少數幾個 severs 上部署新的 feature（程式碼）。

把使用者依照某種規則（比如 ID）分為實驗組與對照組，當實驗組的 client 請求服務時，會被導向裝有新 feature 的 server，對照組則會被導向安裝著原先版本的 server。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/rolling-deployment.png>)

### Side-by-Side Deployment

建立另一個 production environment，部署上有新 feature 的程式碼。

一樣把使用者依照某種規則分為實驗組與對照組，當實驗組的 client 請求服務時，會被導向裝有新 feature 的 production environment，對照組則會被導向安裝著原先版本的 environment。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/side-by-side-deployment.png>)

# 參考資料

- <https://semaphoreci.com/blog/what-is-canary-deployment>
