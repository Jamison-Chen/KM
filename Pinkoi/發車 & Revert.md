# 發車

通過 Code Review (LGTM) 後，就可以進入 Deploy 的流程了，步驟如下：

### Step1: 最終測試

在自己的 branch 上測試，至少此次改動的範圍以及購物流程要 OK。

### Step2: Merge

在 GitHub 上的 pull request 頁面把 feature branch merge 進 `dev` branch。

### Step3

```bash
git checkout dev
```

### Step4

```bash
git pull origin dev
```

### Step5: 發車

```bash
git push origin dev:master
```

> [!Note]
> 可以將 Step3~Step5 結合成一個指令：
> ```bash
>git checkout dev && git pull -v --no-edit origin dev master && git push -v origin dev && git push -v origin dev:master
>```

完成上述五步驟後，就會觸發 GitHub 上的 CI，可以在 GitHub Actions 以及 Slack 的 `koi-bus` Channel 裡看到 CI 進度。

# Revert Commit

[文件](https://sites.google.com/pinkoi.com/epd-wiki/home/dev-guide/for-all-engineers/%E9%96%8B%E7%99%BC%E6%B5%81%E7%A8%8B/revert-deployment-pinkoi-repo)
