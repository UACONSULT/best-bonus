from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from bestbonus import models
import json


def bonusRating(request):
    context = {}    
    
    bonuses = models.Bonus.objects.all()
    sweet_bonuses = models.Bonus.objects.filter(dep_bool=False)

    context['sweet_bonuses'] = sweet_bonuses
    context['sweet_bonuses_count'] = sweet_bonuses.count

    # context['meta_bonus_info'] = {
        # 'nodep_count': len(sweet_bonuses),
    # }
    
    # Paginator paginates 6 bonuses. You may change the value
    paginator = Paginator(bonuses, 6)
    page = request.GET.get('page', 1)
    
    

    if request.is_ajax():
        
        data = {}
        if int(page) >= paginator.num_pages:
            data['paginator_hiding'] = True
        

        paginated_bonuses = paginator.get_page(page)
        
        data['my_message'] = 'It seems AJAX works here!!!'
        data['page'] = page
        data['num_pages'] = paginator.num_pages 
        
        
        data["html_from_view"] = render_to_string(
            template_name="cardblock.html", 
            context={"bonuses": paginated_bonuses, 'bonuses_count': paginated_bonuses.count}
        )

        return JsonResponse(data=data)
    
    paginated_bonuses = paginator.get_page(page)

    context['bonuses'] = paginated_bonuses
    context['bonuses_count'] = paginator.count
    
    return render(request, 'base.html', context=context)


def ajaxPaginator(request):
    pass

def ajaxFilter(request):
    pass


def ajaxSearch(request):
    url_param = request.GET.get('q', False)
    filter_ = request.GET.get('filter', False)    
    print('............ajaxSEarch \n\n')
    sweet_bonuses = []
    data = {}
    
    if request.is_ajax():
        if filter_:
            print(str(filter_) + '............filterIsTrue \n\n')

            # form_data = request.GET.get('form_data')
            form_data = json.loads(request.GET.get('form_data'))

            print( type(form_data))
            print(form_data)         
            print('............filterIsTrue \n\n')

        #     print('YEP')
            

        #     data['html_from_view'] = render_to_string(
        #         template_name="cardblock.html", 
        #         context={"bonuses": bonuses})
            
            # bonuses = models.filterObjReader(form_data)
            
            # Testing new filter mechanism
            bonuses = models.mainFilterWay(form_data)

            # bonuses = json.dumps(bonuses)
 
            data['html_from_view'] = render_to_string(
                template_name="cardblock.html", 
                context={"bonuses": bonuses}
            )
            return JsonResponse(data=data)



        bonuses = models.Bonus.objects.filter(two_word_desc__icontains=url_param)
 
        data['html_from_view'] = render_to_string(
            template_name="cardblock.html", 
            context={"bonuses": bonuses, 'bonuses_count': bonuses.count}
        )

        return JsonResponse(data=data)


