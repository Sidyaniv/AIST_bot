from aiogram import types

from aiogram.types import ContentType
from aiogram.filters import Filter


class ContentTypeFilter(Filter):
    def __init__(self, content_types: list[ContentType]):
        self.content_types = content_types

    async def __call__(self, message: types.Message) -> bool:
        return message.content_type in self.content_types