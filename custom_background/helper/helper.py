from rest_framework.views import APIView
from api.global_variable import BASE_DIR
from rest_framework.response import Response
import boto3, os
from ..models import background_pictures
import magic

class post_pictures(APIView):
    def get(self, request):
        path_list = []
        folder = os.listdir(BASE_DIR + "/bg_images/")
        for i in folder:
            folder_2 = os.listdir(BASE_DIR + "/bg_images/" + i)
            for j in folder_2:
                print(j)
                path = BASE_DIR + "/bg_images/" + i + "/" + j
                item = {"path": path, "name": j, "category": i}
                path_list.append(item)
                break
            break
        print(path_list)
        for i in path_list:
            source = i["path"]
            name = i["name"]
            category = i["category"]
            print(source,name, category)
            s3 = boto3.resource('s3', 'aws_access_key_id', 'aws_secret_access_key')
            BUCKET = 'AWS_STORAGE_BUCKET_NAME'
            destination = "media/custom_background/{}".format(name)
            mimetype = file_path_mime(source)
            s3.Bucket(BUCKET).upload_file(source, destination, ExtraArgs={
        "ContentType": mimetype
    })
            url_list = []
            background_picture = background_pictures()
            background_picture.name = name
            print(background_picture.name)
            background_picture.categories = category
            print(background_picture.categories)
            url = "http://s3.us-east-2.amazonaws.com/video.wiki/media/custom_background/{}".format(name)
            url_list.append(url)
            background_picture.picture = url
            print(background_picture.picture, "here")
            background_picture.save()

        return Response({"status": True, "urls": url_list})


def file_path_mime(file_path):
    mime = magic.from_file(file_path, mime=True)
    return mime