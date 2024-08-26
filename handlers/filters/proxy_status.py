from aiogram import types
from aiogram.filters import Filter


class ProxyStatusFilter(Filter):
    async def __call__(self, data: types.CallbackQuery) -> bool:
        return data.data.startswith('proxy_status')
        