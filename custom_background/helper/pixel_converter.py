from PIL import Image
import glob
import os
from api.global_variable import BASE_DIR

def convert_pixels():
    folder = os.listdir(BASE_DIR + "/bg_images/")
    for i in folder:
        print(i)
        folder_2 = os.listdir(BASE_DIR + "/bg_images/" + i)
        for j in folder_2:
            print(i,j)
            path = BASE_DIR + "/bg_images/" + i + "/" + j
            # j = j.split(("."))
            # k = j[0] + "_lq." + j[-1]
            # print(k)
            resize_path = BASE_DIR + "/resized_images/" + i + "/" + j
            image = Image.open(path)
            print(image.format, image.size)
            res = image.resize((1920,1440))
            res.save(resize_path)
            print(resize_path)




convert_pixels()