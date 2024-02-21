import pydantic
import os


class Env0Settings(
    pydantic.BaseModel,
):
    env0_env_path: str
    
    @property
    def env0_env_path_json_file(
        self,
    ):
        return f'env0.env-vars.json'

    def __init__(
        __pydantic_self__,
        **data,
    ):
        super().__init__(
            env0_env_path=os.getenv('ENV0_ENV'),
            **data
        )
