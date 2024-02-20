import requests


class HttpClient:
    def get_basic_session(
        self,
        username,
        password,
    ):
        session = requests.session()
        session.auth = requests.auth.HTTPBasicAuth(
            username=username,
            password=password,
        )
        
        return session
        
    def send_request(
        self,
        method,
        url,
        headers,
        params=None,
    ):
        if not params:
            
            params={}
        try:
            response = method(
                url=url,
                headers=headers,
                json=params,
            )
            response.raise_for_status()
        except Exception as e:
            raise e
        else:

            return response
