import datetime

from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator

SUPLIER_TYPES = (
    (0, 'Casino'),
    (1, 'Betting'),
    (2, 'CS:GO'),

)

BONUS_TYPES = (
    (0, 'Deposit'),
    (1, 'Freespin'),

)


'''
Suplier/Casino entity describes app/compnay/resource what distributes bonuses.
e.g. Online casino, Betting company, Gambling app, .......

'''
class Suplier(models.Model):

    title = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Name")
    image = models.ImageField(upload_to="casino_logos/", blank=True, null=True, verbose_name="Suplier image")
    
    ca_license_bool = models.BooleanField(default=False, verbose_name="License")
    suplier_type = models.IntegerField(choices=SUPLIER_TYPES, default=0)


    def __str__(self):
        return self.title




# Created for DOE field default in Bonus model 
# Yeah, i know it might not be quite pythonic decision, but Django does not serialize lambda functions
def today_plus_30_days():
    return datetime.date.today() + datetime.timedelta(days=30) 

'''
Bonus entity bonus with some informative attributes for gambling dawgs
e.g. 100% No dep bonus for 365bet.......
    
'''
class Bonus(models.Model):
    two_word_desc = models.CharField(max_length=300, blank=False, verbose_name="About the bonus in 2 words")    
    
# If we have freespin for example, the value should be equals zero
    bonus_digit = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(1000000)],\
        verbose_name="Bonus value")
    bonus_desc = models.TextField(max_length=1500, blank=True, null=True, verbose_name="Bonus description")
    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bonus_images/', blank=True, null=True, verbose_name='Bonus image')

# Deposit or non-dep 
    dep_bool = models.BooleanField(default=True, blank=False)
    dep = models.PositiveSmallIntegerField(blank = False)

# Date of adding
    doa = models.DateField(default=datetime.date.today, verbose_name="Date of adding")
# Date of expiring    
    doe = models.DateField(default=today_plus_30_days, verbose_name="Date of expiring")

    wager = models.SmallIntegerField(default=0, blank=True, \
        validators=[MaxValueValidator(100)], verbose_name='Bonus wager')
    bonus_type = models.IntegerField(choices=BONUS_TYPES, default=0)


# Shows time-to-live of bonus(how much time you have to use the bonus til it expires)
# Checks DOE is not less than DOA. If it less it returns None.
# Returns datetime.date
    def ttl_full(self):
        try:
            # If Date of expiring for some reasons is earlier than date of adding =
            #   - it equals DOE value to DOA value. So ttl is 0, but it will bypass a bunch of issues
            if self.doe < self.doa:
                self.doe = self.doa
                self.save()
            # Way to retrive 'time to live'
            ttl_obj = self.doe - self.doa
            return ttl_obj
        # If something got wrong it will return 0 
        except:
            print('....Some exception raised!!!')
            return 0

# Method retuns time-to-live bonus value in days
# Calls ttl_full methond(because it checks DOE and DOA distinction)
    def ttl_days(self):
        date_object = self.ttl_full()
        return date_object.days

# Method retuns time-to-live bonus value in hours
    def ttl_hours(self):
        date_object = self.ttl_full()
        return date_object.days * 24


# Returns related bonuses to our casino instance
    def otherBonuses(self):
        return self.suplier.bonus_set.all()


    class Meta:
        ordering = ['-bonus_digit']

    def __str__(self):
        return f'{self.suplier.title} : {self.two_word_desc}'




# Отрезок по размеру депозита. value1 - мин значение, value2 - макс значение
def depositRange(value1, value2):
    values_up = set(models.Bonus.objects.filter(dep >= value1))
    values_down = set(models.Bonus.objects.filter(dep <= value2))

    values_sum = values_up.intersection(values_down)
    
    return values_sum


# Sorting


