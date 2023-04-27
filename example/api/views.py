from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag


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
    my_project = Project.objects.get(id=pk)
    my_serializer = ProjectSerializer(my_project, many=False)

    return Response(my_serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def project_vote(request, pk):
    my_project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=my_project,
    )

    if created:
        review.value = data['value']
        review.save()
        my_project.update_vote_count()

    my_serializer = ProjectSerializer(my_project, many=False)
    return Response(my_serializer.data)


@api_view(["DELETE"])
def remove_tag(request):
    tag_id = request.data["tag"]
    project_id = request.data["project"]

    my_project = Project.objects.get(id=project_id)
    my_tag = Tag.objects.get(id=tag_id)

    my_project.tags.remove(my_tag)
    return Response("Tag was deleted")
