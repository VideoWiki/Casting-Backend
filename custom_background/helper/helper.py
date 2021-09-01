from rest_framework.views import APIView
from api.global_variable import BASE_DIR
from rest_framework.response import Response
import boto3, os
from ..models import background_pictures
import magic
from api.global_variable import \
    AWS_LOCATION, BASE_URL_AWS, \
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    AWS_STORAGE_BUCKET_NAME

class post_pictures(APIView):
    def get(self, request):
        path_list = []
        folder = os.listdir(BASE_DIR + "/resized_images/")
        for i in folder:
            folder_2 = os.listdir(BASE_DIR + "/resized_images/" + i)
            for j in folder_2:
                print(j)
                path = BASE_DIR + "/resized_images/" + i + "/" + j
                item = {"path": path, "name": j, "category": i}
                path_list.append(item)



        print(path_list)
        id = 1
        for i in path_list:
            source = i["path"]
            name = i["name"]
            category = i["category"]
            print(name,category)
            print(source,name, category)
            s3 = boto3.resource('s3', region_name=AWS_LOCATION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            BUCKET = AWS_STORAGE_BUCKET_NAME
            destination = "media/custom_background/lq{}".format(name)
            mimetype = file_path_mime(source)
            s3.Bucket(BUCKET).upload_file(source, destination, ExtraArgs={
        "ContentType": mimetype
    })
            url_list = []

            background_picture = background_pictures.objects.get(id=id)
            # background_picture.name = name
            # background_picture.category = category
            # background_picture.credit = name
            url = BASE_URL_AWS + "custom_background/lq{}".format(name)
            url_list.append(url)
            background_picture.low_quality_url = url
            # background_picture.credit = name
            background_picture.save()
            id += 1
        return Response({"status": True, "urls": url_list})


def file_path_mime(file_path):
    mime = magic.from_file(file_path, mime=True)
    return mime


def logo_upload():
    folder = os.listdir(BASE_DIR + "/casting_logo/")
    for i in folder:
        source = BASE_DIR + "/casting_logo/" + i
        name = i
        print(source, name, BASE_URL_AWS)
        s3 = boto3.resource('s3', region_name=AWS_LOCATION,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        BUCKET = AWS_STORAGE_BUCKET_NAME
        destination = "media/default_logo/{}".format(name)
        mimetype = file_path_mime(source)
        s3.Bucket(BUCKET).upload_file(source, destination, ExtraArgs={
            "ContentType": mimetype
        })
        url = BASE_URL_AWS + "default_logo/" + name

    return url
