# 正式機 DB

### db01 configs

- User: pinkoi
- Password: 去 pinkoi repo 的 settings_base.py 找 `DATABASE_PASSWORD`

>[!Note]
>實際輸入密碼時，若使用的是 tableplus 的介面才是輸入上面設定的密碼；若是使用 Mac 的介面，則要輸入開機密碼（或指紋）。

### db02 configs

- User: readonly
- Password: readonly

>[!Note]
>實際輸入密碼時，若使用的是 tableplus 的介面才是輸入上面設定的密碼；若是使用 Mac 的介面，則要輸入開機密碼（或指紋）。

### 注意事項

- 如果 SQL 跑太久或 loading 太大，要直接 kill
- 如果 SQL 就是要跑很久，請搭配 grafana 看 mysql 的狀態
- DB 裡面很多個資，除非業務需求否則不要窺探別人隱私

# 連線 Staging 環境

```sh
ssh staging
```

### 注意事項

- Staging 環境是拿來跑 script 用的，不建議在上面起 server
- 跑任何會發通知的 script 之前，請先跑過 `make compile-intl`，不然會發生沒有翻譯的慘劇
- Staging 所有 users 的 Docker image 都是共用的，不要隨便跑 `make python-container` 之類的 command
- 跑 script 的時候可以用 `htop` 觀測 server 的狀態
- 跑 script 的時候可以用 `tmux` 跑，就不會因為 session 斷開而 process 被中斷
- `tmux` 用完後記得把 session 關掉
