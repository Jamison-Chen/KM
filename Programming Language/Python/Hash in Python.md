>[!Note]
>本文的內容假設你對 [[Hash Function、Hash Table.canvas|Hash Function、Hash Table]] 已有基本的認知。

# Built-In hash Function

```Python
hash("hello")
```

- `hash` 會觸發被傳入的物件的 `__hash__` method，所以在定義 class 時可以自己定義該 class 的 `__hash__` method（一定要回傳 integer）
- 為了避免 hash collision attacks，Python 3.3 及以後的版本在每次啟動 Python interpreter 時都會使用新的、隨機產生的 hash seed，所以不同的 interpreter instance 對同一個值做 `hash` 會得到不同的值
    - 這個特性使得 `hash` 絕對不適合拿來當作資料驗證用的 hash function
- 針對原生的 immutable data，Python 底層是使用 [SipHash](https://en.wikipedia.org/wiki/SipHash) 計算它們的 hash value
    - Python 原本底層使用的 hash function 是 [Fowler-Noll-Vo (FNV) hash function](https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function) 的一種變體，直到 Python 3.4 後才為了要進一步避免 hash collision attacks 而改用 SipHash
- `hash` 的優點是計算速度很快，所以被用在 set 與 dictionary 中
# The hashlib Library

```Python
import hashlib

text = "hello"
h = hashlib.md5(text.encode())
print(h.hexdigest())  # 5d41402abc4b2a76b9719d911017c592
```

# Python 如何處理 Hash Collision？

當 dictionary 中的 key 或 set 中的元素發生 hash collision 時， Python 採用的是 **open addressing** 的方式找到下一個可以放 key/element 的位置。

# 參考資料

- <https://peps.python.org/pep-0456/>
- <https://kinsta.com/blog/python-hashing/>
