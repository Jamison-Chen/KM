### 相關 Tasks

- https://app.asana.com/0/1201591574237600/1204719274585087/f
- https://app.asana.com/0/1201591574237600/1204913798194094/f
- https://app.asana.com/0/1201591574237600/1205071817241001/f

### 會動到的檔案

- base/campaign/credit_card/const.py
- base/campaign/credit_card/deduction.py
- base/campaign/site_campaigns/campaign_2023/credit_card_campaign_2023.py

### 注意事項

同一個週期 (period) 內，若有兩個以上的 campaigns 要進行，則即使這些 campaigns 的期間沒有重疊，也不可以共用同一個 campaign key，否則在計算 period limit 時會出錯。

### Tester 的用意

### 哪裡會顯示 Campaign 文案？

Credit Card Campaign 文案只會顯示在結帳頁下半部（付款方式的上方，紅底，`payment_method_promotion_note`/`exceed_limit_promotion_note`），實際套用到的會顯示在付款方式左側（灰字，`site_additional_note`）

### 相關 Tables

- `campaign_credit_card`