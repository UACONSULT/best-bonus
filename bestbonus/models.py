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

#? Functions used in tests, scripts help to find min/max values for range sliders
# Wager max value
def wagerMax():
    pass

# Deposit max value
def depMax():
    pass

# Bonus max value
def bonusMax():
    pass



# Takes deserialized JSON response array and returns a parsed dict for FilterMechanism 
# e.g of parsingObject in action
"""
.................parsingObject: UNPARSED(list)
[{'name': 'sorting', 'value': 'dep_min_to_max'}, 
{'name': 'type', 'value': 'all'}, 
{'name': 'wager-js-range-slider', 'value': '0;42'}, 
{'name': 'bonus-js-range-slider', 'value': '0;5000'}, 
{'name': 'deposit-js-range-slider', 'value': '0;10000'}]


.................parsingObject: PARSED(dict)
{'sorting': 'dep_min_to_max', 'type': 'all', 'wager-js-range-slider': '0;42',
 'bonus-js-range-slider': '0;5000', 'deposit-js-range-slider': '0;10000'}

"""
# Argument 'unparsed_obj' is JSON array rendered by main.js
def parsingObject(unparsed_obj):
    # Nested dict comprehension
    parsed_obj = { key:value for (key, value) in [o.values() for o in unparsed_obj] }

    return parsed_obj


# This function is an interface between views and FilterMechanism(models)
# Takes as an argument unparsed_json. Unparsed JSON - JSON Array with filter params we gotta apply
#       and fetch proper Bonus QuerySet by these filter params 
# Returns Bonus QuerySet    
def mainFilterWay(unparsed_json):
    # Input data should be parsed(by parsingObject function, see above) JSON object
    # {'sorting': 'dep_min_to_max', 'type': 'all', 'wager-js-range-slider': '0;42',
    #  'bonus-js-range-slider': '0;5000', 'deposit-js-range-slider': '0;10000'}

    # Parsing unparsed_json. Contains readable for FilterMechanism Class filter values  
    obj = parsingObject(unparsed_json) 

    # Returns Bonus QuerySet by taken filter values from parsed JSON/    
    result_query = FilterBox(obj).render()
    
    return result_query



# This class is abstract class. It provides us flexible filter capabilities
# Class provides us completed methods for filtering and sorting.

# All you need to attach this to your filter: 
# 1) Create Child-Class(it should ingerites FilterMechanism Class) for your Filter
# 2) Write in Child CLass your own render method with Parent Class methods for your purposes

# Parent Class returns nothing it just provides methods for filtering and sorting and environment for 
#   sharing result QuerySet(Bonus/Suplier)
# ! BE CAREFULL: 
# ! PAY ATTENTION TO QUERYSET MODEL YOU ARE WORKING WITH. There BONUS QuerySet and Suplier QuerySet.
# !     Do not mix it. To conversion there is provided 'suplier_to_bonus_converting' method
class FilterMechanism:

    # Mapping filters and fitler data or Q objects
    # ? If you wanna add new filter/sorting. ADD HERE.

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
            # 'ttl_min_to_max': 'ttl',
            # 'ttl_max_to_min': '-ttl',
        },

        'type': {
            'casino': Q(suplier_type=0),
            'betting': Q(suplier_type=1),
        },


        # ?Suplier checkboxes
        'license': Q(ca_license_bool=True),
        # 'safe': ,
        # 'fresh':,

        # ?Bonus checkboxes
        'nodep': Q(dep_bool=False),  
        # 'season': Q(),
        
    }
    
    def __init__(self, parsed_JSON):
        self.parsed_JSON = parsed_JSON

# ?VITAL method. Creates first instance of result QuerySet(Suplier)
# Fetches Suplier instances by certain type.
# e.g. Casino/Betting/All. Fetches all Casino Suplier instances(all casinos in current DB)
    def fetchType(self):

        # Type cheking
        # Creates self.resultQuery. Result QuerySet with Supliers taken by filter 'type' 
        if 'type' in self.parsed_JSON and self.parsed_JSON['type'] != 'all':
            _ = self.parsed_JSON['type']
            self.resultQuery = Suplier.objects.filter(FilterMechanism.FILTER_LIST['type'][_])
        else:
            # Happens if 'type' is 'all' or something got wrong
            self.resultQuery = Suplier.objects.all()

        # It also cant return result Suplier QuerySet 
        return self.resultQuery

