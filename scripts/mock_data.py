"""
The script creates mock(fake) data for testing/development purposes


Mock data(fake data) - data for testing current app to see functionality during real work
A word 'mock' and 'fake' have the same meaning in the context of the scipt. 

Suplier - A bonus suplier. E.g. Online-casino, Betting company, CS:GO app, Poker room .......whatever
A word 'casino' and 'suplier' have the same meaning in the context of the scipt. 




To run the scipt:


Exmples of using the scipt for solving real-world issues: 
1) Creating 100 Mock Bonuses
python manage.py runscript mock_data --script-args 10
10 - is FBA(Fake Bonus Amount) argument

2) Creating 0 Mock Bonuses and 10 mock Casinos


3) Deleting all mock data 


4) Deleting certain mock data






?1 - is FCA(Fake Casino Amount) argument. It is not necessary





"""
from random import randrange, randint, choice
from loremipsum import get_sentence

from bestbonus import models


# showBonuses returns all existing bonuses from current DB
def showBonuses():
    # Fetch all bonuses and return them
    all_bonuses = models.Bonus.objects.all()

    return all_bonuses




#
# fba(int) - Fake Bonus Amount. Amount of mock bonuses what will be created.
# e.g. mockData(100) --> Creates(and save) 100 rows(records) of Bonus object.

# fca(int) - Fake Casino Amount. Amount of mock caisnos what will be created.
# e.g. mockData(100, 3) --> Creates(and save) 100 rows(records) of Bonus object and 3 Caisno objects.

#? You can recognise mock data by bonus_name field. If data is mock it always will contain "TESTING RECORD."
def mockData(fba, fca=0):


    # Creates bonus instance for fda(look above to know what FDA means) times
    for b in range(1, int(fba)):

        # Creates bonus filling it with random generated data in some fields 
        mock_object = models.Bonus.objects.create(two_word_desc=f'TESTING RECORD {b}',
        bonus_digit=randrange(100000), bonus_desc=get_sentence(5),
        suplier=models.Suplier.objects.get(pk=randint(1, models.Suplier.objects.count())),
        dep_bool=choice([True, False]), dep=randint(1, 5000), ttl=randint(1,30),
        wager=randint(1,70), bonus_type=choice((0,1)),
        )
        
        print(mock_object)


    # ! BELOW MUST BE THE SAME LOOP CODE FOR CREATING CASINO INSTANCE

    if fca:
        for c in range(1, fca):
            pass

    # ! THE END 

    print(f"\n{fba} records for Bonus model are created successfully!!!")
    print('Check out your DB or go onto the app webpage to see results!!!\n')
    # return



def removeMockData():
    # Function removes all mock data from DB
    # Function fetches mock data by bonus_name filed. 
    # If data is mock it always will contain "TESTING RECORD."
    
    #Fetch testing records



    testing_records = models.Bonus.objects.filter(two_word_desc__contains='TESTING RECORD') 
    print(testing_records)

    # Deletes testing records

    # print('Testing records were deleted successfully!!!')




# !DO NOT TOUCH THE FUNCTION BELOW
# !This file must implement a run() function.
# ?This is what gets called when you run the script
def run(*args):
    print(args)
    mockData(args[0])
    print(showBonuses())