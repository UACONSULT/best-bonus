import os
import datetime
from loremipsum import get_sentence

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError 

from bestbonus import models
from bestbonus.settings import BASE_DIR



# Testing Suplier Model
class SuplierModelTests(TestCase):
    def setUp(self):
        models.Suplier.objects.create(title="TTR Casino")

    def test_title_dublicate(self):
        """
        If we already have casino instace with the same title,
        """        
        with self.assertRaises(IntegrityError):
            models.Suplier.objects.create(title="TTR Casino")
#?
# Just testing case. Do not pay attention
    # def test_isupper(self):
    #     self.assertTrue('foo'.isupper())
#?


# Testing Bonus Model
class BonusModelTests(TestCase):
    def setUp(self):
        mock_casnio = models.Suplier.objects.create(title='TESTING CASINO')

        mock_bonus = models.Bonus.objects.create(two_word_desc='TESTING BONUS',
        bonus_digit=1000, bonus_desc=get_sentence(5),
        suplier=mock_casnio, dep_bool=True, dep=5000, 
        doe=timezone.now() + datetime.timedelta(days=30),
        wager=20, bonus_type=0,
        )


    def test_ttl_full_doe(self):
        """
        test_ttl_full_doe() checks if DOE posted 100 days later DOA. Pretty common case.
        test_ttl_full_doe() should return 100days(datetime.timedelta(100)).
        To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today + 100 days. Bonus expires 100 days later.
        mock_bonus.doe = (timezone.now() + datetime.timedelta(days=100)).date()

        self.assertEqual(mock_bonus.ttl_full(), datetime.timedelta(days=100)) 



    def test_ttl_full_doe_past(self):
        """
        test_ttl_full_doe_past() checks if expiring date(doe) posted earlier adding date(doa) 
        If it is test_ttl_full_doe_past() should return 0 days(datetime.timedelta(0)).
        To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today - 30 days. Bonus expired 30 days ago.
        mock_bonus.doe = (timezone.now() - datetime.timedelta(days=30)).date()

        self.assertEqual(mock_bonus.ttl_full(), datetime.timedelta(0)) 


    def test_ttl_full_doe_today(self):
        """
        test_ttl_full_doe_today() checks if expiring date(doe) are the same with adding date(doa) 
        If it is ttl_full() should return 0 days(datetime.timedelta(0)). To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today
        mock_bonus.doe = datetime.date.today()

        self.assertEqual(mock_bonus.ttl_full(), datetime.timedelta(days=0)) 


    
    def test_ttl_full_no_doe(self):
        """
        test_ttl_full_no_doe() checks if expiring date(doe) is not specified 
        If we do not specify DOE value, default of the field calls today_plus_30_days() method
        and write into DOE field Today + 30 days. To see more, check out models.py
        """

        # Mock Bonus without DOE field. You can see it commented below
        no_doe_mock_bonus = models.Bonus.objects.create(two_word_desc='NO DOE BONUS',
        bonus_digit=1000, bonus_desc=get_sentence(5),
        suplier=models.Suplier.objects.get(pk=1), dep_bool=True, dep=5000, 
        # doe=timezone.now() + datetime.timedelta(days=30),
        wager=20, bonus_type=0,
        )

        self.assertEqual(no_doe_mock_bonus.ttl_full(), datetime.timedelta(days=30)) 


    def test_ttl_days(self):
        """
        test_ttl_days() checks if DOE posted 100 days later DOA. But returns integer of days.
        Instead of datetime.timedelta object
        test_ttl_days() should return 100(int). To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today + 100 days
        mock_bonus.doe = (timezone.now() + datetime.timedelta(days=100)).date()
        
        # 100 days
        self.assertEqual(mock_bonus.ttl_days(), 100) 


    def test_ttl_days_past_doe(self):
        """
        test_ttl_days_past_doe() checks if expiring date(doe) posted earlier adding date(doa).
        But returns integer of days. Instead of datetime.timedelta object.
        If it is test_ttl_days_past_doe() should return 0(int). To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today - 100 days
        mock_bonus.doe = (timezone.now() - datetime.timedelta(days=100)).date()
        
        self.assertEqual(mock_bonus.ttl_days(), 0) 


    def test_ttl_hours(self):
        """
        test_ttl_hours() checks if DOE posted 100 days later DOA. But returns integer of hours.
        Instead of datetime.timedelta object
        test_ttl_hours() should return 48(int). To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today + 2 days
        mock_bonus.doe = (timezone.now() + datetime.timedelta(days=2)).date()
        
        # 48 Hours = 2 days
        self.assertEqual(mock_bonus.ttl_hours(), 48)


    def test_ttl_hours_past_doe(self):
        """
        test_ttl_hours_past_doe() checks if expiring date(doe) posted earlier adding date(doa).
        But returns integer of hours. Instead of datetime.timedelta object.
        If it is test_ttl_hours_past_doe() should return 0(int). To see more, check out models.py
        """
        mock_bonus = models.Bonus.objects.all()[0]

        # Today - 2 days
        mock_bonus.doe = (timezone.now() - datetime.timedelta(days=2)).date()
        
        self.assertEqual(mock_bonus.ttl_hours(), 0) 




# Tests Filter mechansism
class FilterTests(TestCase):
    def setUp(self):
        pass
        # Mock JSON array we get from AJAX


#! Create comment desc and comment vars
    def test_parsingObject_proper_data(self):
        # Test JSON object parsing. It should return comprenshed data for 
        unparsed_JSON_array = [
            {'name': 'sorting', 'value': 'dep_min_to_max'}, 
            {'name': 'type', 'value': 'all'}, 
            {'name': 'wager-js-range-slider', 'value': '0;42'}, 
            {'name': 'bonus-js-range-slider', 'value': '0;5000'}, 
            {'name': 'deposit-js-range-slider', 'value': '0;10000'}
            ]


        parsed_JSON = {
            'sorting': 'dep_min_to_max',
            'type': 'all',
            'wager-js-range-slider': '0;42',
            'bonus-js-range-slider': '0;5000',
            'deposit-js-range-slider': '0;10000'}

        parsed_JSON_obj = models.parsingObject(unparsed_JSON_array)
        
        print(parsed_JSON_obj)
        self.assertEqual(parsed_JSON_obj, parsed_JSON)
        
    # def test_AJAX_works(self):
    #     response = self.client.post('/add-item-to-collection')
    #     self.assertEqual(response.status_code, 200)
    
    def sortingAll(self):
        pass
        # for param in FILTERLIST['sorting'].keys()) 
            # bonuses_result.order_by(FILTER_LIST[])
            # self.assertEqual(b)








#! The testing code below is from Django docs Polls App
# class QuestionModelTests(TestCase):

#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)
    
#     def test_was_published_recently_with_old_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is older than 1 day.
#         """
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_question = Question(pub_date=time)
#         self.assertIs(old_question.was_published_recently(), False)

#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() returns True for questions whose pub_date
#         is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_question = Question(pub_date=time)
#         self.assertIs(recent_question.was_published_recently(), True)


#     def create_question(question_text, days):
#         """
#         Create a question with the given `question_text` and published the
#         given number of `days` offset to now (negative for questions published
#         in the past, positive for questions that have yet to be published).
#         """
#         time = timezone.now() + datetime.timedelta(days=days)
#         return Question.objects.create(question_text=question_text, pub_date=time)


# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )