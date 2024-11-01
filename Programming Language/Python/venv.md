venv 是 Python 原生用來建立虛擬環境 (virtual environment) 的 module。

# Python 虛擬環境

使用虛擬環境開發專案的好處主要有二：

1. 一個人維護多個專案時，各專案所需的環境不同，此時利用虛擬環境可以達到「隔離」的效果
2. 多個人維護一個專案時，須確保所有人的開發環境相同，並且希望新加入的人可以快速建置出相同的環境，此時虛擬環境的設定檔可達到「快速複製環境」的效果

所謂的「環境」包括：

1. 用來執行專案的 Python Interpreter 的版本
2. 專案所用到的套件的版本
3. 與 2. 所相依的套件的版本

# Create a Virtual Environment

在專案根目錄執行下方指令：

```bash
python -m venv <NAME>
```

執行後，專案跟目錄中就會出現一個名字為 `<NAME>` 的資料夾，這整個資料夾就代表一個虛擬環境。`<NAME>` 資料夾中會有下列東西：

- `pyvenv.cfg`：設定檔
- `bin/`：裡面有用來啟動虛擬環境的 script (`activate`)、指向 global Python interpreter 的 softlink
- `lib/`：裡面放安裝在這個虛擬環境中的套件
- `include/`：不重要

>[!Note]
>由於虛擬環境是基於 global Python interpreter 建立的，所以虛擬環境所使用的 Python interpreter 版本會跟 global 的一樣，比如若 global 使用 Python 3.12，那建立出來的虛擬環境也會是 Python 3.12。
>
>若想要在 global 可以有多種不同版本的 Python interpreter 相互切換，須使用 [pyenv](</Programming Language/Python/pyenv.md>)。

# Activate Virtual Environment

在已經建立好虛擬環境的專案跟目錄中執行下方指令：

```bash
source <NAME>/bin/activate
```

- 指令中的 `<NAME>` 是當初建立虛擬環境時所用的名稱，也就是代表虛擬環境的資料夾的名稱。
- 進入虛擬環境後，terminal 的命令列開頭會多出 `(<NAME>)` 這串字。

進入虛擬環境後，使用的 `pip` 指令就會是虛擬環境中的 pip，指令所操作 (CRUD) 的套件也是虛擬環境中的。

由於進入虛擬環境後也是使用 pip 來操作套件，所以關於 pip 的使用方法這邊就不細數，詳情請看[這篇](</Programming Language/Python/pip - 套件管理工具.md>)。

# Deactivate Virtual Environment

在專案跟目錄中執行下方指令：

```bash
deactivate
```

# venv 的缺點

由於 venv 建立的虛擬環境中是使用 pip 來管理套件，所以這樣的虛擬環境就繼承了 pip 本身的缺點：無法對 dependencies 的版本進行精確的管理（詳見[本文](</Programming Language/Python/pip - 套件管理工具.md#pip 的缺點>)）。

市面上有其它解決這個痛點的替代品，最常見的有 [Pipenv](</Programming Language/Python/Pipenv - 虛擬環境與套件管理工具.md>) 與 [Poetry](</Programming Language/Python/Poetry - 虛擬環境與套件管理工具.md>)。

# 虛擬環境放在哪裡比較好？

只要執行專案程式前有先 activate 虛擬環境就可以讓專案順利運作了，所以其實虛擬環境資料夾所放置的位置其實並不一定要放在專案的跟目錄，目前有兩種主流的做法：

- **In-Project**：每個專案的虛擬環境都放在專案自己的跟目錄中
    - 通常虛擬環境的資料夾會叫做 venv 或 .venv
    - 通常不會將虛擬環境納入版控
- **Out-of-Project**：將每個專案的虛擬環境集中在 host 的某個地方管理
    - 以 MacOS 為例，通常會將所有虛擬環境資料夾放在 ~/.local/share/virtualenvs 底下

# 參考資料

- [官方文件](https://docs.python.org/3/library/venv.html)
