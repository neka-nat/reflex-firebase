"""Welcome to Reflex! This file showcases the custom component in a basic app."""
from typing import ClassVar

from rxconfig import config

import reflex as rx
from dotenv import load_dotenv

load_dotenv()

from reflex_firebase import signup_form, login_form, AuthState, PyrebaseModel


class Todo(PyrebaseModel):
    __key__: ClassVar[str] = "todos"
    contents: list[str] = []


class State(rx.State):
    """The app state."""
    todos: list[str] = []

    async def add_todo(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        if auth_state.is_logged_in:
            current_todos = Todo.get(auth_state)
            current_todos = current_todos.contents if current_todos else []
            current_todos.append(form_data["todo"])
            Todo(contents=current_todos).save(auth_state)
            self.todos = current_todos

    async def get_todos(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.is_logged_in:
            current_todos = Todo.get(auth_state)
            return current_todos.contents if current_todos else []
        return []

    async def update_todos(self):
        self.todos = await self.get_todos()


def signup() -> rx.Component:
    return rx.center(
        signup_form(login_path="/", error_message="アカウントを作成できませんでした。", email_validation=True),
        height="100vh",
    )


def todo() -> rx.Component:
    return rx.vstack(
        rx.foreach(State.todos, rx.text),
        rx.form(
            rx.vstack(
                rx.input(name="todo"),
                rx.button("Save", type="submit"),
            ),
            on_submit=State.add_todo,
            reset_on_submit=True,
        ),
        on_mount=State.update_todos,
    )


def index() -> rx.Component:
    return rx.center(
        rx.cond(
            AuthState.is_logged_in,
            rx.vstack(
                rx.heading("You are logged in", size="1"),
                rx.cond(
                    AuthState.is_email_verified,
                    rx.text("Your email is verified."),
                    rx.text("Please verify your email."),
                ),
                rx.cond(
                    AuthState.is_email_verified,
                    todo(),
                ),
                rx.button("Logout", on_click=AuthState.logout),
            ),
            login_form(error_message="ログインできませんでした。"),
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(signup)
