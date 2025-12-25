"""Styling constants and component styles for the Chopstickz web interface."""

import reflex as rx

# Color palette
bg_dark_color = "#04030F"
bg_medium_color = "#9B6A6C"
border_color = "#fff3"
accent_light = "#776885"
accent_color = "#776885"
accent_dark = "#9B6A6C"
icon_color = "#fff8"
text_light_color = "#fff"

# Shadows
shadow_light = "rgba(4, 3, 15, 0.15) 0px 48px 100px 0px"
shadow = (
    "rgba(95, 26, 55, 0.25) 0px 50px 100px -20px, "
    "rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, "
    "rgba(119, 104, 133, 0.35) 0px -2px 6px 0px inset"
)

# Component styles
message_style = dict(
    display="inline-block",
    p="4",
    border_radius="xl",
    max_w="30em",
)

input_style = dict(
    bg=bg_medium_color,
    border_color=border_color,
    border_width="1px",
    p="4",
)

textbox_style = dict(
    bg=accent_color,
    border_color=border_color,
    border_width="1px",
    p="4",
)

icon_style = dict(
    font_size="md",
    color=icon_color,
    _hover=dict(color=text_light_color),
    cursor="pointer",
    w="8",
)

sidebar_style = dict(
    border="double 1px transparent",
    border_radius="10px",
    background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_dark})",
    background_origin="border-box",
    background_clip="padding-box, border-box",
    p="2",
    _hover=dict(
        background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_light})",
    ),
)

# Base application style
base_style = {
    rx.chakra.Avatar: {
        "shadow": shadow,
        "color": text_light_color,
        "bg": accent_color,
    },
    rx.chakra.Button: {
        "shadow": shadow,
        "color": text_light_color,
        "_hover": {
            "bg": accent_dark,
        },
    },
    rx.chakra.Menu: {
        "bg": bg_dark_color,
        "border": "red",
    },
    rx.chakra.MenuList: {
        "bg": bg_dark_color,
        "border": f"1.5px solid {bg_medium_color}",
    },
    rx.chakra.MenuDivider: {
        "border": f"1px solid {bg_medium_color}",
    },
    rx.chakra.MenuItem: {
        "bg": bg_dark_color,
        "color": text_light_color,
    },
    rx.chakra.DrawerContent: {
        "bg": bg_dark_color,
        "color": text_light_color,
        "opacity": "0.9",
    },
    rx.chakra.Hstack: {
        "align_items": "center",
        "justify_content": "space-between",
    },
    rx.chakra.Vstack: {
        "align_items": "stretch",
        "justify_content": "space-between",
    },
}
