# Installation

pip 是 Python 原生的套件管理工具，會在使用者安裝 Python 時一起被安裝。

# 查詢 pip 版本

```bash
pip --version
```

### 目前使用的 Python Interpreter 所使用的 pip 版本

```bash
python -m pip --version
```

>[!Note]
>我們可能會在 host 的不同地方裝上不同的 Python interpreter，有時候是因為需要不同版本的 interpreter，有時後是因為不同專案要有不同的環境。若想要確保你下的指令會是對目前所使用的 Python interpreter 進行操作，就可以加上 `python -m`。

# 將 pip 更新至最新版本

```bash
pip install --upgrade pip
# or
pip install -U pip
```

這個動作可以在每次要用到 pip 來安裝套件前都先做一次。

# 安裝套件

```bash
pip install {PACKAGE}[=={VERSION}] [...]
```

e.g.

```bash
pip install Django==4.2
```

- 可以一次安裝多個 packages，使用空格分隔
- 沒有特別寫 `{VERSION}` 的話就是更新到最新版本

### 使用 requirements.txt 一次安裝所有套件

我們先看看一個 requirements.txt 範例：

```plaintext
# Requirements without Version Specifiers
nose

# Requirements with Version Specifiers
docopt == 0.6.1             # Version Matching. Must be version 0.6.1
keyring >= 4.1.1            # Minimum version 4.1.1
coverage != 3.5             # Version Exclusion. Anything except version 3.5
Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
```

我們可以先將所有想安裝的套件及它們的版本寫在 requirements.txt 裡，然後使用下方指令一次將全部的套件安裝：

```bash
pip install -r requirements.txt
```

# 更新套件

```bash
pip install --upgrade {PACKAGE}[=={VERSION}]
# or
pip install -U {PACKAGE}[=={VERSION}]
```

沒有特別寫 `{VERSION}` 的話就是更新到最新版本。

# 解除安裝套件

```bash
pip uninstall {PACKAGE}
```

# 列出已安裝的套件

### `pip list` 列出「所有」已安裝的套件

Example output:

```plaintext
Package          Version
---------------- ---------
certifi          2022.12.7
distlib          0.3.6
filelock         3.10.0
pip              23.0.1
platformdirs     3.1.1
setuptools       67.6.1
virtualenv       20.21.0
virtualenv-clone 0.5.7
wheel            0.40.0
```

### `pip freeze` 列出所有「透過 pip 安裝」的套件

Example output:

```plaintext
certifi==2022.12.7
distlib==0.3.6
filelock==3.10.0
platformdirs==3.1.1
virtualenv==20.21.0
virtualenv-clone==0.5.7
```

你會發現這個輸出值的格式就是 `requirements.txt` 的格式，因此其實 `pip freeze` 可以拿來生成 `requirements.txt`：

```bash
pip freeze > requirements.txt
```

# Mannual

```bash
pip help
# or
pip install --help
```

# pip 的缺點

### 無法解決 Sub-Dependencies 的版本衝突

假設某專案會使用到 A、B 兩個套件，而這兩個套件內都會使用到 C 套件 (sub-dependency)，但 A 使用的是 v1.0 的 C；B 使用的是 v2.0 的 C，理論上如果要讓這個專案順利運作的話，v1.0 與 v2.0 的 C 應該要同時存在，才能同時滿足 A、B 的要求讓它們順利運作。

但若你使用的是 pip，且先安裝 A 再安裝 B，則 pip 會在安裝 B 時，將 C 的版本從 v1.0 升到 v2.0，進而導致 A 有可能壞掉。

### 沒有 Lock File

不像在 JavaScript 生態系中的 [npm](</Programming Language/JavaScript/Node.js/npm.md>) 有 package.lock.json 紀錄所有套件與 sub-dependencies 的精確版號，pip 中並沒有這樣的檔案，因此只能在 requirements.txt（對應到 npm 的 package.json）中寫清楚版號（但即使如此還是沒辦法解決 sub-dependencies 版本的問題）。

### 無法將套件分類

有些套件是只有在開發環境會用到的，比如 formatter、跑測試用的套件等，既然在正式環境中用不到，我們通常會希望這些套件就不要再正式環境中被下載。在其它套件管理工具中，通常至少都會支援將某些套件標記為 dev-only，並且可以在 `install` 指令中用 option 來決定是否標記 dev-only、是否安裝 dev-only 的套件，但 pip 並沒有這個功能，只要是寫在 requirements.txt 裡的套件就會被安裝；匯出 requirements.txt 時，也只能將所有套件匯出。

# 替代方案

針對上述 pip 的缺點，其實已經有其它工具解決了，包括 [[Pipenv - 虛擬環境與套件管理工具|Pipenv]] 以及 [[Poetry - 虛擬環境與套件管理工具|Poetry]]。

# 參考資料

- <https://note.nkmk.me/en/python-pip-usage/>
- <https://note.nkmk.me/en/python-pip-install-requirements/>
