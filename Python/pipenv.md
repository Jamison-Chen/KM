pipenv 是一個結合「虛擬環境」以及「套件管理」的開發工具，同時也是 pip 官方推薦的套件管理工具之一。

使用虛擬環境開發專案的好處主要有二：

1. 一個人維護多個專案時，各專案所需的環境不同，此時利用虛擬環境可以達到「隔離」的效果
2. 多個人維護一個專案時，須確保所有人的開發環境相同，並且希望新加入的人可以快速建置出相同的環境，此時虛擬環境的設定檔可達到「快速複製環境」的效果

所謂的「環境」包括：

1. 用來執行專案的 Python Interpreter 的版本
2. 專案所用到的第三方套件的版本
3. 與 2. 所相依的套件的版本

# 安裝 pipenv

建議將 pipenv 全域安裝，這樣這台電腦的所有地方都可以使用 pipenv。通常我們會使用 pip 安裝 pipenv：

```bash
pip install pipenv
```

其實安裝 pipenv 的方法有很多，例如也可以使用 brew 或 apt-get，此處略。

### 確認 pipenv 的版本

```bash
pipenv --version
```

# 為專案建置虛擬環境

### Step1: Initialize

切換至專案根目錄後，輸入以下指令：

```bash
pipenv --python <VERSION>
```

比如我現在想要一個裝有 Python 3.11.2 的虛擬環境：

```bash
pipenv --python 3.11.2
```

此時會發生兩件事：

