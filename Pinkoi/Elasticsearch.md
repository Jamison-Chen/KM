### 情境一

```Python
tid = []  # put some tids in this list
product_search = ProductSearch(
    filter_values={"tid": tids}, sort_opt=ProductSortOpt(tids=tids),
)
es_result = product_search.execute(use_cache=True).to_dict()
```

上面這樣的搜尋方法可能會搜不到商品，因為 `ProductSortOpt` 裡面有個 `sort_by`，預設值是 `'pop'`，意思是會將商品依照熱門程度排序，分數過低的商品會直接被截掉（找不到），所以如果 `tids` 裡的商品不夠熱門，就會搜不到那個商品。

**解決方法：**

把 `sort_by` 設為 `'relv'`（以相關性排序），自己與自己的相關性為 1，因此一定在最前面，不會被截斷。
