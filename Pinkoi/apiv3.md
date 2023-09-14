# 資料夾結構 (Partial)

```plaintext
└── apiv3
    ├── dependencies
    │   ├── __init__.py
    │   ├── acl.py
    │   └── rbac.py
    └── routes
    │   ├── admin
    │   │   ├── shop
    │   │   │   ├── __init__.py
    │   │   │   └── seller_rating.py
    │   │   ├── __init__.py
    │   │   └── coupon.py
    |   └── messenger
    │       ├── __init__.py
    │       └── message.py
    ├── __init__.py
    └── app.py
```

>[!Note] 資料夾結構即 API Enpoint Path
>在 `/apiv3/routes` 底下的資料夾結構，應等同於 api endpoint 的 path。
>
>比如若有一個 API endpoint path 為 `/apiv3/admin/coupon/query_coupons`，那它對應到的檔案就會是 `/apiv3/routes/admin/coupon.py`，且 `coupon.py` 中會有一個叫做 `query_coupons` 的 function。

# Include Routers

在 `/apiv3` 底下有一個 `app.py`，其中會 include `/apiv3/routes` 下的所有 top-level sub-packages 與 top-level modules，以開頭的資料夾結構來說，`app.py` 就會有下面這段：

```Python
from .routes.admin import router as admin_router
from .routes.admin.shop.seller_rating import router as sr_router
from .routes.admin.coupon import router as coupon_router
from .routes.messenger.message import router as message_router

api = OpenAPI(
    title='Pinkoi API v3',
    root_path="/apiv3",
    responses={
        400: {'model': BadRequestResponse},
        401: {'model': LoginRequiredResponse},
        228: {'model': OverlayScreenResponse},
        202: {'model': AsyncTaskResponse}
    },
    servers=_SERVERS,
    openapi_url='/openapi.json' if not settings.PRODUCTION else None,
)

api.include_router(admin_router, prefix='/admin')
api.include_router(
    coupon_router,
    prefix='/coupon',
    tags=['coupon']
)
# ...
```

### `api.include_router`

- `prefix` 會設為該 package 所對應到的 API endpoint path，必須以 `/` 開頭
- `tags` 會設為 `/apiv3/routes` 以後的 directory path，開頭不用 `/`

在 `/apiv3/routes` 底下的每層 sub-directory 都要有自己的 `__init__.py` file（但 `/apiv3/routes` 自己不用有），`__init__.py` 內要 include 所有與自己同層的 modules，比如開頭例子中的 `/apiv3/routes/admin/__init__.py` 裡面就應該要有下面這段：

```Python
from django_mini_fastapi import APIRouter

from .shop import router as shop_router
from .coupon import router as coupon_router

router = APIRouter()

router.include_router(
    shop_router,
    prefix='/shop',
    tags=['admin/shop'],
)

router.include_router(
    coupon_router,
    prefix='/coupon',
    tags=['admin/coupon']
)
```

`/apiv3/routes/admin/shop/__init__.py` 裡面則應該要有下面這段：

```Python
from django_mini_fastapi import APIRouter

from .seller_rating import router as seller_rating_router

router = APIRouter()

router.include_router(
    seller_rating_router,
    prefix='/seller_rating',
    tags=['admin/shop/seller_rating'],
)
```

### `tags` 參數

`tags` 參數會讓 API document 出現對應的段落，因此若一個 sub-directory 中全部都是下一層的 route directory、沒有 module，那麼該 sub-directory 在其 parent 的 `__init__.py` 或者是 `/apiv3/app.py` 被 include 時就不需要 `tags`

# 範例 API

```Python
from django_mini_fastapi import APIRouter, Depends

from pinkoi.schemas.base.responses import BaseJSONResponse
from pinkoi.schemas.pinkoi_academy.requests import SubscriptionPayload
from pinkoi.schemas.pinkoi_academy.responses import SubscriberCountResp
from pinkoi.models2 import pinkoi_academy as pinkoi_academy_model
from pinkoi.models2.pinkoi_academy import (
    TopicIdEnum,
    TOPIC_ID_TO_CAMPAIGN_ID,
)
from pinkoi.models2 import campaign_ta as campaign_ta_m
from pinkoi.apiv3.exceptions import handle_base_api_exception
from pinkoi.apiv3.dependencies.acl import seller_required


router = APIRouter()


@router.get('/get_subscriber_count', response_model=SubscriberCountResp)
@handle_base_api_exception
def get_subscriber_count(topic_id: TopicIdEnum):
    return {
        "count": campaign_ta_m.get_campaign_uid_count(
            TOPIC_ID_TO_CAMPAIGN_ID[topic_id]
        )
    }

@router.post('/subscribe',
    dependencies=[
        Depends(write_old_topic_permission),
        Depends(write_old_notification_center_permission),
    ],
    response_model=BaseJSONResponse
)
@handle_base_api_exception
def subscribe(
    payload: SubscriptionPayload, uid: str = Depends(seller_required)
):
    pinkoi_academy_model.user_subscribe_pinkoi_academy(
        payload.topic_id, uid
    )
    return {}
```

### 寫在 `/apiv3/admin` 底下的 API 會預設有 `admin_required` 

# API 文件

下列 endpoints 可以查看自動產生的 API 文件：

- `/apiv3/docs` (OpenAPI)
- `/apiv3/redoc`
