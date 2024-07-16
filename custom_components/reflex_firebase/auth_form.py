from typing import Type

import reflex as rx

from .auth_state import AuthState


def notify_send_email_verification(
    state_type: Type[AuthState] = AuthState,
    size: str = "3",
    width: str = "100%",
    login_path: str = "/login",
) -> rx.Component:
    return rx.vstack(
        rx.text(
            "Please verify your email address.",
            size=size,
            width=width,
        ),
        rx.button(
            "Resend Verification Email",
            on_click=state_type.send_email_verification,
            size=size,
            width=width,
        ),
        rx.button(
            "Continue to Login",
            on_click=rx.redirect(login_path),
            size=size,
            width=width,
        ),
    )


def _signup_form_main(
    state_type: Type[AuthState],
    heading: rx.Component,
    size: str,
    width: str,
    spacing: str,
    confirm: bool,
    error_message: str,
) -> rx.Component:
    return (
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
            rx.cond(
                state_type.signup_error_message,
                rx.text(
                    error_message or state_type.signup_error_message,
                    color="red",
                ),
            ),
            width=width,
            spacing=spacing,
        ),
    )


def signup_form(
    state_type: Type[AuthState] = AuthState,
    heading: rx.Component = rx.heading("Create an account", size="6", as_="h2", width="100%"),
    size: str = "3",
    width: str = "100%",
    spacing: str = "4",
    confirm: bool = True,
    login_path: str = "/login",
    error_message: str = "",
    email_validation: bool = False,
):
    return rx.cond(
        email_validation & state_type.is_logged_in & ~state_type.is_email_verified,
        notify_send_email_verification(state_type=state_type, size=size, width=width, login_path=login_path),
        rx.vstack(
            rx.cond(
                email_validation,
                rx.form(
                    _signup_form_main(
                        state_type,
                        heading,
                        size,
                        width,
                        spacing,
                        confirm,
                        error_message,
                    ),
                    on_submit=state_type.signup_and_send_email_verification,
                ),
                rx.form(
                    _signup_form_main(
                        state_type,
                        heading,
                        size,
                        width,
                        spacing,
                        confirm,
                        error_message,
                    ),
                    on_submit=state_type.signup,
                ),
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
            on_mount=state_type.reset_signup_error_message,
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
    error_message: str = "",
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
                rx.cond(
                    state_type.login_error_message,
                    rx.text(
                        error_message or state_type.login_error_message,
                        color="red",
                    ),
                ),
                width=width,
                spacing=spacing,
            ),
            on_submit=state_type.login,
        ),
        rx.cond(
            len(signup_path) > 0,
            rx.vstack(
                rx.text("Or create an account", size=size),
                rx.button(
                    "Sign Up",
                    on_click=rx.redirect(signup_path),
                    size=size,
                    width="100%",
                ),
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
        on_mount=state_type.reset_login_error_message,
    )
