#OOP

>本系列多數文章將以 Java 作為說明用之語言。

OOP 中包含以下四大核心概念：

1. [[#^53976a|抽象化 (Abstraction)]]
2. [[#^5ba7b6|封裝 (Encapsulation)]]
3. [[繼承 (Inheritance)]]
4. [[多型 (Polymorphism)]]

# Abstraction

^53976a

OOP 的宗旨在：

1. 將現實世界裡的問題抽象化為物件 (objects) 間的行為
2. 將物件抽象化為類別 (classes)
3. 將類別抽象化為 [[Interface vs. Abstract Class in Java|interfaces 以及 abstract classes]]。

# Encapsulation

^5ba7b6

Encapsulation 即「透過 `public`, `private`, `protected` 等關鍵字來限制一個 attribute 或 method 可以在哪裡被存取」這個動作，目的是達到 information hiding，而 information hiding 事實上也是 abstraction 的其中一部分。

一個 class 中，很多時候某些 attributes 並不是設計來給外部使用者隨意更動的；有些 attributes 則可能因爲是機密資訊所以不希望隨意被外部使用者存取，上述兩種情況就需要使用 encapsulation 來限制使用者的存取權限。

通常在標準的 OOP 中，一個 class 內的所有 attributes 都會是 `private` 或是 `protected`，會另外定義 `public` 的 get methods 與 set methods 供外部使用者存取部分 attributes。

# Polymorphism

Polymorphism 從字面上用中文的白話文來說就是「一體多面」或「一詞多義」，技術上可以分為 overriding 與 overloading 兩種技術。

### Override vs. Overload

當 class A 繼承 class B 時，在沒有其餘設計的情況下，一個 method M 在由 class A 所實例化的 object 呼叫，與由 class B 所實例化的 object 呼叫時，所達到的效果會相同。如果想要讓效果有所不同，就必須在 class A 中重新定義 method M，重新定義 method M 時，若 method M 所接收的參數數量與原本相同，則稱此行為為 Overriding；若參數數量不同，則此行為稱為 Overloadding。

# 參考資料

<https://en.wikipedia.org/wiki/Encapsulation_(computer_programming)>
