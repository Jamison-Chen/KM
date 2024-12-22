>[!Note] 官方網站
><https://aws.amazon.com/cli/>

AWS CLI 是一個用來管理 AWS 資源的工具，可以用來進行幾乎任何可在 AWS Management Console（一個網頁式 GUI）上進行的操作。

# Installation

### On MacOS

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# check version
aws --version
```

### On Linux

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# check version
aws --version
```

>[!Info]
>也可以到 AWS 官網下載 installer，使用 GUI 安裝。

# 在開始之前：建立 IAM Identity

因為 AWS CLI 須要先取得 user 的 access key，才能用那個 user 的權限對存取指定的 AWS account 所擁有的資源。==強烈建議不要直接使用 root user 的 long-term access key==，比較好的方法先透過 [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/) 建立一個 IAM identity，使用 IAM identity 的 access key。

建立好 IAM identity 後，會拿到一個 ==AWS access portal URL==，進入該 URL 後會看到該 identity 可以訪問的所有 accounts 與 applications，以及每個 accounts/applications 的 access key，這些 access keys 都是 ==short-term 的==。

>[!Note]
>[AWS IAM](https://aws.amazon.com/iam/) 與 [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/) 是兩個不同的服務，前者只能管理單一個 AWS account 底下的 IAM users；後者則可以跨 accounts 管理 IAM "identities"。
>
>這兩個服務中的 IAM users 不互通，也就是說，使用 IAM 建立的 user 沒辦法透過 IAM Identity Center 管理，反之亦然。通常會建議使用 IAM Identity Center 進行管理就好。
>
>關於 IAM user 的完整介紹，請看[[帳號、使用者與權限管理.canvas|這篇]]。

# Configure the AWS CLI

### 方法一：使用 Credentials

在 terminal 輸入以下指令：

```bash
aws configure
```

此時會看到以下問題：

```plaintext
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]:
Default output format [None]:
```

- **Option 1: Short-Term Credentials**

    如果要使用 IAM Identity Center 所管理的 role 的權限操作 AWS CLI，須到對應的 AWS access portal 找到對應的 AWS account，點擊 Access keys 取得相關資訊並貼上：

    ![[aws-access-portal.png]]

    使用 short-term credential 時，還須額外設定 session token 這個參數：

    ```bash
    aws configure set aws_session_token {YOUR_SESSION_TOKEN}
    ```

- **Option 2: Long-Term Credentials**

    如果是要直接使用 AWS account 的 IAM user 或 root user 操作 AWS CLI，則須到右上角選單中的 Security credentials 取得，預設不會有 access key，須要手動建立：

    ![[aws-security-credentials.png]]

    使用 long-term credential 時不須要輸入（也沒有）session token。

    >[!Warning]
    >強烈建議不要使用 root user 的 access key 來操作 AWS CLI。

---

完成後，==home directory 會多一個叫 .aws 的資料夾==，裡面有 config 與 credentials 兩個檔案，這兩個檔案的內容分別是剛才填寫的資訊：

**config**

```plaintext
[default]
region = {YOUR_REGION_NAME}
output = {OUTPUT_FORMAT}
```

**credentials**

```plaintext
[default]
aws_access_key_id = {YOUR_ACCESS_KEY_ID}
aws_secret_access_key = {YOUR_SECRET_ACCESS_KEY}
aws_session_token = {YOUR_SESSION_TOKEN}
```

可以直接編輯這兩個檔案來更改設定。

使用 `aws` 指令時，若沒有特別提供 argument `--profile {PROFILE}`，則預設是使用 `[default]` 的 config 與 credentials。或者也可以先設定好環境變數：

```bash
export AWS_PROFILE={PROFILE}
```

這樣一來當次 Shell session 中的 `aws` 指令就都不須要額外加上 `--profile` argument 了。

### 方法二：使用 SSO

SSO 的意思就是使用 IAM Identity Center 所管理的 role 的權限操作 AWS CLI。

先在 terminal 輸入以下指令：

```bash
aws configure sso
```

此時會看到以下問題，須到對應的 AWS access portal 找到對應的 AWS account，點擊 Access keys 取得相關資訊並貼上：

```plaintext
SSO session name (Recommended):
SSO start URL [None]:
SSO region [None]:
SSO registration scopes [sso:account:access]:
```

- SSO session name 可以隨意取。
- SSO start URL 與 SSO region 須從 AWS Access Portal 複製：

    ![[aws-access-portal.png]]

- SSO registration scopes 可以直接 enter（使用預設值）。

完成後會看到以下訊息，並且會打開瀏覽器進行驗證：

```plaintext
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

{URL}

The only AWS account available to you is: {YOUR_ACCOUNT_ID}
Using the account ID {YOUR_ACCOUNT_ID}
The only role available to you is: {ROLE_NAME}
Using the role name {ROLE_NAME}
```

最後要做一些關於 CLI 的設定：

```bash
CLI default client Region [{REGION}]:
CLI default output format [{OUTPUT_FORMAT}]:
CLI profile name [{ROLE_NAME}-{YOUR_ACCOUNT_ID}]:
```

使用這個方法的話，完成後也會發現 home directory 多一個叫 .aws 的資料夾，其中會有一個叫 config 的檔案以及一個叫 sso 的子資料夾，其中 sso 資料夾裡會有當次 session 的 access token、secret key 等資料。

>[!Info]
>關於 config、credentials 這些設定檔中的細節，請見[官方文件](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format)。

---

### 其它與 Configuration 相關的指令

- 設定單一參數

    ```bash
    aws configure set {KEY} {VALUE} [--profile {PROFILE}]
    ```

- 取得指定參數的值

    ```bash
    aws configure get {KEY} [--profile {PROFILE}]
    ```

- 列出指定 profile 的所有設定

    ```bash
    aws configure list [--profile {PROFILE}]
    ```

- 列出 profiles

    ```bash
    aws configure list-profiles
    ```

### 透過環境變數來設定

因為使用 `aws configure` 指令所設定的資料會以檔案的形式被存在 .aws 裡，其中包含 token、secret 等機敏資訊，若你不希望設定以檔案的形式儲存，可以選擇改用「設定環境變數」的方式來取代之。詳細此處略，請見[官方文件](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)。

# 登入／登出 IAM IC (SSO) Session

使用 IAM Identity Center role (SSO) 登入的話，token 是短期的，所以過一段時間後就會須要重新登入來更新 token：

```bash
aws sso login --profile {PROFILE}

# or

aws sso login --sso-session {SESSION_NAME}
```

登出：

```bash
aws sso logout
```

一個 token 的有效期間稱為一個 **session**。
