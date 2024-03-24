Quick Select 其實就是 quick sort 的閹割版，且如同 quick sort，quick select 也有分 in-place 跟非 in-place 之分。

### In-place Quick Select

```Python
def inPlaceQuickSelect(nums, k, l, r):
    def inPlacePartition(l, r):
        pivot = nums[r]
        i = l
        for j in range(l, r):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[r] = nums[r], nums[i]
        return i

    if l == r == k:
        return nums[-k]
    elif l >= r:
        raise Exception("The value of l should not be greater than r.")
    
    pivotIdx = inPlacePartition(l, r)
    
    if pivotIdx == len(nums) - k:
        return nums[pivotIdx]
    elif pivotIdx > len(nums) - k:
        return inPlaceQuickSelect(nums, k, l, pivotIdx - 1)
    else:
        return inPlaceQuickSelect(nums, k, pivotIdx + 1, r)
```
