### Enum

```Python
# Use
from pinkoi.utils.enums import TextEnum

# instead of
from django_mini_fastapi.enums import StrEnum
```

### Lang

```Python
# Use
from pinkoi.utils.webs import get_client_lang
lang = get_client_lang()

# instead of
from pinkoi import g
lang = g.LANG
```

### JSON

```Python
# Use
from pinkoi.lib import json

# instead of
import json
```

### 使用 Peewee 取代 Orator

### 新的 API 一律使用 apiv3 的寫法

### APIv3 中的 Pagination

```Python
from pinkoi.base.pagination import Pagination as BasePagination
from pinkoi.schemas.base.base import Pagination

# ...

@router.get('/xxx', dependencies=..., response_model=XxxResponse)
def xxx(pagination: Pagination = Depends()):
    # ...
    result, total_count = ...
    return XxxResponse(
        result=result,
        pagination=BasePagination(
            page=pagination.page,
            limit=pagination.limit,
            total=total_count
        ),
    )
```
