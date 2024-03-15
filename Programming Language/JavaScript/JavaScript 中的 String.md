#MemoryManagement 

# String vs String Object

#TODO 

# String 在多數程式語言中是 Non-Primitive，但在 JS 中是 Primitive

- 這裡說的 string 指的是用 `"..."` 這樣的的變數；`new String("...")` 這樣的語法建立的變數是 object，所以是 non-primitive
- 雖然說 string 在 JavaScript 被定義為 primitive type，但 string 的 value 並不像其他 primitive-type variables 一樣存在 call stack，而是存在 memory heap
- 雖說 string 變數的 value 存在 memory heap，但 string 變數並不像其他 non-primitive 變數一樣有自己專屬的 address，因為它們的 value 被放在 **string pool** 中
- String pool 是一個「strings 的集合」，這個 pool 裡不會出現相同值的 strings，每個唯一的值會有一個 address，這導致 string 有以下現象：
    1. 如果有兩個 string variables 的值一樣，則它們的 memory address 會是同一個
    2. 如果一個 string variable 的值發生改變，則它的 memory address 也會改變
    - 以上兩個特性與 primitive-type variable 一樣，這或許也是 string 在 JavaScript 中被歸類為 primitive 的原因

```JavaScript
const str1 = "Hello";
const str2 = "Hello";
const str3 = "Class";
```

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Pasted image 20240314120531.png>)

```JavaScript
let str1 = new String("John");
let str2 = new String("John");
let str3 = new String("Doe");
```

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/Pasted image 20240314120806.png>)

# 既然 `"abc"` 不是 object，為什麼還有 `"abc".length` 這種語法？

因為 JavaScript engine 執行到 `"abc".length` 時，實際上是先將 `"abc"` 轉換為一個 string object，再取 `.length` attribute，這個「在 runtime 偷偷轉換型別」的行為稱為 **[[Programming Language/零碎筆記#Casting vs. Coercing|coercing]]**，所以你可以把 `"abc".length` 視為 `(new String("abc")).length`。

# 參考資料

- <https://www.geeksforgeeks.org/how-are-strings-stored-in-javascript/>
