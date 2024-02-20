from . import _http_client


class Env0ApiClient(
    _http_client.HttpClient,
):
    base_url = 'https://api.env0.com'
    headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
    
    def __init__(
        self,
        api_key,
        api_secret,
        org_id,
    ):
        self.session = self.get_basic_session(
            username=api_key,
            password=api_secret,
        )
        self.org_id = org_id
        
    def env0_api_call(
        self,
    ):
        pass