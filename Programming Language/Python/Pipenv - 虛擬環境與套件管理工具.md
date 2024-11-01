>[!Note]
>關於什麼是 Python 虛擬環境以及使用虛擬環境的好處，請看[這裡](</Programming Language/Python/venv.md#Python 虛擬環境>)。

# 安裝 Pipenv

強烈建議將 Pipenv 全域安裝，這樣這台電腦的所有地方都可以使用 Pipenv。

通常會使用 pip 安裝 Pipenv：

```bash
pip install pipenv
```

其實安裝 Pipenv 的方法有很多，例如也可以使用 `brew` 或 `apt-get`，此處略。

### 確認 Pipenv 的版本

```bash
pipenv --version
```

# 為既有專案建置虛擬環境

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

1. 在目前的目錄下產生一個名為 Pipfile 的檔案

    格式為 toml。關於 Pipfile 的內容，詳見 [此段](</./Programming Language/Python/Pipenv - 虛擬環境與套件管理工具.md#深入了解 Pipfile>)。

2. 在電腦中的「某個位置」產生對應的虛擬環境資料夾

    在 Pipfile 所在的目錄中可以透過下方指令查詢目前專案的虛擬環境資料夾的位置：

    ```bash
    pipenv --venv
    ```

    以 MacOS 為例，各虛擬環境會放在 `~/.local/share/virtualenvs`。

> [!Note]
> 由於虛擬環境內的 Python 是基於實體全域環境中的 Python 所建立的，所以 `pipenv --python <VERSION>` 的 `<VERSION>` 必須是全域安裝的那個 Python 版本。
> 
> 如果實體環境有安裝 [pyenv](</Programming Language/Python/pyenv.md>)，則在建立虛擬環境的時候，若目前 global 環境中沒有指定 `<VERSION>` 的 Python Interpreter，CLI 會問你要不要先使用 pyenv 全域安裝。

### Step2: Install

在專案根目錄執行以下指令，在虛擬環境中安裝 Pipfile 中所指定的 Python 版本，以及其它基本的套件：

```bash
pipenv install
```

完成後，專案根目錄中會多一個叫 Pipfile.lock 的檔案。

>[!Note]
>關於 Pipfile 與 Pipfile.lock 的差異，請見[此段](</./Programming Language/Python/Pipenv - 虛擬環境與套件管理工具.md#Pipfile 與 Pipfile.lcok>)。

# 進出虛擬環境

### 進入虛擬環境

若要使用 terminal 進入某個 Pipenv 虛擬環境，則須在 `~/.local/share/virtualenv` 底下找到指定的虛擬環境資料夾中的 `./bin/activate` 這個檔案，因此若  terminal 已位在專案根目錄（即 Pipfile 所在的目錄），那就可以結合前面介紹的「查詢虛擬環境資料夾路徑」的指令來進入這個專案專用的虛擬環境：

```bash
source $(pipenv --venv)/bin/activate
```

其實 Pipenv 很貼心地幫我們把上面這個指令包裝成了更簡潔的樣子：

```bash
pipenv shell
```

只是若要使用 `pipenv shell` 就必須在全域安裝 Pipenv。

進入虛擬環境的 shell 後，使用 `python --version` 查到的就會虛擬環境的 Python 版本了！

### 離開虛擬環境

- 用 `deactivate` 離開 shell session 但不關閉 terminal
- 用 `exit` 離開 shell session 並關閉 terminal

### 進入虛擬環境的 Python 互動介面

```bash
pipenv run python
```

使用 `exit()` 離開 Python 互動介面。

### 使用虛擬環境執行 Python 檔案

```bash
pipenv run XXX.py
```

# 使用 Pipenv 安裝與移除套件

### 安裝正式環境會用到的套件

以此方法安裝的 packages 會被列舉在 Pipfile 中的 `[packages]` 底下：

```bash
# 安裝指定版本
pipenv install <PACKAGE_NAME>==<VERSION>

# 安裝預設版本
pipenv install <PACKAGE_NAME>
```

### 使用 `-d` 安裝於開發環境

以此方法安裝的 packages 會被列舉在 Pipfile 中的 `[dev-packages]` 底下：

```bash
pipenv install <PACKAGE_NAME> -d
```

### 移除套件

```bash
pipenv uninstall <PACKAGE_NAME>
```

### 安裝套件時發生了哪些事

安裝套件時皆會依序發生以下三件事：

1. 找到本專案所屬的虛擬環境的資料夾要放的位置
2. 檢查有沒有 Pipfile 有聲明但不存在於虛擬環境的套件，若有則將它們下載並安裝
3. 安裝本次指定的套件至虛擬環境
4. 在 Pipfile 中的 `[packages]` 或 `[dev-packages]` 底下添加套件名稱以及版本
5. 在 Pipfile.lock 檔案中添加套件及 dependencies

> [!Note] 記得刪掉誤裝的套件
> 由於上一段中 2. 的存在，因此若不小心執行 `pipenv install <不存在的套件名稱>`，要記得馬上執行 `pipenv uninstall <不存在的套件名稱>` 來移除套件，或者直接用文字編輯器打開 Pipfile 找到該錯誤名稱並將其刪除，否則下次安裝其他套件時一樣會跳出 error。

# Pipfile 與 Pipfile.lcok

Pipfile 只負責控制「明確指定要用到的套件」的版本，但其內所描述的套件版本可以是模糊的，比如若執行 `pipenv install <PACEAGE_NAME>` 時沒有聲明要安裝的套件版本，該套件在 Pipfile 中就會以 `<PACEAGE_NAME> = "*"` 呈現。

我們都知道，其實大多數第三方套件內部都會用到其他套件，我們統稱這些「套件用到的套件」為 **Dependencies**， Pipfile.lock 就是負責控制「明確指定要用到的套件」以及「它們的 Dependencies」的版本，且所有套件都有明確的版本號碼。

Pipfile.lock 還負責控制下載套件的來源，並且會根據套件內容計算出 hash value，這可以避免開發者下載到惡意來源的套件。

### 深入了解 Pipfile

Pipfile 以 toml 格式撰寫，當[初始化虛擬環境](</./Programming Language/Python/Pipenv - 虛擬環境與套件管理工具.md#Step1 Initialize>)時（`pipenv --python <VERSION>`）就會被自動建立，新建立的 `Pipfle` 內容如下：

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

其中 `[requires]` 中的 `python_version` 就是 `pipenv --python <VERSION>` 所指定的 `<VERSION>`，若要更改為其他版本的 Python（前提是你的電腦裡要有該版本），則直接改 `python_version` 然後重新執行一次 `pipenv install` 即可。

### 根據 Pipfile 建立或更新 Pipfile.lock

```bash
pipenv lock
```

若 Pipfile 中有未明確聲明版本的套件，那就是使用 `latest` 版本。

### 完全根據 Pipfile.lock 建置環境

```bash
pipenv install --ignore-pipfile
```

其實若沒有加 `--ignore-pipfile` option，就是 `pipenv lock` + `pipenv install --ignore-pipfile`。也就是說，若沒有加 `--ignore-pipfile` option，且 Pipfile 中有未明確聲明版本的套件，那就會 install 該套件的 `latest` 版本，且若這個 `latest` 版本與 Pipfile.lock 原本記錄不同，那會先改 Pipfile.lock 中的版本，再 install。

在某些情境下，「自動使用最新版本」這個特性是不被期待的，比如我們通常會希望一個穩定在線上的產品在正式環境的套件版本、dependencies 要與開發環境是完全相同的（因為功能會在開發環境上驗證過沒問題），這時候就要仰賴 Pipfile.lock 「有詳實紀錄每個套件的版本」這個特色，來確保無論何時何地，都可以建置出相同的環境。

>[!Note]
>建議將 Pipfile 以及 `Pipfile.lcok` 都納入版控。

# 刪除虛擬環境

當專案開發完畢或者長期不會用到時，代表它所使的虛擬環境也不會用到了，此時可以放心的刪除該虛擬環境，下次要用到時再重新建起來就可以了。

### 刪除

在專案根目錄（也就是 Pipfile 所在的目錄）輸入以下指令來刪除虛擬環境：

```bash
pipenv --rm
```

此時 `~/.local/share/virtualenvs` 底下的對應的虛擬環境資料夾就會被刪除，但專案中的 Pipfile 以及 Pipfile.lock 都會留著（必須留著）。

當然你也可以手動找到電腦中 `~/.local/share/virtualenvs` 底下的對應的虛擬環境資料夾，然後手動刪除它，比較麻煩而已。

### 重建

```bash
pipenv install --dev
```

其實你可以想像重建就等同於是一個新的成員加入開發團隊，在他的電腦架設開發環境的過程。

# 其它常見操作

### 根據 Pipfile.lock 建立 requirements.txt

由於 pip 只認得 `.txt` 檔案（`pip install -r requirements.txt`），因此有時候（尤其是在正式環境中）我們還是需要準備一份 requirements.txt，此時可以用 Pipenv 提供的指令來完成，還可以指定生成的檔案的名稱：

```bash
pipenv requirements > requirements.txt
```

### 查詢指令

```bash
pipenv -h
```

# 其它替代工具

- [Poetry](</Programming Language/Python/Poetry - 虛擬環境與套件管理工具.md>)

# 參考資料

- [官方文件](https://pipenv.pypa.io/en/latest)
- [Github Repo](https://github.com/pypa/pipenv)
