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

###### Mako Template

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

# 其他

### 關閉通知

在 `user_notification_status` table 中有一個 column 叫 `enabled`，`enabled` = 1 代表該 user 不會收到某種類別的通知（類別由 `noti_type` 與 `content_type` 兩個 column 決定），若同時 `modified_by` = "system"，則代表該 user 是被系統冷凍的 user（詳見[此段](https://github.com/pinkoi-inc/pinkoi/blob/5b91509b8d6602663b1ea76e0496f341e9c85f38/models2/user_notification_status.py#L18)）。

>[!Note]
>系統只會冷凍 `buyer_` 開頭的通知種類。

在 `profile` table 中有一個 column 叫 `preference`，使用 14 個 bits 控制 user 的 14 種通知分別是開啟或關閉（1 是關閉，0 是開啟）。

當 user 主動將某個通知開啟／關閉時，`preference` 對應的 bit 會被反轉，`user_notification_status` 中也會 update-or-create 一筆資料，將 `enabled` 設為相對應的值（1 是關閉，0 是開啟）、`modified_by` 設為 "user"（`modified_by` 也是 primary key 的一部份）。

系統冷凍 user 時，只會更改 `user_notification_status`，不會更改 `preference`。

當被冷凍的 user 登入時，會被解凍，解凍的意思就是將 `user_notification_status` 中，該 user 的所有 `modified_by` = "system" 且 `enabled` = 1 的 rows 都改為 0（`preference` 一樣不會連動）。

寄送 email 時（新舊版都是），會先依據 `preference` 決定是否要送，如果要，再依據 `user_notification_status` 決定是否要送，所以當兩者狀態不等價時，只要任一邊是關的，就無法送出。

###### 舊版 Notification

先：

```Python
# base/notification.py::send_notification
(
    user_email_pref,
    is_email_permanent_bounced,
) = EmailPreference.query_pref_and_permanent_bounced_flag(uid)

email_is_sendable = (
    ignore_email_pref
    or notification_config["email_type"] == "test_email"
    or EmailPreference.has_email_permission(
        user_email_pref,
        notification_config["email_type"],
    )
) and (ignore_email_permanent_bounced or not is_email_permanent_bounced)
```

再：

```Python
# base/notification.py::send_notification()
if email_is_sendable and user_notification_status.is_user_email_freezed(
    uid, notification_config["email_type"]
):
email_is_sendable = False
```

###### 新版 Notification

先：

```Python
# models2/notifiaction/email/config.py::EmailNotificationConfigItem._query_uid_email_map()
if not option.ignore_email_pref:
    freezed_uid_set = set(
        query_freezed_uids(
            list(uid_set_need_query_emails),
            noti_type='email',
            content_type=self.email_type,
        )
    )

uid_set_need_query_emails -= freezed_uid_set
```

再：

```Python
# models/User.py::query_uid_emails_map()
query = OraUser.query().where_in('uid', uids)
if email_type is not None:
    email_flag = EmailPreference.get_email_flag(email_type)
    query.where_raw(f'preference & {email_flag} = 0')
```

---

>[!Question]
>某天有一個使用者自己關掉某種通知 A，然後有一天他被系統冷凍了，再過幾天他登入了（所以被解凍），請問他現在收得到 A 種類的通知嗎？

>[!Summary] Answer
>收不到，因為從使用者自己關掉後，通知 A 在 `preference` 中就一直都是關閉的，不會因為系統冷凍或解凍而改變，而送信時只要兩邊有一邊是關的就送不了，所以收不到。

### [沒有成功寄出信的可能原因](https://paper.dropbox.com/doc/--B9Ir6izJRE0COc0qdF2Dyv6YAg-rIA8F1XCh3lHKslIdt0u1)

### [[存取資料庫#通知紀錄|通知紀錄]]
