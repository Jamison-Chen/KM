BOM 即 byte order mark，是一個 [[Character Encoding & Decoding#Unicode|Unicode]]，其值為 `U+FEFF`。

BOM 會（但不是一定會）出現在某些 text stream 的開頭，用來告訴讀取這段 text stream 的程式以下資訊：

- 在使用 16-bit 和 32-bit 為單位的 Unicode 編碼方式中，這段 text stream 的 [[Endianness.draft|endianness]]（又叫 byte order）
- 這段 text stream「很有可能」是使用 Unicode 編碼
- 這段 text stream 使用的是哪種 [[Character Encoding & Decoding#UTF|Unicode transformation format (UTF)]]

### 處理方式

以 Python 為例，若呼叫 `bytes` 物件的 `decode` function 時，傳入的 encoding function name 是 "utf-8"，則當 `bytes` 物件有 BOM 開頭時，BOM 會出現在 decode 的結果裡面：

```Python
# 當傳入 open 的 mode 為 "r" 時，預設就是使用 utf-8 來 decode bytes
with open("my_file.csv", "r") as file:
    dr = csv.DictReader(file)
    for line in dr:
        print(line)
```

Outputs:

```plaintext
{'\ufeffoffer': 'S2S_order', 'date_time': '2024-02-07 23:40:39', 'timetoaction': '00:08:39', 'transaction_id': '10285d78508f5ebfad9b9a0599fe68', 'cost': '31.702731', 'status': 'pending'}
{'\ufeffoffer': 'S2S_order', 'date_time': '2024-02-07 22:41:04', 'timetoaction': '00:04:18', 'transaction_id': '1020e4f50e9c3f0ae54bd9f10c0d01', 'cost': '1.534003', 'status': 'pending'}
```

理論上，上方 outputs 中每個 dictionary 的第一個 key 應該要是 `"offer"`，但現在都有一個 "\\ufeff" 在 "offer" 前面。這通常不會是我們想拿到的結果，在 Python 中，若要讀取檔案時忽略 BOM，則應該要==改用 "utf-8-sig" 來 decode `bytes` 物件==，方法如下：

```Python
# Approach 1: read in as bytes, decode using utf-8-sig
with open("my_file.csv", "rb") as file:
    dr = csv.DictReader(file.read().decode("utf-8-sig").splitlines())
    for line in dr:
        print(line)

# Approach 2: read in str, encode and than decode
with open("my_file.csv", "r") as file:
    dr = csv.DictReader(file.read().encode().decode("utf-8-sig").splitlines())
    for line in dr:
        print(line)
```

上面兩種方法的 outputs 會一樣：

```plaintext
{'offer': 'S2S_order', 'date_time': '2024-02-07 23:40:39', 'timetoaction': '00:08:39', 'transaction_id': '10285d78508f5ebfad9b9a0599fe68', 'cost': '31.702731', 'status': 'pending'}
{'offer': 'S2S_order', 'date_time': '2024-02-07 22:41:04', 'timetoaction': '00:04:18', 'transaction_id': '1020e4f50e9c3f0ae54bd9f10c0d01', 'cost': '1.534003', 'status': 'pending'}
```
