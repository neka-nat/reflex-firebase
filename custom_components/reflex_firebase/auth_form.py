from typing import Type

import reflex as rx

from .auth_state import AuthState


def signup_form(
    state_type: Type[AuthState] = AuthState,
    heading: rx.Component = rx.heading("Create an account", size="6", as_="h2", width="100%"),
    size: str = "3",
    width: str = "100%",
    spacing: str = "4",
    confirm: bool = True,
    login_path: str = "/login",
):
    return rx.vstack(
        rx.form(
            rx.vstack(
                heading,
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="Email",
                    type="email",
                    name="email",
                    size=size,
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Password",
                    name="password",
                    type="password",
                    size=size,
                    width="100%",
                ),
                rx.cond(
                    confirm,
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Confirm Password",
                        name="confirm_password",
                        type="password",
                        size=size,
                        width="100%",
                    ),
                ),
                rx.button(
                    rx.spinner(loading=state_type.in_progress),
                    "Sign Up",
                    type="submit",
                    size=size,
                    width="100%",
                ),
                rx.text(
                    state_type.error_message,
                    color="red",
                ),
                width=width,
                spacing=spacing,
            ),
            on_submit=state_type.signup,
        ),
        rx.cond(
            len(login_path) > 0,
            rx.button(
                "Already have an account?",
                on_click=rx.redirect(login_path),
                size=size,
                width="100%",
            ),
        ),
    )


def login_form(
    state_type: Type[AuthState] = AuthState,
    heading: rx.Component = rx.heading("Login", size="6", as_="h2", width="100%"),
    size: str = "3",
    width: str = "100%",
    spacing: str = "4",
    reset_password_path: str = "",
    signup_path: str = "/signup",
) -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                heading,
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="Email",
                    type="email",
                    name="email",
                    size="3",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Password",
                    name="password",
                    type="password",
                    size="3",
                    width="100%",
                ),
                rx.button(
                    rx.spinner(loading=state_type.in_progress),
                    "Login",
                    type="submit",
                    size=size,
                    width="100%",
                ),
                rx.text(
                    state_type.error_message,
                    color="red",
                ),
                width=width,
                spacing=spacing,
            ),
            on_submit=state_type.login,
        ),
        rx.cond(
            len(signup_path) > 0,
            rx.button(
                "Create an account",
                on_click=rx.redirect(signup_path),
                size=size,
                width="100%",
            ),
        ),
        rx.cond(
            reset_password_path,
            rx.button(
                "Forgot password?",
                on_click=rx.redirect(reset_password_path),
                size=size,
                width="100%",
            ),
        ),
    )
