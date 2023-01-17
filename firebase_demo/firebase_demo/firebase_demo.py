"""Welcome to Reflex! This file showcases the custom component in a basic app."""

from rxconfig import config

import reflex as rx
from dotenv import load_dotenv

load_dotenv()

from reflex_firebase import signup_form, login_form, AuthState


class State(rx.State):
    """The app state."""

    pass


def signup() -> rx.Component:
    return rx.center(
        signup_form(),
        height="100vh",
    )


def index() -> rx.Component:
    return rx.center(
        rx.cond(
            AuthState.is_logged_in,
            rx.vstack(
                rx.heading("You are logged in", size="1"),
                rx.button("Logout", on_click=AuthState.logout),
            ),
            login_form(),
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(signup)
