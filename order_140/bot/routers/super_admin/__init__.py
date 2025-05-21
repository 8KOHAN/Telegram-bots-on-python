from aiogram import Router, F
from aiogram.filters import MagicData

from . import menu, admin, channel, statistics


router = Router()


router.include_router(menu.router)
router.include_router(admin.router)
router.include_router(channel.router)
router.include_router(statistics.router)


__all__ = [
    'router'
]
