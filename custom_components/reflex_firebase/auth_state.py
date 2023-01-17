import json
from typing import Any

import reflex as rx

from .config import auth


class AuthState(rx.State):
    error_message: str = ""
    user: str = rx.LocalStorage("null")

    def login(self, form_data: dict[str, Any]):
        try:
            user = auth.sign_in_with_email_and_password(form_data["email"], form_data["password"])
            self.user = json.dumps(user)
            self.error_message = ""
        except Exception as e:
            error = json.loads(e.strerror)
            self.error_message = error["error"]["message"]

    def signup(self, form_data: dict[str, Any]):
        try:
            if "confirm_password" in form_data and form_data["password"] != form_data["confirm_password"]:
                raise ValueError("Passwords do not match")
            user = auth.create_user_with_email_and_password(form_data["email"], form_data["password"])
            self.user = json.dumps(user)
            self.error_message = ""
        except ValueError as e:
            self.error_message = str(e)
        except Exception as e:
            error = json.loads(e.strerror)
            self.error_message = error["error"]["message"]

    def logout(self):
        self.user = "null"
        self.error_message = ""

    @rx.var
    def is_logged_in(self):
        return json.loads(self.user) is not None
