import json
from typing import Dict

from fastapi import FastAPI
from modal import App, Image, Secret, Volume, asgi_app

from app.settings import settings

name = "modal-crdts"
app = App(name=name)
vol = Volume.from_name(label=f"{name}-db", create_if_missing=True)

_app_env_dict: Dict[str, str | None] = {
    f"APP_{str(k)}": str(v) for k, v in json.loads(settings.model_dump_json()).items()
}
app_env = Secret.from_dict(_app_env_dict)


image = (
    Image.debian_slim()
    .pip_install("uv")
    .workdir("/work")
    .copy_local_file("pyproject.toml", "/work/pyproject.toml")
    .copy_local_file("uv.lock", "/work/uv.lock")
    .copy_local_dir("app", "/work/app")
    .env({"UV_PROJECT_ENVIRONMENT": "/usr/local"})
    .run_commands(
        [
            "uv sync --frozen --compile-bytecode",
            "uv build",
        ]
    )
)


@app.function(
    allow_concurrent_inputs=100,
    concurrency_limit=1,
    cpu=2.0,
    image=image,
    keep_warm=1,
    memory=1024,
    secrets=[app_env],
    volumes={"/work/modal-crdts-db": vol},
)
@asgi_app(label=name)
def _app() -> FastAPI:
    from app.main import app as _app

    return _app
