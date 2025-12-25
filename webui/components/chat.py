"""Chat interface components."""

import reflex as rx

from webui import styles
from webui.components.loading import loading_icon
from webui.state import QA, State


def message(qa: QA) -> rx.Component:
    """Render a single question/answer message pair."""
    return rx.chakra.box(
        rx.chakra.box(
            rx.chakra.text(
                qa.question,
                bg=styles.border_color,
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.chakra.box(
            rx.chakra.text(
                qa.answer,
                bg=styles.accent_color,
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """Render the chat message list."""
    return rx.chakra.vstack(
        rx.heading("LLM powered Editor", align="center", weight="medium"),
        rx.chakra.box(rx.foreach(State.chats[State.current_chat], message)),
        py="8",
        flex="1",
        width="100%",
        max_w="3xl",
        padding_x="4",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    """Render the message input action bar."""
    return rx.chakra.box(
        rx.chakra.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.chakra.hstack(
                        rx.chakra.input(
                            placeholder="Type something...",
                            id="question",
                            _placeholder={"color": "#fffa"},
                            _hover={"border_color": "#fffa"},
                            style=styles.textbox_style,
                        ),
                        rx.chakra.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.chakra.text("Process"),
                            ),
                            type_="submit",
                            _hover={"bg": "#5F1A37"},
                            style=styles.input_style,
                        ),
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.process_question,
                reset_on_submit=True,
                width="100%",
            ),
            width="100%",
            max_w="3xl",
            mx="auto",
        ),
        position="sticky",
        bottom="0",
        left="0",
        py="4",
        backdrop_filter="auto",
        backdrop_blur="lg",
        align_items="stretch",
        width="100%",
        bg="rgba(255,255,255, 0.1)",
    )
