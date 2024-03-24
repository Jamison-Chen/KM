#WebDevPractice

# 安裝

### On MacOS

```bash
brew install vegeta
```

>[!Note]
>執行這個指令時，若出現 `command not found: brew`，代表你的電腦中沒有沒有 Homebrew，此時你須要先[[Homebrew#安裝|安裝 Homebrew]]。

# 示範

```bash
echo "GET http://localhost/" | vegeta attack -duration=5s | tee results.bin | vegeta report
vegeta report -type=json results.bin > metrics.json
cat results.bin | vegeta plot > plot.html
cat results.bin | vegeta report -type="hist[0,100ms,200ms,300ms]"
```

# 參考資料

- <https://github.com/tsenart/vegeta>
