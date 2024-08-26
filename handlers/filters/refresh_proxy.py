from aiogram import types
from aiogram.filters import Filter


class RefreshProxyFilter(Filter):
    async def __call__(self, data: types.CallbackQuery) -> bool:
        return data.data.startswith('refresh_proxy_status')