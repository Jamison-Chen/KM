# 各種語言中的 String 是否為 Immutable

「是否為 Immutable」與「是否為 Constant」是兩件不同的事情。前者表示的是一塊已經儲存著某些值的記憶體可不可以被修改內容；後者指的則是一個已經被指派值的變數可不可以再次被指派一個值。

### Immutable

Java、C#、JavaScript、Python、Go

舉例而言，若在 Python 中執行以下程式碼：

```Python
s = "abcd"
s[0] = "e"
```

則你會看到以下錯誤訊息：

```plaintext
TypeError: 'str' object does not support item assignment
```

### Mutable

Ruby、PHP、C++

### 其他

- 在 C 語言中並沒有 string objects，只能用向量 `char *` 來表示，而向量是 mutable 的。

- In both C and C++, string constants (declared with the *const qualifier*) are immutable, but you can easily "cast away" the const qualifier, so the immutability is weakly enforced.
