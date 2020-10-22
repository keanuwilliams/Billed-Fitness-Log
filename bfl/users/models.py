from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    DISTANCES = (
        ('mi', 'mi'),
        ('km', 'km'),
    )
    WEIGHTS = (
        ('lbs', 'lbs'),
        ('kg', 'kg'),
        ('st', 'st'),
    )
    # if the user is deleted, also delete the profile but not vice versa
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # default to the default.jpeg picture when profile is created
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    weight = models.FloatField(default=0)
    goal_weight = models.FloatField(default=0)
    weight_units = models.CharField(max_length=3, choices=WEIGHTS, default='lbs')
    distance_units = models.CharField(max_length=3, choices=DISTANCES, default='mi')
    hide_resistance = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'  # how profile name will be displayed on Admin site

    def save(self):
        super().save()  # initially save the image
        img = Image.open(self.image.path)  # open the image
        if img.height > 300 or img.width > 300:  # if the image is too large
            output_size = (300, 300)  # the desired output size
            # if the image is rectangular then crop the top half of the picture into a square
            # depending on if the height is larger than the width or vice versa
            if img.height > img.width:
                crop_size = (0, 0, img.width, img.width)
            else:
                crop_size = (0, 0, img.height, img.height)
            cropped_img = img.crop(crop_size)  # crop the image into a square
            cropped_img.thumbnail(output_size)  # crop the image into the desired output size
            cropped_img.save(self.image.path)  # save the image
