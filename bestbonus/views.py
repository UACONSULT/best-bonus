import json

from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from bestbonus import models



# / view. 
# Returns main page, returns JSON paginated bonuses when user triggers pagination button
# Paginates all bonuses, shows sweet bonuses(no dep).
# Checks if request is AJAX. Send JSON with next paginated page with bonuses
def bonusRating(request):
    bonuses = models.Bonus.objects.all()

    # Paginator paginates 6 bonuses
    paginator = Paginator(bonuses, 6)
    page = request.GET.get('page', 1)

    paginated_bonuses = paginator.get_page(page)
    
# Executes if an user clicked paginator button(like 'show more'....whatever)
# Check out main.js to see how AJAX works that
    if request.is_ajax():
        data = {}
        # If current page(like 1,2,3..) is out of paginated pages count
        # str -> int
        if int(page) >= paginator.num_pages:
            # It says to main.js when paginated bonuses are out then we have to hide paginator button
            data['paginator_hiding'] = True
                
        # Testing records 
        data['page'] = page
        data['num_pages'] = paginator.num_pages 
        
        # Renders a string with html code of 'cardblock.html' template.
        # Loads new 'data' context with next page of paginated bonuses
        data["html_from_view"] = render_to_string(
            template_name="cardblock.html", 
            context={
                'bonuses': paginated_bonuses,
        
                'bonuses_meta' : {
                    'count': paginator.count,
                    'title' : "Самые выгодные бонусы",
                    'description' : 'В разделе расположены бесплатные и выгодные бонусы для пользователя......блабла',
                },
                #? Rudiment attribute. It should be implemented by .._meta
                'bonuses_count': paginated_bonuses.count,
                }
        )

        return JsonResponse(data=data)
    
# If request is not AJAX(event was not triggered)
# Just returns first all bonuses paginator page 

#! Think about adding a paginaotr to sweet bonuses
# And returns all sweet bonuses
# Sweet bonuses = no dep bonuses
    sweet_bonuses = models.Bonus.objects.filter(dep_bool=False)

    context = {
        'bonuses' : paginated_bonuses,
        'bonuses_meta' : {
            'count': paginator.count,
            'title' : 'Самые выгодные бонусы',
            'description' : 'В разделе расположены бесплатные и выгодные бонусы для пользователя......блабла',
        },
#? Rudiment attribute. It should be implemented by .._meta
        'bonuses_count' : paginator.count, 

        'sweet_bonuses' : sweet_bonuses,
        'sweet_bonuses_meta': {
            'count' : sweet_bonuses.count,
            'title' : "Самые выгодные бонусы",
            'description' : 'В разделе расположены бесплатные и выгодные бонусы для пользователя......блабла',
        },
#? Rudiment attribute. It should be implemented by .._meta
        'sweet_bonuses_count' : sweet_bonuses.count,
    } 

    return render(request, 'base.html', context=context)


# Calls when user types some query text into search input. Works using AJAX
# Looks up bonuses comparing the query and return result JSON 
def ajaxSearch(request):
# Search input data
    search_query = request.GET.get('q', False)

# Marker variable
# Shows filter is called from filter-box
# Why do we use this var instead of 'form-data'??
# 'form-data' provides a non-empty object. So we cannot capture when when we have to work with it 
    filter_ = request.GET.get('filter', False)
    data = {}

    if request.is_ajax():
# AJAX can work with filter or search
# Checks if filter is triggered. So if it returns JSON response with a template what contains filtered bonus queryset
# If not, it returns JSON response filtered by search input query
        if filter_:
# Filtering
            # Deserialization JSON object
            # 'form_data' contains different filter params what we need to apply to Filter Mechanism
            form_data = json.loads(request.GET.get('form_data'))

            # mainFilterWay - rendering function of Filter Mechanism for filter-box
            # Returns bonus queryset what fits filter params('form_data'))
            bonuses = models.mainFilterWay(form_data)
 
            data['html_from_view'] = render_to_string(
                template_name="cardblock.html", 
                context={
                    'bonuses': bonuses,
                    
                    'bonuses_meta' : {
                        'count': bonuses.count,
                        'title' : "Бонусы по вашему запросу",
                        'description' : 'Бонусы по вашему запросу, самые прикольные......блабла',
                    },
                    #? Rudiment attribute. It should be implemented by .._meta
                    'bonuses_count': bonuses.count,
                    }
            )
            return JsonResponse(data=data)
# Searching

# searchFilterWay - a rendering Filter Mechanism function for search input
# Returns bonus queryset what fits search input
        bonuses = models.searchFilterWay(search_query)

        data['html_from_view'] = render_to_string(
            template_name="cardblock.html", 
            context={
                'bonuses': bonuses,
                'bonuses_meta' : {
                        'count': bonuses.count,
                        'title' : "Бонусы по вашему поиску",
                        'description' : 'Обнаруженые бонусы по вашему запросу!!!........',
                    },
                    #? Rudiment attribute. It should be implemented by .._meta
                'bonuses_count': bonuses.count,                
                }
        )
        return JsonResponse(data=data)
