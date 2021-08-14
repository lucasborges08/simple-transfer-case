from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="CONF",
    settings_files=["settings.toml", "urls.toml", ".secrets.toml"],
    environments=True,
)
