from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from bbb_api.models import TemporaryFiles
from api.global_variable import BASE_DIR
import boto3
import magic
from api.global_variable import AWS_LOCATION, \
    AWS_SECRET_ACCESS_KEY, \
    AWS_ACCESS_KEY_ID, \
    AWS_STORAGE_BUCKET_NAME, \
    AWS_BASE_URL


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):

      file = TemporaryFiles.objects.create(
          temp_file=request.data['media'],
          created_at=datetime.utcnow()
      )
      path = BASE_DIR + "/" + file.temp_file.url[1:]
      name = file.temp_file.url.split("/")[-1]
      s3 = boto3.resource('s3', region_name=AWS_LOCATION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
      BUCKET = AWS_STORAGE_BUCKET_NAME
      destination = "media/cover_images/{}".format(name)
      mimetype = file_path_mime(path)
      s3.Bucket(BUCKET).upload_file(path, destination, ExtraArgs={
          "ContentType": mimetype
      })
      url = AWS_BASE_URL + name
      return Response({"status": True, "url": url})


def file_path_mime(file_path):
    mime = magic.from_file(file_path, mime=True)
    return mime
