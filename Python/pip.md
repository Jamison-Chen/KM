### 查詢目前安裝的 pip 版本

```bash
pip --version
```

### 顯示 pip 使用說明

```bash
pip help
# or
pip install --help
```

### 將 pip 更新至最新版本

```bash
pip install --upgrade pip
# or
pip install -U pip
```

這個動作可以在每次要用到 pip 來安裝套件前都先做一次。

### 安裝指定套件

```bash
pip install <package>[==<version>] [...]
```

e.g.

```bash
pip install django==4.2
```

可以一次安裝多個 packages，使用空格分隔。

### 使用 `requirements.txt` 一次安裝所有套件

我們先看看一個 `requirements.txt` 範例：

```plaintext
# Requirements without Version Specifiers
nose

# Requirements with Version Specifiers
docopt == 0.6.1             # Version Matching. Must be version 0.6.1
keyring >= 4.1.1            # Minimum version 4.1.1
coverage != 3.5             # Version Exclusion. Anything except version 3.5
Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
```

我們可以先將所有想安裝的套件及它們的版本寫在 `requirements.txt` 裡，然後使用下方指令一次將全部的套件安裝：

```bash
pip install -r requirements.txt
```

### 更新套件

```bash
pip install --upgrade <package>
```

### 解除安裝套件

```bash
pip uninstall <package>
```

### 列出已安裝的套件

- **`pip list` 列出「所有」已安裝的套件**

    Example Output:

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

- **`pip freeze` 列出所有「透過 pip 安裝」的套件**

    Example Output:

    ```plaintext
    certifi==2022.12.7
    distlib==0.3.6
    filelock==3.10.0
    platformdirs==3.1.1
    virtualenv==20.21.0
    virtualenv-clone==0.5.7
    ```

    你會發現這個 output 的格式就是 `requirements.txt` 的格式，因此其實 `pip freeze` 可以拿來生成 `requirements.txt`：

    ```bash
    pip freeze > requirements.txt
    ```

# 參考資料

- <https://note.nkmk.me/en/python-pip-usage/>
- <https://note.nkmk.me/en/python-pip-install-requirements/>
