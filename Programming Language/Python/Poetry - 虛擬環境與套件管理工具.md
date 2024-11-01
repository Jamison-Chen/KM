>[!Note]
>關於什麼是 Python 虛擬環境以及使用虛擬環境的好處，請看[[venv#Python 虛擬環境|這裡]]。

# 為既有專案建置虛擬環境

>[!Note]
>下方步驟是針對從來沒使用 Poetry 管理過的專案，若專案本來就是用 Poetry 管理的，只是要重新安裝環境，請看[[#根據 poetry.lock 或 pyproject.toml 安裝套件|本段]]。

### 須在全域先安裝 Poetry 的方法

- **Step1: 在全域安裝 Poetry**

    ```bash
    pip install poetry
    ```

- **(Optional) Step2: 設定 In-Project Virtual Environment**

    ```bash
    poetry config virtualenvs.in-project true --local
    ```

    - 此時專案跟目錄會出現一個叫 **poetry.toml** 的檔案，這個檔案是用來設定 Poetry 的行為的設定檔。
    - "In-project" 的意思是將虛擬環境資料夾放在專案跟目錄中。
    - `virtualenvs.in-project` 預設是 false。

- **Step3: 初始化 Poetry 設定檔**

    ```bash
    poetry init
    ```

    須要回答一些關於專案設定的問題，回答完後，專案跟目錄會出現一個叫 **pyproject.toml** 的檔案，這個檔案可以用來管理套件的版本、紀錄專案的基本資訊，甚至是定義常用的 scripts，角色就像是 [[npm]] 中的 package.json。

### 不在全域先安裝 Poetry 的方法

- **Step1: 使用 venv 建立一個虛擬環境**

    ```bash
    python -m venv .venv
    ```

    這裡假設是要建立一個 in-project 的虛擬環境，因此是在專案跟目錄下執行指令。

- **Step2: 進入虛擬環境**

    ```bash
    source .venv/bin/activate
    ```

- **Step3: 更新虛擬環境中的 pip 與 setuptool**

    ```bash
    pip install -U pip setuptools
    ```

- **Step4: 安裝 Poetry**

    ```bash
    pip install poetry
    ```

- **(Optional) Step5: 設定 In-Project Virtual Environment**

    ```bash
    poetry config virtualenvs.in-project true --local
    ```

- **Step6: 初始化 Poetry 設定檔**

    ```bash
    poetry init
    ```

### 刪除虛擬環境

直接刪除整包代表虛擬環境的資料夾即可刪除虛擬環境。

# 進出虛擬環境

### 進入虛擬環境

當直接使用 venv + pip 進行虛擬環境的套件管理時，須使用 `source <VENV_PATH>/bin/activate` 來進入虛擬環境，但如果 global 也安裝 Poetry 後，可以改用：

```bash
poetry shell
```

>[!Info]
>可以使用 `which python` 來確認現在使用的 Python 環境是否為虛擬環境。

### 離開虛擬環境

- 用 `deactivate` 離開 shell session 但不關閉 terminal
- 用 `exit` 離開 shell session 並關閉 terminal

### 取得虛擬環境資料夾的位置

```bash
poetry env info --path
```

這個指令可以用在開啟虛擬環境時：

```bash
source $(poetry env info --path)/bin/activate
```

# 使用 Poetry 安裝與移除套件

### 根據 poetry.lock 或 pyproject.toml 安裝套件

如果是一個本來就使用 Poetry 作為虛擬環境與套件管理工具的專案，那麼它的 poetry.lock 與 pyproject.toml 中通常已經寫了一些專案會用到的套件 & 版本了，此時我們可以透過以下指令快速安裝所有套件與他們的 sub-dependencies：

```bash
poetry install
```

- 如果 poetry.lock 與 pyproject.toml 都存在，則會根據 poetry.lock 的內容來安裝套件。
- 如果只有 pyproject.toml，則會根據 pyproject.toml 的內容來安裝套件，此時 sub-dependencies 的「最新可用版本」會即時被運算出來然後安裝，最後會將所有安裝的套件與它們的版本寫進 poetry.lock 中。
- 如果只有 poetry.lock，那指令就會報錯。

### 安裝單一套件

```bash
poetry add <PACKAGE_NAME>

# or if you want to specify the version number
poetry add <PACKAGE_NAME>@<VERSION>
```

執行 `poetry add` 時，Poetry 會先檢查所有列在 pyproject.toml 中的套件是否都已安裝，若沒有的話會先安裝缺少的套件，都安裝完了才會安裝目前這個指令要安裝的套件。

如果要安裝的套件已存在但版本不一樣，那這個指令就是在升級該套件的版本；如果已存在的套件版本與要安裝的一樣，那就什麼事都不會發生。

### 升級所有 Sub-Dependencies 至「最新可用版本」

```bash
poetry update
```

這個指令的效果等同於先將 poetry.lock 刪除，再執行 `poetry install`。

### 移除套件

```bash
poetry remove <PACKAGE_NAME>
```

# Dependency Group

大部分套件管理工具都有提供將套件分為 "default" 與 "dev" 兩類的功能，而 Poetry 與其它套件管理工具最大的不同，就是使用者可以自定義各種 groups 給要安裝的套件，不限於 default 與 dev。

安裝套件時如果要為它分類，指令如下：

```bash
poetry add <PACKAGE_NAME> --group <GROUP_NAME>
```

- group 的名稱是自訂的。
- 如果沒有特別聲明 group 的話，套件預設是屬於 `main` group。
- 對應到 pyproject.toml 中的結構如下：（假設有一個 group 叫做 `dev`）

    ```toml
    [tool.poetry.group.dev.dependencies]
    pytest = "^6.0.0"
    pytest-mock = "*"
    ```

    `main` group 的開頭是 `[tool.poetry.dependencies]`

### 只安裝特定 Group 中的套件

執行 `poetry install` 時可以加上 `--only <GROUP_NAME>`，這樣就只會安裝指定 group 中的套件，比如：

```bash
poetry install --only main
```

### Optional Group

在 pyproject.toml 的指定 group 底下可以將 group 設定為 optional group：

```toml
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "*"
```

optional group 中的套件不會在執行單純的 `poetry install` 時被安裝，須要額外使用 `--with` 才能安裝它們，比如：

```bash
poetry install --with docs
```

`--with` 後可以用 `,` 連接多個套件，比如 `poetry install --with docs,dev,test`。

# Poetry Configuration

- 全域設定檔
    - MacOS：~/Library/Application Support/pypoetry/config.toml
- Local 設定檔：`PROJECT_PATH`/poetry.toml

上面的兩個設定檔是設定 Poetry 要如何運作的檔案，與設定 dependencies 的檔案 (`pyproject.toml`) 是分開的。

更改設定的方式：

- 直接改設定檔的內容
- 使用指令 `poetry config`

詳見[官方文件](https://python-poetry.org/docs/configuration/)。

# 參考資料

- [官方網站](https://python-poetry.org/)
- [GitHub Repo](https://github.com/python-poetry/poetry)
