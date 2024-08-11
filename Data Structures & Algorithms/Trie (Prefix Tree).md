Prefix tree 顧名思義就是用來解決與 prefix 相關的問題的資料結構，比如當你在瀏覽器的搜尋列輸入關鍵字時，如果你之前曾搜尋過相同的關鍵字，瀏覽器就會在你輸入到一半時提供自動完成的功能。

這類問題一般化後就是「在一堆詞中找出所有具有給定 prefix 的資料」。解決這個問題主要有 array 與 prefix tree 兩種方法：

# 使用 Array

這是比較直觀的想法，用 array 把所有詞存起來，每次要搜尋時就將 array 中的資料一個一個拿出來檢查。

### Time Complexity

- Insert: $O(1)$
    - 將詞放進 array
- Search: $O(m \cdot n)$
    - m 為存詞的 array 的長度，n 為 prefix 的長度

可以發現使用 array 在 search 的時間複雜度很高，而 prefix tree 的誕生正是為了降低 search 的時間複雜度。

# 使用 Prefix Tree

假設現在有 "app"、"apple"、"bear"、"beer"、"cat" 與 "camel" 這些字要存起來供搜尋，可以把他們存成這樣：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/trie.png>)

### Insertion

每次加入新詞 `w` 時都會從 tree root 開始，看 `w` 的第一個字元（`w[0]`）是否是 root 的其中一個 child node，如果是的話就直接移到該 node，並對 `w[1]` 做相同的事；如果沒找到 child node，就為目前所在的 node 新增一個值為 `w[i]` 的 child node。重複上述動作直到遍歷完 `w` 的所有字元後，將最後一個字元所在的 node 額外做一個標記，表示該 node 是某個詞的結尾。

##### Time Complexity

每次加入新詞時都要遍歷該詞的所有字元，並在 prefix tree 中往下探索，因此時間複雜度是 $O(n)$，n 為 prefix 的長度。

### Search

Search 與 insert 的流程很像，差別是當在某個字元處（`w[k]`）沒有找到 child node 時，就會停下來了，且此時就代表沒有任何一個既有的詞擁有 prefix `w`；反之若成功遍歷完 `w` 的所有字元，就代表有找到至少一個具有 prefix `w` 的字詞，此時若要取出所有結果，就是從目前停下來的 node 開始往下 traverse 整個 subtree。

##### Time Complexity

- 若只是要確認有沒有任何一個既有字詞擁有 prefix，則時間複雜度是 $O(n)$
    - n 是 prefix 的長度
- 若要得到所有具有 prefix 的字詞，因為要遍歷最後停下來的 node 的所有 subtree，所以時間複雜度為 $O(m \cdot (k-n))$，
    - m 是既有字詞數量，n 是 prefix 的長度，k 是平均每個既有字詞的長度

# Implement Trie

（使用 Python）

```Python
class PrefixTree:
    def __init__(self) -> None:
        self.prefix_tree = {}

    def insert(self, input_str: str) -> None:
        if not input_str:
            return
        root = self.prefix_tree
        for char in input_str:
            root.setdefault(char, {})
            root = root[char]
        root[""] = root.get("", 0) + 1  # use "" to count words that end here

    def search(self, input_str: str) -> list[str]:
        root = self.prefix_tree
        for char in input_str:
            if char not in root:
                return []
            root = root[char]
        return self.__get_all_suffixes(root, input_str)

    def __get_all_suffixes(self, root: dict, prefix: str) -> list[str]:
        result = []
        if count := root.get(""):
            result.extend([prefix] * count)
        for key in root:
            if key != "":
                result.extend(self.__get_all_suffixes(root[key], prefix + key))
        return result
```

# 參考資料

- <https://ithelp.ithome.com.tw/m/articles/10294596>
- <https://itsparesh.medium.com/24f9375cdbc3>
