Module system（模組系統）是 JavaScript 在 [ES6](</Programming Language/JavaScript/ES5 vs ES6.md>) 才引入的概念。

# Module Import & Export in ES6

若要在 client-side JavaScript 中使用 `import`/`export` statement，則必須在 html 引入 root script 時聲明 `type="module"`：

```html
<script type="module" src="./js/main.js"></script>
```

在 [Node.js](</Programming Language/JavaScript/Node.js/Introduction.md>) 中要使用 `import`/`export`，則有兩種作法：

- 將有 `import`/`export` statement 的 module files 的副檔名改為 **.mjs**（聲明這是一個 module file）
- 在 package.json 中聲明 `"type": "module"`（否則預設是 `"type": "commonjs"`）

### Export

```JavaScript
// lib.js
export const aString = "test";

export function functionOne() {
    console.log("function one");
}

export const anObject = { a: 1 };

export class aClass {
    constructor(name) {
        this.name = name;
    }
}

function functionTwo() {
    console.log("function two");
}
export default functionTwo;
```

>[!Note]
>一個 module 只能有一個 `export default` statement。

### Import

```JavaScript
import defaultExport from "./lib.js";
import * as arbitraryName from "./lib.js";
import { aString, anObject } from "./lib.js";
import { aString as alias1 } from "./lib.js";
import { default as defaultExport } from "./lib.js";
import { aString, anObject as alias2, /* … */ } from "./lib.js";
import { "string name" as alias } from "./lib.js";
import defaultExport, { aString, /* … */ } from "./lib.js";
import defaultExport, * as arbitraryName from "./lib.js";
import "./lib.js";

console.log(arbitraryName.aString);
```

- Import default 時，若被 import 的 file 中有 `export default xxx` 語句，就會將 `xxx` import 進來；若被 import 的 file 中沒有 `export default xxx` 語句，就會噴 SyntaxError。
- `import defaultExport from "./lib.js";` 效果等同於 `import { default as defaultExport } from "./lib.js";`

# Static Import vs. Dynamic Import

前面提供的 import declaration syntax 都屬於 static import，所有被 import 的 modules 都會在載入當前的 module 時的 **load time** 被一併載入。

如果有一些肥大且不一定會用到的模組，使用 static import 不只很浪費網路流量與頻寬，也佔用 memory。

ECMAScript 在 ES2020 推出了 function 型式的 `import()`，讓開發者可以在程式碼中進行 conditional import（又叫做 dynamic import），可以讓 module 在 **run time** 被選擇性載入。

### Dynamic Import 的用法

[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import)

### 把 Dynamic Import 變 Synchronous

`import()` statement 會 return 一個 `Promise` object，所以可以用 `async`/`await` 或 `.then` 把 import 流程變成 synchronous，例如：

```JavaScript
async function loadMyModule() {
    return ({ default: hello, world } = await import("./exp2.mjs"));
}

loadMyModule().then((module) => {
    console.log(module.default, module.world);
});
```

### Dynamic Import 不須要宣告 `type="module"`

`import()` 與 import declaration syntax 最大的差別是後者會需要在 html file 中先聲明 `<script type="module" src="<ROOT_MODULE>"></script>` 才能使用，但前者可以不用！

### Node.js 與 Client Side 皆可使用 Dynamic Import

# CommonJS vs. AMD

雖說 module system 是 JavaScript 在 ES6 才引入的概念，然而在 ES6 之前，社群上已發展了兩套較知名的模組系統，它們分別是 CommonJS 與 AMD (Asynchronous Module Definition)，兩者的簡單比較如下：

- CommonJS 在載入模組時是 synchronous 的；AMD (Asynchronous Module Definition) 則人如其名，是 asynchronous 的
- CommonJS 是設計給 server-side 用的（比如 Node.js）；AMD 則適合 client-side 使用（但現在大家都寫 ECMAScript）
- CommonJS 人如其名，在 import/export modules 時所使用的語法是與其他主流程式語言更像的；相對的 AMD 的 import/export 方式則很繁瑣

### `require` vs. `import`

我們已經知道 `import` 是 ES6 import module 所使用的 keyword。

CommonJS 與 AMD 在 import module 時使用的 keyword 則是 `require`，下方範例是 CommonJS 中 import module 的方式：

```JavaScript
// payments.js
var customerStore = require("./customer");
```

AMD 使用 `require` 的方式與 CommonJS 不同，因現在寫 client side code 的多數都已改用 ECMAScript 了，所以此處省略 AMD 的介紹。

>[!Note]
>以 `require` import module 時，module name 最後不用寫副檔名，但該檔案必須是 .js 檔（與 ES6 的 import 不同，ES6 是要帶副檔名，且該檔案要是 .mjs）。
>
>以上方的例子來說，customer 必定是一個叫 customer.js 的檔案。

### `exports` vs. `modules.exports`

CommonJS 的 export statement 型如 `exports = ...`（注意結尾有 s）：

```JavaScript
// customer.js
exports = function () {  
    return customers.get("store");  
};
```

雖然說早期 Node.js 使用的是 CommonJS 的規範，但其實在 Node.js 中必須使用 `module.exports = ...` 才行：

```JavaScript
// customer.js
module.exports = function () {  
    return customers.get("store");  
};
```

### `exports` vs. `define`

CommonJS 與 AMD 在 import module 時使用的 keyword 都是 `require`，但在 export module 時它們所使用的 keyword 就有分歧了。

如前所述，`exports` 是 CommonJS 用來 export module 的 keyword；AMD 則是使用 `define`。 

因現在寫 client side code 的多數都已改用 ECMAScript 了，所以此處省略 AMD 的介紹。

# 在 Module System 之前

在 CommonJS 與 AMD 也還沒發展起來之前，JavaScript 只能透過 **Revealing Module Pattern** 實現 encapsulation，舉例如下：

```JavaScript
var revealingModule = (function () {
    var privateVar = "Ben Thomas";
    function setNameFn(strName) {
        privateVar = strName;
    }
    return {
        setName: setNameFn,
    };
})();

revealingModule.setName("Paul Adams");
```

這種替代方案的缺點包括：

- 所有程式碼都要寫在同一個 file 中，不能跨 files 引用
- 所有 revealing module 的載入過程是 synchronous 的

# 參考資料

- <https://eyesofkids.gitbooks.io/javascript-start-from-es6/content/part4/module_system.html>
- <https://www.greatfrontend.com/questions/quiz/what-do-you-think-of-amd-vs-commonjs>
- <https://dmitripavlutin.com/ecmascript-modules-dynamic-import/>
