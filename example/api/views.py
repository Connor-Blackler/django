from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project


@api_view(["GET"])
def get_routes(request):
    routes = [
        {"GET": "api/projects"},
        {"GET": "api/projects/id"},
        {"POST": "api/projects/id/vote"},
        {"POST": "api/users/token"},
        {"POST": "api/users/token/refresh"},
    ]

    return Response(routes)


@api_view(["GET"])
def get_projects(request):
    my_projects = Project.objects.all()
    my_serializer = ProjectSerializer(my_projects, many=True)

    return Response(my_serializer.data)


@api_view(["GET"])
def get_project(request, pk):
    my_project = Project.objects.get(pk=pk)
    my_serializer = ProjectSerializer(my_project, many=False)

    return Response(my_serializer.data)
