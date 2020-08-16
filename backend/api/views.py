from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, generics

from .models import Issue, IssueSerializer, IssueSerializerWithChildren, Platform


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class RootIssueView (generics.ListAPIView):
    queryset = Issue.objects.filter(parents=None)
    serializer_class = IssueSerializer


class IssueViewSet (viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializerWithChildren