# 語言定位

- Static language
- Strongly-typed language
- Compiled language

# 特色

- Garbage collection
- Goroutine
- 語法簡潔

# Installation

[官方文件](https://go.dev/doc/install)

### On Mac

- Step1: 至官網下載安裝程式
- Step2: 執行安裝程式
- Step3: 將 Go 的路徑 (/usr/local/go/bin) 加入 `PATH` 環境變數

Done!

# Create Your First Module

```bash
mkdir go_tutorial  # this is the root directory of your module
cd go_tutorial
go mod init <MODULE_LOCATION>
```

執行完 `go mod init <MODULE_LOCATION>` 指令後，專案根目錄會出現一個叫 go.mod 的檔案。指令中的 `<MODULE_LOCATION>` 是

#TODO 

# 核心概念：Module & Package

Module 在 Go 的定義，與在 Python、JavaScript 等其它程式語言不同，在 Go 的世界中，一整個專案就是一個 module，module 底下包含若干個 packages 或 .go 檔，package 底下也會有若干個 .go 檔。

一個簡單的 Go module 結構如下圖：

```plaintext
module
├── go.mod
├── package1
│   ├── hello.go
│   └── world.go
├── package2
│   └── helloagain.go
└── main.go
```
