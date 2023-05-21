> [!Info]
> 本篇及後續篇章中，若沒有特別說明，則皆是在 MacOS 中操作，且會以 CLI 為主。

# 安裝 Git

### 法一：安裝 Xcode

在 MacOS 中，可以直接安裝 Xcode，因為 Xcode 裡就包含了 Git：

```bash
xcode-select --install
```

或者可以直接輸入以下指令查詢 Git 的版本：

```bash
git --version
# or
git -v
```

若系統發現 Git 還沒被安裝，就會跳出詢問是否安裝 Xcode 的對話，輸入 `yes` 即開始安裝 Xcode。

### 法二：使用 Homebrew

使用這個方法的前提是你的 MacOS 內要已經安裝 [[Homebrew]]：

```bash
brew install git
```

### 法三：從官方網站下載

至 <https://git-scm.com/download/mac> 透過網頁下載。

# 設定 Git

|層級|位置|檔名|Memo|
|---|---|---|---|
|**System**|`/etc`|`gitconfig`|需要 root 權限才能修改這個設定檔|
|**Global**|`~`|`.gitconfig`||
|**Local**|`<PATH_TO_REPO>/.git`|`config`||

總共有三種層級的設定檔，層級由高到低分別為 **system**, **global** 與 **local**，預設的情況下，若不同層級的設定檔對同一個參數有不同的設定，則會採取較低層級的設定。比如在 global 設定 alias `st` 代表 `status`，在專案 A 的 local 設定 alias `st` 代表 `stash`，則在專案 A 中使用 `git st` 時，預設會觸發的是 `git stash`。 

使用 CLI 新增、修改或刪除設定時，須依照欲設定的層級在指令後方加上 `--system` 或 `--global` 或 `--local`。

### 設定 Username 與 Email

使用 `git config` 進行設定：

```bash
# Set username
git config --global user.name "John Doe"

# Set email
git config --global user.email johndoe@example.com
```

從上方指令中，我們可以看出來現在要設定的是 global 層級的設定檔，在終端機輸入上面這兩行指令後，你會看到 `~/.config` 多了下面這些內容：

```plaintext
[user]
	name = John Doe
	email = johndoe@example.com
```

### 設定編輯器

Git 有時後需要使用者進行必較複雜的操作時會需要使用到文字編輯器，下面這段指令將 Git 使用的編輯器設為 Visual Studio Code：

```bash
git config --global core.editor "code --wait"
```

其中 `--wait` 讓 Git 在 VS Code 完整開啟後才繼續動作。

### 查看所有設定

使用以下指令可以一次查看所有設定，同時列出每個設定所來自的設定檔，及該設定檔的位置，藉此我們可以知道每個設定所屬的層級：

```bash
git config --list --show-origin
```

### 查看單一設定

```bash
git config user.name
```

# 查看指令教學文件

```bash
git <VERB> --help
# or
git <VERB> -h
# or
git help <VERB>
# or
man git-<VERB>
```