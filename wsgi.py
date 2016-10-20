import os

from pagetags.main import create_app

environment_type = os.getenv("PAGETAGS_ENV_TYPE", "production")

settings_file = os.getenv("PAGETAGS_SETTINGS")

if settings_file is None:
    print("The environment variable PAGETAGS_SETTINGS is not set")
    exit(1)

app = create_app(settings_file, environment_type)
