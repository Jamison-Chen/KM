# 存取 Admin Tool

正式環境與開發環境皆有 Admin Tool，存取方式如下：

**Step1: 至首頁**

（正式）`www.pinkoi.com`

（測試）`www.local.office.pinkoi.com`

**Step2: 先登入有 Admin 權限的帳號**

**Step3: 網址列輸入 path `/admin/v-dash` (新版) 或 `/admin` (舊版)**

舊版 Admin Tool (`www.local.office.pinkoi.com/admin`) 會將你導向至 `https://sites.google.com/pinkoi.com/pinkoi-wiki?pli=1&authuser=1`，此時須點選左側選單中的 Tools，然後下滑至 Admin Tools 段落。

# Watch Admin Tool

#TODO 

# 新增一個 Tool

### Step1: 新增一個 Page Folder

在 `/admin-site/src/pages` 裡新增一個 Page Folder，folder 所在的位置應與 tool 在 Admin Tool 側邊欄的位置一致，這是 convention，目的是方便尋找。

有些 directory 只是用來 group 多個 tools 用的。

Page folder 裡至少會有 `index.vue` 一個檔案，這個檔案是 tool 的 home。

Page folder 的 `index.vue` 裡不應放入任何 UI 邏輯以及資料操作邏輯，故通常只會看到：

- `<template>` 裡包著若干個 component(s)
- `<route>` 裡包著一個 object，這個 object 決定了畫面的 header
- 在 `<script>` 裡更改 `document.title`

像是下面這樣：

```vue
<template>
    <my-component />
</template>

<route>
{
    meta: {
        title: 'My Tool Name'
    }
}
</route>

<script>
export default {
    created() {
        document.title = 'My Tool Name'
    }
}
</script>
```

### Step2: 新增一個 Menu Item

在 `/admin-site/src/components/menuItems.js` 裡新增一個 object，object 所在的位置會影響 tool 在 Admin Tool 側邊欄的位置。

Object 長的像這樣：

```javascript
{
    title: 'My Tool',
    icon: 'icon-name',
    to: '/route/to/tool',
}
```

# Components

#TODO 
