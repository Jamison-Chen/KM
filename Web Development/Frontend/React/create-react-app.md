#package

# 在 React 中使用 TypeScript

### 初始化專案

```bash
npx create-react-app my-app --template typescript

# TypeScript + Redux
npx create-react-app my-app --template redux-typescript
```

### Class component 在繼承 `React.Component` 時，需要使用 generic 的方式注入定義好的 props 以及 state 的 interfaces

```tsx
interface Props {
    // ...
}

interface State {
    // ...
}

export default class HelloWorld extends React.Component<Props, State> {
    public state: State;
    public constructor(props: Props) {
        super(props);
        this.state = {};
    }
    public render(): React.ReactNode {
        return <div></div>;
    }
}
```

# 在 React 中使用 SCSS

### Step1

```bash
npm install sass
```

### Step2

將所有副檔名為 `.css` 的檔案改為 `.scss`

# Scoped Styling

在 React 中，一個 `.css` 檔案只要被任一個 component import，就會變成 global styling。

因此，如果有 `a.css` 與 `b.css` 兩個檔案，裡面都含有對 `.button` (class) 的 styling，其中 `a.css` 先被 component `a.tsx` import；而後 `b.css` 被 component `b.tsx` import（注意先後順序），則 `a.tsx` 中，`className="button"` 的元素的 styling，會是 `b.css` 中 `.button` 的樣子，這是因為發生了 Class Name Collision（`a.css` 的 `.button` 被 `b.css` 的 `.button` 覆蓋過去了）。

然而，若將 `a.css` 以及 `b.css` 的檔名分別改為 `a.module.css` 與 `b.module.css`，則 create-react-app 會在 compile 時幫我們把 `.<className>` 改成 `<fileName>_<className>__<hash>`，進而避免 Class Name Collision 發生，這使得我們可以不用考慮不同 components 間是否有用到重複的 CSS class name，這就是所謂的 Scoped Styling。

需要注意的是，改完檔名後，component import CSS 的方式，以及設定元素的 `className` attribute 的方式也會有所改變：

### Importing

從原本的 `import "./example.css";` 變成 `import styles from "./example.module.css";`。

### 設定 `className` Attribute

從原本的 `className="button"` 變成 `className={styles.button}`，其中 `styles.button` 的型別為 `string`。

上述改檔名的方法也適用於 SCSS 檔案，也就是說 `a.scss` 只要改成 `a.module.scss` 就會有 Scoped Styling 效果。

其實還有其他方法可以做到 Scoped Styling，請參考 <https://www.upbeatcode.com/react/css-scoping-in-react-everything-you-need-to-know/>

# 建議的專案結構

```plaintext
├── .git
├── build
├── node_modules
├── public
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── src
│   ├── assets
│   │   ├── dog.png
│   │   └── cat.png
│   ├── components
│   │   ├── Button
│   │   |   ├── Button.module.scss
│   │   |   └── Button.tsx
│   │   └── Header
│   │       ├── Header.module.scss
│   │       └── Header.tsx
│   ├── pages
│   │   ├── Main
│   │   │   ├── About
│   │   │   |   ├── About.module.scss
│   │   │   |   └── About.tsx
│   │   │   ├── Home
│   │   │   |   ├── Home.module.scss
│   │   │   |   └── Home.tsx
│   │   │   ├── Main.module.scss
│   │   │   └── Main.tsx
│   │   └── Login
│   │       ├── Login.module.scss
│   │       └── Login.tsx
│   ├── utils
│   │   ├── apis.ts
│   │   └── auth.ts
│   ├── _global_variables.scss
│   ├── index.scss
│   ├── index.tsx
│   ├── react-app-env.d.ts
│   ├── reportWebVitals.ts
│   ├── router.tsx
│   └── setupTests.ts
├── .gitignore
├── package-lock.json
├── package.json
├── README.md
├── tsconfig.json
└── .gitignore
```

# 如何讀取 `.env` 檔案？

### 參考資料

[Adding Custom Environment Variables | Create React App](https://create-react-app.dev/docs/adding-custom-environment-variables)

### 摘要

除非是 React 原本就定義好的 attributes，否則所有自定義的 environment variables 皆須以 `REACT_APP_` 開頭，在 component 內則以 `process.env.REACT_APP_XXX` 讀取之。
