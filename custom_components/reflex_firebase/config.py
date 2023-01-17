import os

import pyrebase
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class FirebaseConfig(BaseModel):
    api_key: str = os.environ.get("FIREBASE_API_KEY")
    auth_domain: str = os.environ.get("FIREBASE_AUTH_DOMAIN")
    project_id: str | None = os.environ.get("FIREBASE_PROJECT_ID")
    storage_bucket: str | None = os.environ.get("FIREBASE_STORAGE_BUCKET")
    messaging_sensor_id: str | None = os.environ.get("FIREBASE_MESSAGING_SENDER_ID")
    app_id: str | None = os.environ.get("FIREBASE_APP_ID")
    measurement_id: str | None = os.environ.get("FIREBASE_MEASUREMENT_ID")
    database_url: str | None = Field(os.environ.get("FIREBASE_DATABASE_URL"), alias="databaseURL")

    model_config = ConfigDict(
        alias_generator=to_camel,
        population_by_field_name=True,
    )


def initialize_firebase(config: FirebaseConfig):
    firebase = pyrebase.initialize_app(config.model_dump(by_alias=True))
    auth = firebase.auth()
    db = firebase.database() if config.database_url else None
    storage = firebase.storage() if config.storage_bucket else None
    return auth, db, storage, firebase


auth, db, storage, firebase = initialize_firebase(FirebaseConfig())
