from aiogram import Dispatcher

from .admin import AdminMiddleware
from aiogram_album.no_check_count_middleware import WithoutCountCheckAlbumMiddleware

def setup_middlewares(dispatcher: Dispatcher) -> None:
    WithoutCountCheckAlbumMiddleware(router=dispatcher)
    dispatcher.message.outer_middleware(AdminMiddleware())
    dispatcher.callback_query.outer_middleware(AdminMiddleware())


__all__ = [
    'setup_middlewares'
]
