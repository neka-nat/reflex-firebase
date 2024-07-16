import json
from typing import Any

import reflex as rx

from .config import auth


class AuthState(rx.State):
    login_error_message: str = ""
    signup_error_message: str = ""
    user_json: str = rx.LocalStorage("null")
    account_info: dict[str, Any] = {}
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
            self.login_error_message = ""
        except Exception as e:
            error = json.loads(e.strerror)
            self.login_error_message = error["error"]["message"]

    @rx.background
    async def signup(self, form_data: dict[str, Any]):
        async with self:
            self.in_progress = True
        async with self:
            self.signup_main(form_data)
        async with self:
            self.in_progress = False

    @rx.background
    async def signup_and_send_email_verification(self, form_data: dict[str, Any]):
        async with self:
            self.in_progress = True
        async with self:
            self.signup_main(form_data)
        if self.is_logged_in:
            self.send_email_verification()
        async with self:
            self.in_progress = False

    def signup_main(self, form_data: dict[str, Any]):
        try:
            if "confirm_password" in form_data and form_data["password"] != form_data["confirm_password"]:
                raise ValueError("Passwords do not match")
            user = auth.create_user_with_email_and_password(form_data["email"], form_data["password"])
            self.user_json = json.dumps(user)
            self.signup_error_message = ""
        except ValueError as e:
            self.signup_error_message = str(e)
        except Exception as e:
            error = json.loads(e.strerror)
            self.signup_error_message = error["error"]["message"]

    def logout(self):
        self.user_json = "null"
        self.login_error_message = ""

    def send_email_verification(self):
        auth.send_email_verification(self.user["idToken"])

    def refresh(self):
        if self.is_logged_in:
            user = auth.refresh(self.user["refreshToken"])
            self.user_json = json.dumps(user)
        else:
            self.user_json = "null"

    def get_account_info(self):
        if not self.is_logged_in:
            return
        try:
            self.account_info = auth.get_account_info(self.user["idToken"])
        except Exception as e:
            self.account_info = {}

    @rx.var
    def user(self) -> dict[str, Any]:
        return json.loads(self.user_json)

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user is not None

    @rx.cached_var
    def is_email_verified(self) -> bool:
        if not self.is_logged_in:
            return False
        if not self.account_info:
            self.get_account_info()
        if "users" in self.account_info and self.account_info["users"]:
            return self.account_info["users"][0].get("emailVerified", False)
        return False

    @rx.var
    def email(self) -> str:
        return self.user["email"] if self.user else ""

    def reset_login_error_message(self):
        self.login_error_message = ""

    def reset_signup_error_message(self):
        self.signup_error_message = ""
