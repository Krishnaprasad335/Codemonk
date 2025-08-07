from django.urls import path
from .views import ParagraphCreateView, ParagraphWordSearchAPIView

urlpatterns = [
    path("", ParagraphCreateView.as_view(), name="paragraph-create"),
    path("search/", ParagraphWordSearchAPIView.as_view(), name="paragraph-search"),
]