FILTER_LIST = {
    'sorting': {
        'bon_max_to_min': 'dep',
        'bon_min_to_max': '-dep',
        'dep_min_to_max': 'bonus_digit',
        'dep_max_to_min': '-bonus_digit',
        'doa_old_to_new': 'doa',
        'doa_new_to_old': '-doa',
        'wager_min_to_max': 'wager',
        'wager_max_to_min': '-wager',
        'ttl_min_to_max': 'ttl',
        'ttl_max_to_min': '-ttl',


    },

    'license': Q(ca_license_bool=True),
        # 'safe': ,
    # 'fresh':,
    'nodep': Q(dep_bool=False),  
        # 'season': Q( =True),
    # 'season': Q(),
    'type': {
        'all': '',
        'casino': Q(suplier_type=0),
        'betting': Q(suplier_type=1),
    },
    # 'wager-js-range-slider': Q(wager__range=(start_date, end_date)),
    # 'deposit-js-range-slider': Q(wager__range=(start_date, end_date)),
    # 'bonus-js-range-slider': Q(wager__range=(start_date, end_date)),
}




# Argument 'filter_array' is filter form list data rendered by main.js
# def ajaxFitlerLoader(filter_array):
#     for obj in filter_array:
#         if obj['name'] in FILTER_LIST.keys():


#! Okay, we gotta refactor the function below(mainFilter way)
#! mainFilterWay describes the proper way and order of executing filter functions  
#!  describes the proper way and order of executing filter functions  
#! mainFilterWay describes the proper way and order of executing filter functions  



#!? Also you may think about release the filter and sorting using class
# Takes deserialized JSON response array 
#! Cover by tests(takes unproper object,)
def filterObjReader(obj):
    # Nested dict comprehension
    #! Cover by tests(cannot parse the object)
    parsed_obj = { key:value for (key, value) in [o.values() for o in obj] }

    # Type cheking
    #! Cover by tests(type is not in parsed_obj)
    #! Delete cruft and not informative prints, comments, whitespaces
    if 'type' in parsed_obj and parsed_obj['type'] != 'all':
        print('NE RAVNO ALL I EST NAHUIII...................................\n\n\n')
        obj_type = parsed_obj['type']
        supliers_result = Suplier.objects.filter(FILTER_LIST['type'][obj_type])
    else:
        supliers_result = Suplier.objects.all()
    
    # License checking
    #!
    if 'license' in parsed_obj:
        supliers_result = supliers_result.filter(FILTER_LIST['license'])

#
# /CREATE HERE ANY FILTERS FOR SUPLIER MODEL






# /
#   
    #Transforming suplier data into bonus data
    # ! Pretty strange way to merge 2 querysets. Look for a better way 
    
    bonuses_result = Bonus.objects.none()
    for suplier in supliers_result:
        bonuses_result = bonuses_result | suplier.bonus_set.all()


    # bonuses_result = list(set(bonuses_result))

    # Nodep checking 
    if 'nodep' in parsed_obj:
        bonuses_result = bonuses_result.filter(FILTER_LIST['nodep'])
    
    # if 'season' in parsed_obj:
    #     bonuses_result = bonuses_result.filter(FILTER_LIST['season'])
    # if 'fresh' in parsed_obj:
    #     bonuses_result = bonuses_result.filter(FILTER_LIST['season'])


    # Wager settings

    bonuses_result = bonuses_result.filter( 
        Q(wager__range = parsed_obj['wager-js-range-slider'].split(';')) &\
        Q(dep__range = parsed_obj['deposit-js-range-slider'].split(';')) &\
        Q(bonus_digit__range = parsed_obj['bonus-js-range-slider'].split(';')) \
        )


    # 'wager-js-range-slider': Q(wager__range=(start_date, end_date)),
    # 'deposit-js-range-slider': Q(wager__range=(start_date, end_date)),
    # 'bonus-js-range-slider': Q(wager__range=(start_date, end_date)),



# /CREATE HERE ANY FILTERS FOR BONUS MODEL






#
#   

    # Sorting
    bonuses_result = bonuses_result.order_by(FILTER_LIST['sorting'][parsed_obj['sorting']])



    print('BONUSES RESULT ::::::...................................\n\n\n')
    print(bonuses_result)
    print(parsed_obj)
    print('...................................\n\n\n')




    return bonuses_result



#! 

def mainFilterWay():
    

    pass













