#Cookie 

使用 `document.cookie` API 可以對 browser 的 cookies  進行寫入與讀取。

### 設置 Cookie

```JavaScript
document.cookie = "my_cookie=a1234"
```

上面的語法只會新增或修改 `my_cookie` 這個 cookie 的值，並不會把其它已存在的 cookies 清除。

### 讀取與刪除 Cookie

```TypeScript
function getCookie(key: string): string | null {
    const divider = key + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookies = decodedCookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i];
        while (c.charAt(0) === " ") c = c.substring(1);
        if (c.indexOf(divider) === 0) {
            return c.substring(divider.length, c.length);
        }
    }

    return null;
}

function deleteCookie(key: string): void {
    if (getCookie(key)) {
        const d = new Date();
        d.setTime(d.getTime() - 10);
        document.cookie = `${key}=;expires=${d.toUTCString()};path=/`;
    } else throw Error("Cookie Not Found");
}
```
