import asyncio
from typing import Dict, Any, Optional

from app.core.init_redis import drugs_db


class DrugCache:
    def __init__(self):
        self.session = drugs_db
        self.expire = 60 * 60 * 24

    async def save_query_to_cache(self, **kwargs) -> bool:
        # check if cart already exists
        search_query = kwargs['search_query']
        url: str = kwargs['url']
        key = f"drag:{search_query}:{url.split(':')[1]}"

        if await self.is_search_query_in_cache(search_query, url):
            return False
        else:
            await self.session.set(f'query:{search_query}', 1, ex=self.expire)
            [await self.session.hset(key, index, str(value)) for index, value in kwargs.items()]
            await self.session.expire(key, self.expire)

            return True

    async def save_page_to_cache(self, **kwargs) -> bool:
        page_id: str = kwargs['page_id']
        key = f"drag:page:{page_id}"

        if await self.get_page_query(page_id):
            return False
        else:
            [await self.session.hset(key, index, str(value)) for index, value in kwargs.items()]
            await self.session.expire(key, self.expire)

            return True

    async def is_search_query_in_cache(self, search_query, url: str = None) -> bool:
        query = await self.session.get(f'query:{search_query}')
        if query is None:
            return False

        if url is None:
            pass
        else:
            data = await self.get_all_search_query(search_query)
            url_list = []

            for item in data:
                url_list.append(item['url'])

            return url in url_list

        return True

    # async def is_page_in_cache(self, page_id: str = None) -> bool:
    #     query = await self.session.get(f'query:{page_id}')
    #     if query is None:
    #         return False
    #     return True

    async def get_all_search_query(self, query: str) -> list:
        data = []
        async for item in self.session.scan_iter(f"drag:{query}:*"):
            item = await self.session.hgetall(item)
            data.append(
                {index.decode('utf-8'): value.decode('utf-8') for index, value in item.items()}
            )
        return data

    async def get_page_query(self, page_id) -> Optional[dict[Any, Any]]:
        item = await self.session.hgetall(f'drag:page:{page_id}')
        if len(item) == 0:
            return None
        return {index.decode('utf-8'): value.decode('utf-8') for index, value in item.items()}

    async def save_user_query(self, search_query: str, user_id: int) -> None:
        await self.session.set(search_query, user_id, ex=60*15)

    async def get_user_query(self, user_id: int) -> str:
        return await self.session.get(user_id)


drug_cache = DrugCache()


# class CartService:
#     _CART_SESSION = cart
#     _EXPIRED_TIME = 60 * 60
#
#
#
#     async def _quantity_check(self, data: dict) -> bool:
#         if int(data['takes_by_user']) >= int(data['quantity']):
#             return False
#         else:
#             await self._CART_SESSION.hincrby(
#                 f'carts:{data['user_id']}:{data['id']}',
#                 'takes_by_user'
#             )
#             return True
#
#
#
#     async def _update_time_all_cart(self, data: dict = None) -> None:
#         if data is not None:
#             await self._CART_SESSION.expire(
#                 f'carts:{data['user_id']}:{data['id']}',
#                 self._EXPIRED_TIME
#             )
#
#     async def carts(self, user_id: int) -> List[Dict[str, str]]:
#         description = []
#
#         async for user_carts in self._CART_SESSION.scan_iter(f"carts:{user_id}:*"):
#             data = await self._get_all_carts_data(user_carts)
#             await self._update_time_all_cart(data)
#
#             if int(data['takes_by_user']) > 1:
#                 items_price = float(data['price']) * float(data['takes_by_user'])
#             else:
#                 items_price = float(data['price'])
#
#             data.update(items_price=items_price)
#             description.append(data)
#         return description
#
#     async def get_product_from_cart(self, user_id: int, uuid: str) -> Optional[dict]:
#         key = f"carts:{user_id}:{uuid}"
#         item = await self._CART_SESSION.hgetall(key)
#         if len(item) > 0:
#             product = {index.decode('utf-8'): value.decode('utf-8') for index, value in item.items()}
#         else:
#             product = None
#         return product
#
#     async def add_product_to_cart(self, user_id: int, uuid: str, amount: int = 1) -> Optional[bool]:
#         data = await self.get_product_from_cart(user_id=user_id, uuid=uuid)
#         if data is None:
#             return None
#         else:
#             if amount + int(data['takes_by_user']) > int(data['quantity']):
#                 return False
#             else:
#                 await self._CART_SESSION.hincrby(
#                     f'carts:{data['user_id']}:{data['id']}',
#                     'takes_by_user',
#                     amount=amount
#                 )
#                 return True
#
#     async def add_choose_amount(self, user_id: int, uuid: str, amount: int) -> Optional[bool]:
#         data = await self.get_product_from_cart(user_id=user_id, uuid=uuid)
#         if data is None:
#             return None
#         else:
#             takes_by_user = int(data['takes_by_user'])
#             quantity = int(data['quantity'])
#             if takes_by_user >= quantity and amount + takes_by_user > data['quantity']:
#                 return False
#             else:
#                 await self._CART_SESSION.hincrby(
#                     f'carts:{data['user_id']}:{data['id']}',
#                     'takes_by_user'
#                 )
#                 return True
#
#     async def delete_product_cart(self, user_id: int, uuid: str) -> Optional[bool]:
#         data = await self.get_product_from_cart(user_id=user_id, uuid=uuid)
#         if data is None:
#             return None
#         else:
#             if int(data['takes_by_user']) <= 1:
#                 await self._CART_SESSION.delete(f"carts:{data['user_id']}:{data['id']}")
#                 return True
#             else:
#                 await self._CART_SESSION.hincrby(
#                     f'carts:{data['user_id']}:{data['id']}',
#                     'takes_by_user',
#                     amount=-1
#                 )
#                 return False
#
#     async def delete_all_carts(self, user_id: int) -> None:
#         [await self._CART_SESSION.delete(x) async for x in self._CART_SESSION.scan_iter(f"carts:{user_id}:*")]
#
#
# cart_service = CartService()
