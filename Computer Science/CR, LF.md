在古早的打字機時代，要換到新的一行繼續書入文字，就必須做兩個動作：「回到一行的開頭」以及「往下推進一行」。CR (Carriage Return) 與 LF (Line Feed) 就分別代表這兩個動作。

對現今的電腦而言，CR 與 LF 是兩種不同的換行符號，在 [ASCII table](</Computer Science/Character Encoding & Decoding.md#ASCII Table>) 裡，CR 是編號第 13 號；LF 是編號第 10 號，兩者都屬於 control characters；在程式語言中則是使用 [escape character](</Programming Language/String.md#Escape Character（跳脫字元）>) 中的 `"\n"` 表示 LF、`"\r"` 表示 CR。

Unix 作業系統（包括 Linux 與 MacOS）是使用 `"\n"` 來換行，但在 Windows 作業系統是使用 `"\r\n"` 來換行，所以在 Windows 系統中打開 Unix 系統產生的檔案，會全部變成同一行。

> [!Note]
> 舊版 MacOS (pre-OS X MacIntosh) 是使用 `"\r"` 來換行，所以也會出現相容性問題。

# 參考資料

- <http://violin-tao.blogspot.com/2016/05/crlflf-bug.html>
- <https://en.wikipedia.org/wiki/Newline>
