import boto3


class Boto3Client:
    def get_session(
        self,
        service_name,
        region_name,
    ):
        session = boto3.session.Session()

        return session.client(
            service_name=service_name,
            region_name=region_name,
        )
