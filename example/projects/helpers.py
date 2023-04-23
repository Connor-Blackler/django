from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag


def search_projects(request):
    search = ""

    if request.GET.get("search"):
        search = request.GET.get("search")

    tags = Tag.objects.filter(name__icontains=search)

    my_projects = Project.objects.distinct().filter(
        Q(title__icontains=search) |
        Q(description__icontains=search) |
        Q(owner__name__icontains=search) |
        Q(tags__in=tags)
    )

    return my_projects, search


def paginate_projects(request, projects, results_per_page):
    page_number = request.GET.get("page_number")
    my_paginator = Paginator(projects, results_per_page)

    try:
        projects = my_paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        projects = my_paginator.page(page_number)
    except EmptyPage:
        page_number = my_paginator.num_pages
        projects = my_paginator.page(page_number)

    left_index, right_index = max(
        int(page_number) - 4, 1), min(int(page_number) + 5, my_paginator.num_pages + 1)

    custom_range = range(left_index, right_index)

    return custom_range, projects
