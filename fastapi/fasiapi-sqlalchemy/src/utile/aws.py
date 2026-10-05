import boto3


class S3:


    def __init__(self):
        self.__access_key_id = "CRRW7b3F2tkPtB50On54"
        self.__secret_access_key = "YgCqvWEtCSQglNozwdCI4FLw0Ob9Bgr25VxZl75s"
        self.__endpoint_url = "http://localhost:9000"  # Change this if using a different S3 provider
        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.__access_key_id,
            aws_secret_access_key=self.__secret_access_key,
            endpoint_url=self.__endpoint_url,  # Change this to your bucket name
            region_name="us-east-1"
        )
        self.bucket_name="spark-data"


    def put_object_presigned_url(self, object_name,content_type=None, expiration=3600):
        params={'Bucket': self.bucket_name, 'Key': object_name}
        if content_type:
            params['ContentType'] = content_type
        return self.client.generate_presigned_url(
            ClientMethod='put_object',
            Params=params,
            ExpiresIn=expiration,
            HttpMethod="PUT"
        )

    def get_object_presigned_url(self, object_name, expiration=3600):
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )

    def delete_object(self, object_name):
        self.client.delete_object(Bucket=self.bucket_name, Key=object_name)

    def get_object(self, object_name):
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=object_name
        )
        return response['Body']