import json
from typing import Any

import reflex as rx

from .config import auth


class AuthState(rx.State):
    error_message: str = ""
    user_json: str = rx.LocalStorage("null")
    in_progress: bool = False

    @rx.background
    async def login(self, form_data: dict[str, Any]):
        async with self:
            self.in_progress = True
        async with self:
            self.login_main(form_data)
        async with self:
            self.in_progress = False

    def login_main(self, form_data: dict[str, Any]):
        try:
            user = auth.sign_in_with_email_and_password(form_data["email"], form_data["password"])
            self.user_json = json.dumps(user)
            self.error_message = ""
        except Exception as e:
            error = json.loads(e.strerror)
            self.error_message = error["error"]["message"]

    @rx.background
    async def signup(self, form_data: dict[str, Any]):
        async with self:
            self.in_progress = True
        async with self:
            self.signup_main(form_data)
        async with self:
            self.in_progress = False

    def signup_main(self, form_data: dict[str, Any]):
        try:
            if "confirm_password" in form_data and form_data["password"] != form_data["confirm_password"]:
                raise ValueError("Passwords do not match")
            user = auth.create_user_with_email_and_password(form_data["email"], form_data["password"])
            self.user_json = json.dumps(user)
            self.error_message = ""
        except ValueError as e:
            self.error_message = str(e)
        except Exception as e:
            error = json.loads(e.strerror)
            self.error_message = error["error"]["message"]

    def logout(self):
        self.user_json = "null"
        self.error_message = ""

    def refresh(self):
        if self.is_logged_in:
            user = auth.refresh(self.user["refreshToken"])
            self.user_json = json.dumps(user)
        else:
            self.user_json = "null"

    @rx.var
    def user(self):
        return json.loads(self.user_json)

    @rx.var
    def is_logged_in(self):
        return self.user is not None

    def reset_error(self):
        self.error_message = ""
