### 相關 Tasks

- [Seller Rating Tool (Reason: B22)](https://app.asana.com/0/1201591574237600/1204191157675342/f)
- [Pinkoi Academy](https://app.asana.com/0/1201591574237600/1204212555752821/f)
- [After Paid Notification](https://app.asana.com/0/1201591574237600/1204028093057409/f)

# 教學文件

- [通知系統 (Email, App Push, Notification Center)](https://sites.google.com/pinkoi.com/epd-wiki/home/dev-guide/for-backend-engineers/know-how/%E5%90%84%E9%A1%9E%E7%B3%BB%E7%B5%B1%E9%80%9A%E7%9F%A5%E9%96%8B%E7%99%BC%E6%96%B9%E6%B3%95?pli=1&authuser=1)
- [Guiding Tips (GT)](https://paper.dropbox.com/doc/Guiding-Tips-Admin-Tool---B2wmGo~M3CncImEXm56k33WDAg-wQwhd4F32n8DVeHkuan6X)

> [!Note]
> 通知系統 (Email, App Push, Notification Center) 分為[[#新版通知系統|新版]]與[[#舊版通知系統|舊版]]，若有新的通知要發，要用新版。

# 新版通知系統

### Repo 中的相關檔案

- `models2/notification/configs.py` 定義每一種不同的通知的 mata

    [UTM Meta 命名原則的文件](https://docs.google.com/spreadsheets/d/1sSb2Zd-SCFFcxCOvvlPMmizIH7MK_ViU0fHDB6wbwlg/edit?pli=1#gid=1969289036)

- `models2/notificaiton/contexts.py` 定義通知的 template 中可塞入哪些名字的變數

- `models2/notification/service.py`

    其中的 `NotificationServeice` 是負責發送通知的 Class，具有發送通知用的 `send` method。

### Email

需要有一個與 email config 的 `conent_key` 同名的 `.mako` 檔案作為 template，比如當 `content_key` 為 `test_notification` 時，就要有一個叫做 `test_notification.mako` 的檔案，這個檔案要放在 `/rabbitmq/consumers/templates` 底下。

### App Push

> [!Note]
> App Push 有字數限制：以中文字而言，Subject + Body Text 不可超過 516 個字。

### Notification Center (NC)

在 `models2/notification/configs.py` 中加上 NC config 後，須手動在測試環境中跑這個檔案最後的 `update_nc_templates` function，但在正式機不用手動跑，因為這已經包括在 CI 的流程中。

# Guiding Tips (GT)

GT 的發送方式與其他三者皆不同。

#TODO 

# 預覽 Email

`/models2/noti_mocks.py`

#TODO 

# 舊版通知系統

### Repo 中的相關檔案

- `base/notification`

    `CONF` dictionary 用來定義通知

#TODO 
