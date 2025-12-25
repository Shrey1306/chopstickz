"""Main Chopstickz web application."""

import reflex as rx

from webui import styles
from webui.components import chat, modal, navbar, sidebar, videodisplay
from webui.state import State


@rx.page(title="prod.ai")
def index() -> rx.Component:
    """Render the main application page."""
    return rx.chakra.vstack(
        rx.script(src="/custom_video_controls.js"),
        navbar(),
        rx.chakra.hstack(
            rx.scroll_area(
                rx.chakra.flex(
                    videodisplay(),
                    direction="column",
                    spacing="4",
                ),
                type="always",
                scrollbars="vertical",
                style={
                    "height": "calc(100vh - 20vh)",
                    "width": "80%",
                    "borderRightWidth": "1px",
                    "borderColor": "white",
                },
            ),
            rx.scroll_area(
                rx.chakra.flex(
                    chat.chat(),
                    direction="column",
                    spacing="4",
                ),
                type="always",
                scrollbars="vertical",
                style={"height": "calc(100vh - 20vh)", "width": "20%"},
            ),
            align="stretch",
            spacing="0",
        ),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


app = rx.App(style=styles.base_style)
app.add_page(index)
