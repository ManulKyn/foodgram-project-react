from django.urls import path

from .views import (RecipeDetailView, RecipeUpdateView,
    RecipeCreateView, RecipeDeleteView, ProfileView,)

urlpatterns = [
    path(
        'recipes/<slug:slug>/',
        RecipeDetailView.as_view(),
        name='recipe'
    ),
    path(
        'edit/<slug:slug>/',
        RecipeUpdateView.as_view(),
        name='edit'
    ),
    path(
        'create/',
        RecipeCreateView.as_view(),
        name='create'
    ),
    path(
        'delete/<slug:slug>/',
        RecipeDeleteView.as_view(),
        name='delete'
    ),
    path(
        'profiles/<str:username>/',
        ProfileView.as_view(),
        name='profile'
    ),
]
