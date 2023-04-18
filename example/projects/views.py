from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {
    'id':'1',
    'title':'Ecommerce Website',
    'description':'A fully functional Ecommerce website'
    },
    {
    'id':'2',
    'title':'Portfolio Website',
    'description':'This was a project where I built out my portfolio'
    },
    {
    'id':'3',
    'title':'Social Network',
    'description':'Awesome open source project I am still working on'
    },
]

def projects(request):
    page = "projects"
    number = 11

    context = {"page":page, "number": number, "projects":projectsList}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_object = None
    for i in projectsList:
        if i['id'] == pk:
            project_object = i
    return render(request, 'projects/single-projects.html', {"project":project_object})
