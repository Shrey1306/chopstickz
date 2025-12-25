"""Navigation bar component."""

import reflex as rx

from webui.state import State


def navbar() -> rx.Component:
    """Render the top navigation bar."""
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.hstack(
                rx.chakra.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=State.toggle_drawer,
                    cursor="pointer",
                ),
                rx.chakra.link(
                    rx.chakra.box(
                        rx.chakra.image(src="favicon.ico", width=30, height="auto"),
                        p="1",
                        border_radius="6",
                        bg="#F0F0F0",
                        mr="2",
                    ),
                    href="/",
                ),
                rx.chakra.breadcrumb(
                    rx.chakra.breadcrumb_item(
                        rx.chakra.heading("prod.ai", size="sm"),
                    ),
                    rx.chakra.breadcrumb_item(
                        rx.chakra.text(
                            State.current_chat, size="sm", font_weight="normal"
                        ),
                    ),
                ),
            ),
            rx.chakra.hstack(
                rx.chakra.button(
                    "+ New Edit",
                    bg="#9B6A6C",
                    px="4",
                    py="2",
                    h="auto",
                    on_click=State.toggle_modal,
                ),
                rx.chakra.menu(
                    rx.chakra.menu_button(
                        rx.chakra.avatar(name="User", size="md"),
                        rx.chakra.box(),
                    ),
                    rx.chakra.menu_list(
                        rx.chakra.menu_item("Help"),
                        rx.chakra.menu_divider(),
                        rx.chakra.menu_item("Settings"),
                    ),
                ),
                spacing="8",
            ),
            justify="space-between",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        position="sticky",
        top="0",
        z_index="100",
        bg="rgba(255,255,255, 0.1)",
    )
