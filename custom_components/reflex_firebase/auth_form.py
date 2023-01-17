import reflex as rx

from .auth_state import AuthState


def signup_form(
    heading: rx.Component = rx.heading("Create an account", size="3"),
    width: str = "100%",
    spacing: str = "4",
    confirm: bool = True,
):
    return rx.vstack(
        rx.form(
            rx.vstack(
                heading,
                rx.input(
                    placeholder="Email",
                    name="email",
                ),
                rx.input(
                    placeholder="Password",
                    name="password",
                    type="password",
                ),
                rx.cond(
                    confirm,
                    rx.input(
                        placeholder="Confirm Password",
                        name="confirm_password",
                        type="password",
                    ),
                ),
                rx.button(
                    "Sign Up",
                    type="submit",
                ),
                rx.text(
                    AuthState.error_message,
                    color="red",
                ),
                width=width,
                spacing=spacing,
            ),
            on_submit=AuthState.signup,
        )
    )


def login_form(
    heading: rx.Component = rx.heading("Login", size="3"),
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
                    placeholder="Email",
                    name="email",
                ),
                rx.input(
                    placeholder="Password",
                    name="password",
                    type="password",
                ),
                rx.button(
                    "Login",
                    type="submit",
                ),
                rx.text(
                    AuthState.error_message,
                    color="red",
                ),
                rx.cond(
                    len(signup_path) > 0,
                    rx.button(
                        "Create an account",
                        on_click=rx.redirect(signup_path),
                    ),
                ),
                rx.cond(
                    reset_password_path,
                    rx.button(
                        "Forgot password?",
                        on_click=rx.redirect(reset_password_path),
                    ),
                ),
                width=width,
                spacing=spacing,
            ),
            on_submit=AuthState.login,
        )
    )