1. 在目前的 directory 下產生一個名為 `Pipfile` 的檔案

    以 toml 格式呈現，關於 `Pipfile` 的內容，詳見 [[#深入了解 Pipfile|此段]]。

2. 在電腦中的「某個位置」產生對應的虛擬環境資料夾

    在 `Pipfile` 所在的 directory 中透過下方指令，可以查詢目前專案的虛擬環境資料夾的位置：

    ```bash
    pipenv --venv
    ```

    在 MacOS 中， `~/.local/share/virtualenvs` 是管理所有 pipenv 虛擬環境的地方。

注意，由於虛擬環境內的 Python 是基於實體全域環境中的 Python 所建立的，所以你指定的 `<VERSION>` 必須跟全域安裝的 Python version 一致。

> [!Info]
> 如果實體環境有安裝 [[pyenv]]，則在建立虛擬環境的時候，若目前 global 環境中沒有指定 `<VERSION>` 的 Python Interpreter，CLI 會問你要不要先使用 pyenv 全域安裝。

### Step2: Install

在專案根目錄執行以下指令，安裝 `Pipfile` 中所指定版本的 Python，以及其他基本的套件：

```bash
pipenv install
```

完成後你會發現專案根目錄中多了一個叫做 `Pipfile.lock` 的檔案，關於 `Pipfile` 與 `Pipfile.lock` 的差異，請見 [[#Pipfile 與 Pipfile.lcok|此段]]。

# 進出虛擬環境

### 開啟虛擬環境中的 shell

若要使用 terminal 進入某個 pipenv 虛擬環境，則須在 `~/.local/share/virtualenv` 底下找到指定之虛擬環境 directory 中的 `./bin/activate` 這個檔案，因此若  terminal 已位在專案跟目錄（即 `Pipfile` 所在之目錄），那就可以結合前面介紹的「查詢虛擬環境資料夾路徑」的指令來進入這個專案專用的虛擬環境：

```bash
source $(pipenv --venv)/bin/activate
```

其實 pipenv 很貼心地幫我們把上面這個指令包裝成了更簡潔的樣子：

```bash
pipenv shell
```

進入虛擬環境的 shell 後，使用 `python --version` 查到的就會虛擬環境的 Python 版本了！

### 離開虛擬環境中的 shell

- 用 `deactivate` 離開環境但不關閉 terminal
- 用 `exit` 離開環境並關閉 terminal

### 進入虛擬環境的 Python 互動介面

```bash
pipenv run python
```

使用 `exit()` 離開 Python 互動介面。

### 使用虛擬環境執行某個 `.py` 檔

```bash
pipenv run XXX.py
```

# 使用 pipenv 安裝套件

### 安裝正式環境會用到的套件

以此方法安裝的 packages 會被列舉在 `Pipfile` 中的 `[packages]` 底下：

```bash
# 安裝指定版本
pipenv install <PACKAGE_NAME>==<VERSION>

# 安裝預設版本
pipenv install <PACKAGE_NAME>
```

### 使用 `-d` 安裝於開發環境

以此方法安裝的 packages 會被列舉在 `Pipfile` 中的 `[dev-packages]` 底下：

```bash
pipenv install <PACKAGE_NAME> -d
```

### 移除套件

```bash
pipenv uninstall <PACKAGE_NAME>
```

### 安裝套件時發生了哪些事

安裝套件時皆會依序發生以下三件事：

1. 找到本專案所屬的 `virtualenv` directory 的位置
2. 檢查有沒有 `Pipfile` 有聲明但不存在於虛擬環境的套件，若有則將它們下載並安裝
3. 安裝本次指定的套件至虛擬環境
4. 在 `Pipfile` 中的 `[packages]` 或 `[dev-packages]` 底下添加套件名稱以及版本
5. 在 `Pipfile.lock` 檔案中添加套件及 dependencies

> [!Note] 記得刪掉誤裝的套件
> 由於上一段中 2. 的存在，因此若不小心執行 `pipenv install <不存在的套件名稱>`，要記得馬上執行 `pipenv uninstall <不存在的套件名稱>` 來移除套件，或者直接用文字編輯器打開 `Pipfile` 找到該錯誤名稱並將其刪除，否則下次安裝其他套件時一樣會跳出 error。

# `Pipfile` 與 `Pipfile.lcok`

`Pipfile` 只負責控制「明確指定要用到的套件」的版本，但其內所描述的套件版本可以是模糊的，比如若執行 `pipenv install <PACEAGE_NAME>` 時沒有聲明要安裝的套件版本，該套件在 `Pipfile` 中就會以 `<PACEAGE_NAME> = "*"` 呈現。

我們都知道，其實大多數第三方套件內部都會用到其他套件，我們統稱這些「套件用到的套件」為 **Dependencies**， `Pipfile.lock` 就是負責控制「明確指定要用到的套件」以及「它們的 Dependencies」的版本，且所有套件都有明確的版本號碼。

`Pipfile.lock` 還負責控制下載套件的來源，並且會根據套件內容計算出 hash value，這可以避免開發者下載到惡意來源的套件。

### 深入了解 `Pipfile`

`Pipfile` 以 toml 格式撰寫，當[[#Step1 Initialize|初始化虛擬環境]]時（`pipenv --python <VERSION>`）就會被自動建立，新建立的 `Pipfle` 內容如下：

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]

[dev-packages]

[requires]
python_version = "3.11.2"
```

你可以發現 `[requires]` 中的 `python_version` 就是 `pipenv --python <VERSION>` 所指定的版本，若要更改為其他版本的 Python（前提是你的電腦裡要有該版本），則直接改這裡然後重新執行一次 `pipenv install` 即可。

### 根據 `Pipfile` 建立或更新 `Pipfile.lock`

```bash
pipenv lock
```

若 `Pipfile` 中有未明確聲明版本的套件，那就使用 `latest` 版本。

### 完全根據 `Pipfile.lock` 建置環境

```bash
pipenv install --ignore-pipfile
```

其實沒有加 `--ignore-pipfile` 的版本 (`pipenv install`)，就是 `pipenv lock` + `pipenv install --ignore-pipfile`。也就是說若 `Pipfile` 中有未明確聲明版本的套件，那該套件實際被 install 的就會是 `latest` 版本，且若這個 `latest` 版本與 `Pipfile.lock` 原本記錄不同，那 `Pipfile.lock` 就也會一併被更新。

在某些情境下「自動使用最新套件」這個特性是不被期待的，比如我們通常會希望一個產品的正式環境的套件版本與 dependencies 與開發環境（已經被驗證過沒問題）是完全相同的，這時候就要仰賴 `Pipfile.lock` 「有詳實紀錄每個套件的版本」這個特色，來確保「無論何時何地，都可以建置出相同的環境」。

# 刪除虛擬環境

當專案開發完畢或者長期不會用到時，代表它所使的虛擬環境也不會用到了，此時可以放心的刪除該虛擬環境，下次要用到時再重新建起來就可以了。

### 刪除

在專案根目錄（也就是 `Pipfile` 所在的 directory）輸入以下指令來刪除虛擬環境：

```bash
pipenv --rm
```

此時 `~/.local/share/virtualenvs` 底下的對應的虛擬環境資料夾就會被刪除，但專案中的 `Pipfile` 以及 `Pipfile.lock` 都會留著（必須留著）。

當然你也可以手動找到電腦中 `~/.local/share/virtualenvs` 底下的對應的虛擬環境資料夾，然後手動刪除它，比較麻煩而已。

### 重建

```bash
pipenv install --dev
```

其實你可以想像重建就等同於是一個新的成員加入開發團隊，在他的電腦架設開發環境的過程。

# 其它常見操作

### 根據 `Pipfile.lock` 建立 `requirements.txt`

由於 pip 只認得 `.txt` 檔案（`pip install -r requirements.txt`），因此有時候（尤其是在正式環境中）我們還是需要準備一份 `requirements.txt`，此時可以用 pipenv 提供的指令來完成，還可以指定生成的檔案的名稱：

```bash
pipenv requirements > requirements.txt
```

### 查詢指令

```bash
pipenv -h
```

# 其它

- 建議將 `Pipfile` 以及 `Pipfile.lcok` 都納入版控。

# 參考資料

- [官方文件](https://pipenv.pypa.io/en/latest)