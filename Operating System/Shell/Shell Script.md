### 在 Shell 中執行 Shell Script File

執行 shell script file 的指令有 `sh` 與 `source` 兩種：

- `sh`

    ```sh
    sh <FILE>
    ```

    若使用 `sh` 執行 shell script file，則會在當前的 shell session 中==另開一個 sub-shell==來執行，因此 file 中對於 shell 環境的更動不會影響到當前的 shell。

- `source`

    ```sh
    source <FILE>
    ```

    若使用 `source` 執行 shell script file，則會在當前的 shell session 中直接執行，因此 file 中對於 shell 環境的更動會影響到當前的 shell。

    可以把 `source` 當成其它語言中的 `import`，可以在一個 shell script file 中 `source` 另一個 shell script file 來載入變數或函式。
