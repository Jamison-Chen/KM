在網頁應用程式的領域中，JavaScript 是 client-side 唯一的程式語言（唯一可以運行在所有主流瀏覽器中的程式語言），不過其實 JavaScript 不只可以運行在 client side，也可以用來寫 server side 的服務。

# 語言定位

- [Dynamic language](</Programming Language/程式語言的分類.md>)
- [Weakly-typed language](</Programming Language/程式語言的分類.md>)
- [Interpreted language](</Programming Language/程式語言的分類.md>)

# ECMAScript

ECMAScript 是規範所有 scripting language 的國際標準，JavaScript 也是在這個規範下發展。

不同年份制定的 ECMAScript 規範有可能差異很大，比如 [ES5 vs ES6](</Programming Language/JavaScript/ES5 vs ES6.md>)。這導致在某些版本能用的語法或 APIs 不一定能在另一個版本中使用。

為了 backward compatibility，有些開發者會先使用最近／主流的 ECMAScript 版本撰寫程式，再使用[[Babel.draft|其它工具]]將 source code 轉成較舊版本 ECMAScript，這個動作稱為 **transpiling**。

# JavaScript Runtime

完整文章請見 [[JavaScript Runtime.draft|JavaScript Runtime]]。

在 client side，JavaScript 運行在瀏覽器的 JavaScript runtime 上；在 server side 則是運行在像 [Node.js](</Programming Language/JavaScript/Node.js/0 - Introduction.md>) 這樣的 JavaScript runtime 中。
