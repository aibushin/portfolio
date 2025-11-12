import uvicorn
from src.configs import EnvEnum, settings


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=settings.backend_port,
        log_config=settings.log_config,
        reload=settings.enviroment == EnvEnum.dev,
        reload_dirs=["src"],
        # reload_includes=["src/**/*.py"],
        # reload_excludes=["logs"],
    )
