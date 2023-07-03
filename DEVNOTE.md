# 如何維護此專案？

## `master` branch 與 `dev` branch

master branch 是給 Gitbook 的版本，因此：

- 會有 `SUMMARY.md` 檔案
- 所有圖片連結皆為標準 markdown 語法而非 obsidian 特有語法

---

## 編譯 SCSS

本專案採用 SCSS 編輯 Obsidian 編輯器的外觀，也就是說原則上開發者只會透過手動更改 `.scss` 檔案來更改外觀，且必須使用第三方套件將其編譯為 `.css` 檔，指令如下：

```bash
# 在 dev branch 的根目錄執行
npx sass ./.obsidian/snippets/custom.scss ./.obsidian/snippets/custom.css --no-source-map
```

---

## 準備 `SUMMARY.md`

>[!Info]
>這個動作只會在 master branch 做。

因為將新的版本推送至 GitHub 後就會觸發 GitBook 的更新，所以在推送前必須根據現在的文件結構更新 `SUMMARY.md` 並一起推送，指令如下：

```bash
python summary.py
```

---

## 將圖片連結從 Obsidian 特有語法轉換為 Markdown 標準語法

>[!Info]
>這個動作只會在 master branch 做。

```bash
python normalize_img_links.py
```
