"""Modal dialog component for creating new chats."""

import reflex as rx

from webui.state import State


def modal() -> rx.Component:
    """Render the new chat creation modal."""
    return rx.chakra.modal(
        rx.chakra.modal_overlay(
            rx.chakra.modal_content(
                rx.chakra.modal_header(
                    rx.chakra.hstack(
                        rx.chakra.text("Create new chat"),
                        rx.chakra.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_modal,
                            color="#fff8",
                            _hover={"color": "#fff"},
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                rx.chakra.modal_body(
                    rx.chakra.input(
                        placeholder="Type something...",
                        on_blur=State.set_new_chat_name,
                        bg="#776885",
                        border_color="#5F1A37",
                        _placeholder={"color": "#776885"},
                    ),
                ),
                rx.chakra.modal_footer(
                    rx.chakra.button(
                        "Create",
                        bg="#9B6A6C",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#9B6A6C"},
                        on_click=State.create_chat,
                    ),
                ),
                bg="#1D1C27",
                color="#fff",
            ),
        ),
        is_open=State.modal_open,
    )
