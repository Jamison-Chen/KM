#package 

# 官方文件

[Docs Home v6.3.0](https://reactrouter.com/docs/en/v6)

# Installation

```bash
npm install react-router-dom@6
```

# 基本導入方法

index.tsx

```tsx
import { BrowserRouter } from "react-router-dom";

import MyRouter from "./router";

root.render(
    <React.StrictMode>
        <BrowserRouter>
            <MyRouter />
        </BrowserRouter>
    </React.StrictMode>
);
```

---

router.tsx

```tsx
import {Routes, Route} from "react-router-dom";

import Home from "./page/Main/Home/Home.tsx"
import About from "./page/Main/About/About.tsx"

export default function MyRouter() {
    return (
        <Routes>
            <Route path="home" element={<Home />}>
            <Route path="about" element={<About />}></Route>
                // ...
            </Route>
            // ...
        </Routes>
    );
}
```

# 其他筆記

### 在 Class Component 上使用 React-Router Hooks

React-router hooks 只能在 function-based  components 中使用，無法直接在 class component 中使用，但可以將定義好的 class component 用 wrapper function 包住，並在 wrapper function 中利用 props 將 hooks 注入 component 中。詳見 <https://reactrouter.com/docs/en/v6/getting-started/faq#what-happened-to-withrouter-i-need-it> 。

在 router.tsx 定義 interface 與 wrapper function：

```tsx
import {
    Routes,
    Route,
    Navigate,
    Location,
    NavigateFunction,
    Params,
    useLocation,
    useNavigate,
    useParams,
    useSearchParams,
} from "react-router-dom";

export interface RouterInterface {
    router: {
        location: Location;
        navigate: NavigateFunction;
        params: Params;
        search_params: URLSearchParams;
        set_search_params: ReturnType<typeof useSearchParams>[1];
    };
}

export function withRouter(Component: any) {
    return (props: any = {}) => {
        let location = useLocation();
        let navigate = useNavigate();
        let params = useParams();
        let [search_params, set_search_params] = useSearchParams();
        return (
            <Component
                {...props}
                router={{
                    location,
                    navigate,
                    params,
                    search_params,
                    set_search_params,
                }}
            />
        );
    };
}
```

想使用的 React-router hooks 的 component，其 props 的 interface 需繼承 RouterInterface

```tsx
interface Props extends RouterInterface {}
```

export component 時，須使用 wrapper function 包住：

```tsx
export default withRouter(ExampleComponent);
```

在 router.tsx 中使用 page componet 的方法與原本無異：

```tsx
import Home from "./page/Main/Home/Home.tsx";

export default function MyRouter() {
    return (
        <Routes>
            <Route path="home" element={<Home />} />
            // ...
        </Routes>
    );
}
```

### `NavLink` 比 `Link` 更適合應用在 Navigation Bar

原因：`NavLink` 的 `className` 可以依照現在的頁面更換

```tsx
<NavLink
    to="/home"
    className={
        ({ isActive }) => isActive ? "active" : ""
    }
>
    首頁
</NavLink>
```
