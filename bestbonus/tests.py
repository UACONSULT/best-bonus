import os
import datetime
from PIL import Image
from loremipsum import get_sentence


from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError 


from bestbonus import models
from bestbonus.settings import BASE_DIR



# Tests Suplier Model
class SuplierModelTests(TestCase):
    def setUp(self):
        models.Suplier.objects.create(title="TTR Casino")



    def test_title_dublicate(self):
        """
        If we already have casino instace with the same title,
        """        
        with self.assertRaises(IntegrityError):
            models.Suplier.objects.create(title="TTR Casino")

# Just testing case. Do not pay attention
    def test_isupper(self):
        self.assertTrue('foo'.isupper())




    




# Tests Bonus Model
class BonusModelTests(TestCase):
    def setUp(self):
        mock_casnio = models.Suplier.objects.create(title='TESTING CASINO')

        mock_bonus = models.Bonus.objects.create(two_word_desc='TESTING BONUS',
        bonus_digit=1000, bonus_desc=get_sentence(5),
        suplier=mock_casnio, dep_bool=True, dep=5000, 
        doe=timezone.now() + datetime.timedelta(days=30),
        wager=20, bonus_type=0,
        )



