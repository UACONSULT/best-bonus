import datetime

from django.db import models
from django.db.models import Q


SUPLIER_TYPES = (
    (0, 'Casino'),
    (1, 'Betting'),
    (2, 'CS:GO'),
    (3, 'Other'),
)

BONUS_TYPES = (
    (0, 'Deposit'),
    (1, 'Freespin'),
)



list1 = [124124,23124,324]


class Suplier(models.Model):
    '''
    Testing of doc string 

    INPUT:

    OUTPUT:
    
    '''



    title = models.CharField(max_length=100, verbose_name="Name")
    image = models.ImageField(upload_to="casino_logos/", blank=True, null=True, verbose_name="Suplier image")
    
    ca_license_bool = models.BooleanField(max_length=100, default=False, \
        verbose_name="License Y/N")
    suplier_type = models.IntegerField(choices=SUPLIER_TYPES, default=0)





    def __str__(self):
        return self.title








class Bonus(models.Model):
    two_word_desc = models.CharField(max_length= 300, verbose_name="About the bonus in 2 words", blank=False)    
    
    bonus_digit = models.PositiveSmallIntegerField(verbose_name="Bonus value")
    bonus_desc = models.TextField(blank=True, verbose_name="Bonus description")

    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bonus_images/', blank=True, null=True, verbose_name='Bonus image')

# Депозитный или бездепозитный бонус
    dep_bool = models.BooleanField(default=True, blank=False)
    dep = models.PositiveSmallIntegerField(blank = False)

# Date of adding
    doa = models.DateField(default=datetime.date.today)
    ttl = models.SmallIntegerField(default=7, blank=True, null=True, verbose_name='Amount of days to bonus expiring')


    wager = models.SmallIntegerField(default=0, blank=True, verbose_name='Bonus wager')
    bonus_type = models.IntegerField(choices=BONUS_TYPES, default=0)

    class Meta:
        ordering = ['-bonus_digit']

    def __str__(self):
        return f'{self.suplier.title}:{self.two_word_desc}'



# Returns other bonuses of instance casino
    def otherBonuses(self):
        suplier_instance = self.suplier.bonus_set.all()

        return suplier_instance

# Filters

# Отрезок по размеру депозита. value1 - мин значение, value2 - макс значение
def depositRange(value1, value2):
    values_up = set(models.Bonus.objects.filter(dep >= value1))
    values_down = set(models.Bonus.objects.filter(dep <= value2))

    values_sum = values_up.intersection(values_down)
    
    return values_sum

# Отрезок по размеру бонуса. value1 - мин значение, value2 - макс значение
def bonusRange(value1, value2):
    pass






# Все бездепозитные бонусы
def nodepAll():
    values = models.Bonus.filter(dep_bool = False)

    return values


# Только бонусы от лицензионных казино
def onlyLicense():

    return values

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



# Takes deserialized JSON response array 
def filterObjReader(obj):
    parsed_obj = { key:value for (key, value) in [o.values() for o in obj] }

    # Type cheking
    if 'type' in parsed_obj and parsed_obj['type'] != 'all':
        print('NE RAVNO ALL I EST NAHUIII...................................\n\n\n')
        obj_type = parsed_obj['type']
        supliers_result = Suplier.objects.filter(FILTER_LIST['type'][obj_type])
    else:
        supliers_result = Suplier.objects.all()
    
    # License checking 
    if 'license' in parsed_obj:
        supliers_result = supliers_result.filter(FILTER_LIST['license'])

#
# /CREATE HERE ANY FILTERS FOR SUPLIER MODEL






# /
#   
    #Transforming suplier data into bonus data    
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

















