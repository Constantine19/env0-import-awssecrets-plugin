import pydantic
import os


class Env0Settings(
    pydantic.BaseModel,
):
    api_key: str
    api_secret: str
    env0_env_path: str

    def __init__(
        __pydantic_self__,
        **data,
    ):
        super().__init__(
            api_key=os.getenv('ENV0_API_KEY'),
            api_secret=os.getenv('ENV0_API_SECRET'),
            env0_env_path=os.getenv('ENV0_ENV'),
            **data
        )
