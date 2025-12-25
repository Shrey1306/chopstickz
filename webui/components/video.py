"""Video display and upload components."""

import reflex as rx

from webui import styles
from webui.state import State


class VideoDisplayState(State):
    """Extended state for video display functionality."""

    @rx.var
    def dynamic_section(self) -> str:
        """Generate dynamic HTML for video display based on uploaded segments."""
        video_segments = self.video_segments

        if len(video_segments) > 0:
            videos_html = (
                "<script src='./custom_video_controls.js'></script>"
                "<div style='width: 100%;'>"
            )
            for url_v in video_segments[:1]:
                videos_html += f"""
                <div class="custom-video-player">
                    <video id="video_1" width="100%" height="auto" controls autoplay loop muted>
                        <source src="/{url_v}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <button id="playPauseBtn" data-video-id="video_1" style="margin: 20px; background-color: #9B6A6C; border-radius: 10px; padding: 10px 20px 10px 20px; color: white; cursor: pointer;">Pause</button>
                    <div class="seek-bar-container" style="position: relative; width: 100%;">
                        <input type="range" id="seekBar" value="0" min="0" max="100" step="1" style="width: 100%; z-index: 2; position: relative;">
                        <canvas id="highlightCanvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; opacity: 0.4;"></canvas>
                    </div>
                </div>
                """
            videos_html += "</div>"
            return videos_html
        else:
            return "<p style='font-size: large; padding: 50px;'>Upload a Stream to Start Editing</p>"


def videodisplay() -> rx.Component:
    """Render the video upload and display component."""
    color = "#776885"

    upload_section = rx.chakra.vstack(
        rx.upload(
            rx.chakra.vstack(
                rx.button(
                    "Select File",
                    _hover={"bg": "#5F1A37"},
                    style=styles.input_style,
                ),
                rx.text("Drag and drop Stream here or Click to Select"),
            ),
            border=f"1px dotted {color}",
            padding="50px",
            border_radius="lg",
        ),
        rx.hstack(rx.foreach(rx.selected_files, rx.text)),
        rx.button(
            "Upload",
            on_click=lambda: State.handle_upload(rx.upload_files()),
            bg=color,
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files,
            bg=color,
        ),
        spacing="4",
    )

    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.box(
                upload_section,
                width="40%",
                margin="0px",
                padding="10px",
                flex_grow="1",
                text_align="center",
            ),
            rx.chakra.box(
                rx.html(VideoDisplayState.dynamic_section),
                width="60%",
                border_radius="lg",
                padding="10px",
                flex_grow="1",
                text_align="center",
                bg="rgba(255,255,255, 0.1)",
            ),
            spacing="4",
        ),
        flex_grow="1",
        padding_right="20px",
    )

