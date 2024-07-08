"""Welcome to Reflex! This file showcases the custom component in a basic app."""
from typing import ClassVar

from rxconfig import config

import reflex as rx
from dotenv import load_dotenv

load_dotenv()

from reflex_firebase import signup_form, login_form, AuthState, PyrebaseModel


class User(PyrebaseModel):
    __key__: ClassVar[str] = "users"
    email: str


class State(rx.State):
    """The app state."""
    error_message: str = ""
    in_progress: bool = False

    @rx.background
    async def login(self, form_data: dict[str, str]):
        async with self:
            self.in_progress = True
        async with self:
            auth_state = await self.get_state(AuthState)
        auth_state.login_main(form_data)
        if auth_state.is_logged_in:
            User(email=auth_state.user["email"]).save(auth_state.user["localId"])
        async with self:
            self.error_message = auth_state.error_message
            self.in_progress = False


def signup() -> rx.Component:
    return rx.center(
        signup_form(login_path="/"),
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
            login_form(State),
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(signup)
