# import libraries
import os.path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from .models import NftCertificateImage
from bbb_api.models import TemporaryFiles
import uuid
from api.global_variable import BASE_URL, BASE_DIR
from .models import NftCertificateImage

def ImageWriter(user_name):
    # open image
    img_path = NftCertificateImage.objects.get(name="NFT template").image.path
    img = Image.open(img_path)

    I1 = ImageDraw.Draw(img)

    # Custom font style and font size
    myFont = ImageFont.truetype('/usr/share/fonts/truetype/Ikaros-Regular.ttf', 48)

    # Add Text to an image
    I1.text((36, 230), f"{user_name}", font=myFont, fill=(0, 0, 0))

    # Display edited image
    # img.show()

    # Save the edited image
    img_name = uuid.uuid4()
    if not os.path.exists('media/nft_images/'):
        os.mkdir("media/nft_images/")
    generated_path = os.path.join("media/nft_images/{}".format(img_name)+ ".jpeg")
    img.save(generated_path)
    return BASE_URL + "/" + generated_path

