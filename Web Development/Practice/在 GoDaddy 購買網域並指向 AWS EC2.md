### Step1: 在 GoDaddy 購買網域

比如購買 my-domain.com。

### Step2: 在 AWS Route53 上 Create Hosted Zone

輸入剛剛購買的 my-domain.com，成功建立後會出現一個 NS Record。

### Step3: 在 GoDaddy 上設定網域的 Name Server

把 name server 的網址改成剛剛出現在 Route53 的 NS Record 中的 values（應該會有 4 個值）。

### Step4: 在 Route53 上新增 A Record

Value 填 EC2 instance 的 public IP。

### Step5: 等待 DNS Propagation

最多需要等兩天，但通常不用這麼久。
