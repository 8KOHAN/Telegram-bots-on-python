from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardBuilder, InlineKeyboardButton,
                                    ReplyKeyboardMarkup, ReplyKeyboardBuilder)


class AdminFactory(CallbackData, prefix="sa"):
    action: str
    value: str = "-"

    @staticmethod
    def add_channel(channel_id: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="✅ додати",
            callback_data=AdminFactory(action="add_channel", value=channel_id)
        )
        return builder.as_markup()

    @staticmethod
    def back() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="📝 меню",
            callback_data="menu"
        )
        return builder.as_markup()

    class menu:
        @staticmethod
        def main() -> ReplyKeyboardMarkup:

            builder = ReplyKeyboardBuilder()

            builder.button(
                text="➕ создать пост",
                callback_data=AdminFactory(action="add_post")
            )
            builder.button(
                text="📑 контент-план",
                callback_data=AdminFactory(action="my_posts")
            )

            builder.button(
                text="✏️ изменить пост",
                callback_data=AdminFactory(action="admins")
            )
            builder.button(
                text="📊 статистика",
                callback_data=AdminFactory(action="channels")
            )
            builder.button(
                text="🖌 креативы",
                callback_data=AdminFactory(action="channels")
            )
            builder.button(
                text="⚙️ настройка",
                callback_data=AdminFactory(action="channels")
            )

            builder.adjust(1)
            return builder.as_markup()

        @staticmethod
        def choose_channel(channels: list[list[str]]) -> InlineKeyboardMarkup:

            builder = InlineKeyboardBuilder()
            buttons = []
            for channel in channels:
                buttons.append(
                    InlineKeyboardButton(
                        text=channel[0],
                        callback_data=AdminFactory(action="channel_settings", value=channel[1]).pack()
                    )
                )

            builder.row(
                *buttons,
                width=2
            )

            builder.row(
                InlineKeyboardButton(
                    text="📝 меню",
                    callback_data="menu"
                ),
                width=1
            )

            return builder.as_markup()

        @staticmethod
        def link(link: str, requests_count: int, link_id: str) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="✅ автоприйом",
                callback_data=AdminFactory(action="set_l_auto_a_t", value=link)
            )
            builder.button(
                text="❌ автоприйом ",
                callback_data=AdminFactory(action="set_l_auto_a_f", value=link)
            )

            builder.button(
                text=f"⚡ прийняти ({requests_count})",
                callback_data=AdminFactory(action="accept_link_req", value=link)
            )

            builder.button(
                text=f"📊 статистика",
                callback_data=AdminFactory(action="l_stat", value=link_id)
            )

            builder.button(
                text="➖ видалити",
                callback_data=AdminFactory(action="delete_link", value=link)
            )

            builder.button(
                text="📝 меню",
                callback_data="menu"
            )
            builder.adjust(2)

            return builder.as_markup()

        @staticmethod
        def channel(channel_id: str) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="🔗 посилання",
                callback_data=AdminFactory(action="channel_links", value=channel_id)
            )

            builder.button(
                text="📊 статистика",
                callback_data=AdminFactory(action="choose_c_stat", value=channel_id)
            )

            builder.button(
                text="➖ видалити",
                callback_data=AdminFactory(action="delete_channel", value=channel_id)
            )

            builder.button(
                text="🔙 назад",
                callback_data=AdminFactory(action="channels")
            )
            builder.adjust(2)

            return builder.as_markup()

        @staticmethod
        def admin(admin_id: str) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="⬇️ знизити",
                callback_data=AdminFactory(action="set_adm_n_sup", value=admin_id)
            )
            builder.button(
                text="⬆️ підвищити ",
                callback_data=AdminFactory(action="set_adm_sup", value=admin_id)
            )

            builder.button(
                text="🔗 посилання",
                callback_data=AdminFactory(action="admin_links", value=admin_id)
            )

            builder.button(
                text="📊 статистика",
                callback_data=AdminFactory(action="choose_a_stat", value=admin_id)
            )

            builder.button(
                text="➖ видалити",
                callback_data=AdminFactory(action="delete_admin", value=admin_id)
            )

            builder.button(
                text="🔙 назад",
                callback_data=AdminFactory(action="admins")
            )
            builder.adjust(2)

            return builder.as_markup()

        @staticmethod
        def choose_admin(admins: list[list[str]]) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            buttons = []
            for admin in admins:
                buttons.append(
                    InlineKeyboardButton(
                        text=admin[0],
                        callback_data=AdminFactory(action="admin_settings", value=admin[1]).pack()
                    )
                )

            builder.row(
                *buttons,
                width=2
            )

            builder.row(
                InlineKeyboardButton(
                    text="➕ додати адміна",
                    callback_data=AdminFactory(action="add_admin", value="0").pack()
                ),

                InlineKeyboardButton(
                    text="➕ додати суперадміна",
                    callback_data=AdminFactory(action="add_admin", value="1").pack()
                ),
                InlineKeyboardButton(
                    text="📝 меню",
                    callback_data="menu"
                ),
                width=1
            )
            return builder.as_markup()

    class statistics:
        @staticmethod
        def admin(date: str = "-") -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="⬅️",
                callback_data=AdminFactory(action="admin_stat", value="back")
            )

            if date == "all":

                builder.button(
                    text="🟦",
                    callback_data=AdminFactory(action="admin_stat", value="-")
                )
            else:
                builder.button(
                    text="➡️",
                    callback_data=AdminFactory(action="admin_stat", value="forward")
                )

            builder.button(
                text="📝 меню",
                callback_data="menu"
            )

            builder.adjust(2)
            return builder.as_markup()

        @staticmethod
        def channel(date: str = "-") -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="⬅️",
                callback_data=AdminFactory(action="channel_stat", value="back")
            )

            if date == "all":

                builder.button(
                    text="🟦",
                    callback_data=AdminFactory(action="channel_stat", value="-")
                )
            else:
                builder.button(
                    text="➡️",
                    callback_data=AdminFactory(action="channel_stat", value="forward")
                )
            builder.button(
                text="📝 меню",
                callback_data="menu"
            )
            builder.adjust(2)
            return builder.as_markup()


    @staticmethod
    def choose_channel_link(links: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        all_buttons = []
        for item in range(links):
            all_buttons.append(
                InlineKeyboardButton(
                    text=str(item + 1),
                    callback_data=AdminFactory(action="choose_chan_link", value=str(item)).pack()
                ))

        builder.row(
            *all_buttons, width=3
        )
        builder.row(
            InlineKeyboardButton(
                text="📝 меню",
                callback_data="menu"
            ),
            width=1
        )
        return builder.as_markup()

    class posts:
        @staticmethod
        def admin(links_list: list[int]) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            all_buttons = []
            for item in links_list:
                all_buttons.append(
                    InlineKeyboardButton(
                        text=str(item),
                        callback_data=AdminFactory(action="choose_chan_link", value=str(item)).pack()
                    ))

            builder.row(
                *all_buttons, width=3
            )

            buttons = []

            buttons.append(
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=AdminFactory(action="admin_links", value="back").pack()
            ))

            buttons.append(
                InlineKeyboardButton(
                    text="📝 меню",
                    callback_data="menu"
            ))

            buttons.append(
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=AdminFactory(action="admin_links", value="forward").pack()
            ))

            builder.row(
                *buttons, width=3
            )
            return builder.as_markup()

        @staticmethod
        def channel(links_list: list[int]) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            all_buttons = []
            for item in links_list:
                all_buttons.append(
                    InlineKeyboardButton(
                        text=str(item),
                        callback_data=AdminFactory(action="choose_chan_link", value=str(item)).pack()
                    ))

            builder.row(
                *all_buttons, width=3
            )

            buttons = []
            buttons.append(
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=AdminFactory(action="admin_links", value="back").pack()
                ))

            buttons.append(
                InlineKeyboardButton(
                    text="📝 меню",
                    callback_data="menu"
                ))

            buttons.append(
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=AdminFactory(action="channel_links", value="forward").pack()
                ))

            builder.row(
                *buttons, width=3
            )
            return builder.as_markup()

        @staticmethod
        def comments() -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="Так",
                callback_data=AdminFactory(action="comments", value="yes")
            )

            builder.button(
                text="Нi",
                callback_data=AdminFactory(action="comments", value="no")
            )
            return builder.as_markup()

        @staticmethod
        def sound() -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="Так",
                callback_data=AdminFactory(action="sound", value="yes")
            )

            builder.button(
                text="Нi",
                callback_data=AdminFactory(action="sound", value="no")
            )
            return builder.as_markup()

        @staticmethod
        def time() -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="Зараз",
                callback_data=AdminFactory(action="time", value="now")
            )

            builder.button(
                text="Потiм",
                callback_data=AdminFactory(action="time", value="other")
            )
            return builder.as_markup()

        @staticmethod
        def auto_delete() -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()

            builder.button(
                text="Так",
                callback_data=AdminFactory(action="auto_delete", value="yes")
            )

            builder.button(
                text="Нi",
                callback_data=AdminFactory(action="auto_delete", value="no")
            )
            return builder.as_markup()

        @staticmethod
        def choose_channel(channels: list[list[str]]) -> InlineKeyboardMarkup:

            builder = InlineKeyboardBuilder()
            buttons = []
            for channel in channels:
                buttons.append(
                    InlineKeyboardButton(
                        text=channel[0],
                        callback_data=AdminFactory(action="create_post", value=channel[1]).pack()
                    )
                )

            builder.row(
                *buttons,
                width=2
            )

            return builder.as_markup()

        @staticmethod
        def post_settings() -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()
            buttons = []

            buttons.append(
                InlineKeyboardButton(
                    text="Удалить описание",
                    callback_data="delete_description"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Изменить описание",
                    callback_data="change_description"
                )
            )

            builder.row(
                *buttons,
                width=1
            )

            buttons = []

            buttons.append(
                InlineKeyboardButton(
                    text="Описание: снизу",
                    callback_data="delete_post"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Спойлер: выкл",
                    callback_data="delete_post"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Реакции",
                    callback_data="delete_post"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="URL-кнопки",
                    callback_data="add_buttons"
                )
            )

            builder.row(
                *buttons,
                width=2
            )

            buttons = []
            buttons.append(
                InlineKeyboardButton(
                    text="🔔",
                    callback_data="delete_post"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Отключить комментарии",
                    callback_data="delete_post"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Копировать",
                    callback_data="delete_post"
                )
            )
            builder.row(
                *buttons,
                width=1
            )

            buttons = []
            buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Отменить",
                    callback_data="delete_post"
                )
            )
            buttons.append(
                InlineKeyboardButton(
                    text="Далее ➡️",
                    callback_data="plan_post"
                )
            )
            builder.row(
                *buttons,
                width=2
            )
            return builder.as_markup()

        @staticmethod
        def post_plan() -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()
            buttons = []

            buttons.append(
                InlineKeyboardButton(
                    text="По расписанию ▶️",
                    callback_data="delete_description"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Зацикленный постинг",
                    callback_data="change_description"
                )
            )

            buttons.append(
                InlineKeyboardButton(
                    text="Платный просмотр 🌟",
                    callback_data="change_description"
                )
            )

            builder.row(
                *buttons,
                width=1
            )

            buttons = []
            buttons.append(
                InlineKeyboardButton(
                    text="💰 Стоимость",
                    callback_data="delete_description"
                )
            )
            buttons.append(
                InlineKeyboardButton(
                    text="Отчет клиенту",
                    callback_data="delete_description"
                )
            )
            buttons.append(
                InlineKeyboardButton(
                    text="Таймер удаления",
                    callback_data="delete_description"
                )
            )
            buttons.append(
                InlineKeyboardButton(
                    text="Отложить ⏰",
                    callback_data="delete_description"
                )
            )
            buttons.append(
                InlineKeyboardButton(
                    text="◀️ Назад",
                    callback_data="delete_description"
                )
            )
            buttons.append(
                InlineKeyboardButton(
                    text="Опубликовать 🔥",
                    callback_data="post"
                )
            )
            builder.row(
                *buttons,
                width=2
            )
            return builder.as_markup()

