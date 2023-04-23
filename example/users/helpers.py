from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill


def search_profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query


def paginate_profiles(request, profiles, results_per_page):
    page_number = request.GET.get("page_number")
    my_paginator = Paginator(profiles, results_per_page)

    try:
        profiles = my_paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        profiles = my_paginator.page(page_number)
    except EmptyPage:
        page_number = my_paginator.num_pages
        profiles = my_paginator.page(page_number)

    left_index, right_index = max(
        int(page_number) - 4, 1), min(int(page_number) + 5, my_paginator.num_pages + 1)

    custom_range = range(left_index, right_index)

    return custom_range, profiles
