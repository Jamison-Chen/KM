在網頁應用程式的領域中，JavaScript 是 client-side 唯一的程式語言（唯一可以運行在所有主流瀏覽器中的程式語言），不過其實 JavaScript 不只可以運行在 client side，也可以用來寫 server side 的服務。在 client side，JavaScript 運行在 [[JavaScript Engine]] 上；在 server side，則是運行在 [[JavaScript/Node.js/Introduction|Node.js]] 中。

# 語言定位

- [[程式語言的分類|Dynamic Language]]
- [[程式語言的分類|Weakly-Typed Language]]

# ECMAScript

ECMAScript 是規範所有 scripting language 的國際標準，JavaScript 也是在這個規範下發展。

不同年份制定的 ECMAScript 規範有可能差異很大，比如 [[ES5 vs ES6]]，這導致在某些版本能用的語法或 APIs 不一定能在另一個版本中使用。

為了 backward compatibility，有些開發者會先使用最近／主流的 ECMAScript 版本撰寫程式，再使用[[Babel|其它工具]]將 source code 轉成較舊版本 ECMAScript，這個動作稱為 **transpiling**。

# Web APIs

Web APIs 是一系列瀏覽器原生的 APIs，這些 APIs 只有寫 client side 時可以用，但某些 API 名稱也被 server side 拿去當作類似功能的 API 名稱。舉例來說，Web API 中的 `console.log` 的功能是將 output stdout 在瀏覽器的 developer tool 中；在 Node.js 則是拿來將 output stdout 在 terminal 中。

其中一個 client-side code 與 server-side code 最大的差別就是 client side 有許多與 event listening/handling 相關的 Web APIs，因為在 client side 要處理各式各樣的 user actions 才能與 user 互動。

參考資料：[Web APIs Documentation](https://developer.mozilla.org/en-US/docs/Web/API)
