from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # if the user is deleted, also delete the profile but not vice versa
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            if img.height > img.width:
                crop_size = (0, 0, img.width, img.width)
            else:
                crop_size = (0, 0, img.height, img.height)
            cropped_img = img.crop(crop_size)
            cropped_img.thumbnail(output_size)
            cropped_img.save(self.image.path)