# Apply checkboxes for Suplier model
    def checkboxSuplierFilter(self):
        # ? Vital note. The method gotta be called before conversion 

        # License checking
        if 'license' in self.parsed_JSON:
            self.resultQuery = self.resultQuery.filter(FilterMechanism.FILTER_LIST['license'])
        # CREATE HERE ANY FILTERS FOR SUPLIER MODEL

        #        

# Apply checkboxes for Bonus model
    def checkboxBonusFilter(self):
        # ? Vital note. The method gotta be called after conversion 
        
        # Nodep checking 
        if 'nodep' in self.parsed_JSON:
            self.bonuses_result = self.bonuses_result.filter(FilterMechanism.FILTER_LIST['nodep'])
        # CREATE HERE ANY FILTERS FOR BONUS MODEL
        
        #

# Apply range slider filters for result Bonus QuerySet 
    def wagerFilter(self):
        # Range sliders
        self.bonuses_result = self.bonuses_result.filter( 
            Q(wager__range = self.parsed_JSON['wager-js-range-slider'].split(';')) &\
            Q(dep__range = self.parsed_JSON['deposit-js-range-slider'].split(';')) &\
            Q(bonus_digit__range = self.parsed_JSON['bonus-js-range-slider'].split(';')) \
            # If you wanna add a new range-slider, just add below

            )

# Sorting
    def sorting(self):
        # It gotta be occured after all filters in the order.
        self.bonuses_result = self.bonuses_result.order_by(FilterMechanism.FILTER_LIST['sorting'][self.parsed_JSON['sorting']])
        

# Converts Suplier result queryset to Bonus result query set
# It is a vital method, cause we should return to django templates Bonus queryset
    def _suplier_to_bonus_converting(self):
        #! Just do not touch this method
        #? Pretty weird way to merge 2 querysets. Look for a better decision 
        self.bonuses_result = Bonus.objects.none()
        
        for suplier in self.resultQuery:
            self.bonuses_result =  self.bonuses_result | suplier.bonus_set.all()
        
        return self.bonuses_result

# Method for query by name fetching
# e.g. SearchBox 
    def searchFilter(self, query): 
        pass

    def __str__(self):
        return self.resultQuery
    
# FILTERING ROADMAP:
#
# 1) We gotta filter by selected Suplier type(Casino/Betting/All...)
# We fetch type results first and then work with results
# 2) Check and apply Suplier checkboxes
# 
# ?4) Converting Suplier result Query Set into Bonus result Query Set
# ? Pay attention we work with Suplier Queryset before conversion. 
# And after conversion we work with Bonus Result QuerySet 
#
# 5) Check and apply Bonus checkboxes
# 6) Aplly Range sliders params(wager, bonus, deposit.....)
# 
# 7) Sorting Bonus Query Set result 
#
# SCHEME OF FILTERING(this is how FilterBox render method works) 
#   TYPE -> SUPLIER CHECKBOXES -> COVERSION -> BONUS CHECKBOXES -> RANGE SLIDERS\
#               -> SORTING ----> Result Bonus Queryset 
#

# Class creates filter construction with applying in certain order.
# FilterBox class is a child class of FilterMechanism
# ! One filter - one instance
# # e.g. FilterBox instance that constructs SearchBox\FilterBox\..
# ......whatever what has to search\fetch\find\sort smt 
class FilterBox(FilterMechanism):
    def __init__(self, parsed_JSON):
        self.parsed_JSON = parsed_JSON
        # invokes FilterMechanism.__init__
        super().__init__(parsed_JSON)
        
# ?Vital method. The method creates filter construction and defines order of applying
# You can see example of using this class and method above
# Remember. Order - is super important here.
    def render(self):
        # Type filter
        # It always gotta be first in the order.
        # It creates flow object(resultQuery/bonusQuery....the var contains our result QuerySet)
        self.suplier_query = self.fetchType()
        self.checkboxSuplierFilter()
        # Add code below if you wanna add smt for Suplier model


        # Converting flow object from suplier to bonus
        self._suplier_to_bonus_converting()
        
        self.checkboxBonusFilter()
        # Add code below if you wanna add smt for Bonus model


        # Silder-range filters
        self.wagerFilter()
        
        # Sorting. Sorting uses always last in the order
        self.sorting()


        # Returns Bonus Query Set
        # It takes self.bonus_result(aka flow object) from Class attributes. When any method calls, it rewrites flow object
        return self.bonuses_result

    def __str__(self):
        return self.bonuses_result

# Class for searching
class SearchBox(FilterMechanism):
    pass
