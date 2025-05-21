from aiogram import Dispatcher

from . import super_admin, my_chat_member
from .admin import post, link_replace


def setup_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(super_admin.router)
    dispatcher.include_router(link_replace.router)

    dispatcher.include_router(post.router)
    dispatcher.include_router(my_chat_member.router)


__all__ = [
    'setup_routers'
]
