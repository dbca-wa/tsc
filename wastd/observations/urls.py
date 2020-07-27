
from django.urls import path
from . import views

app_name = 'observations'

urlpatterns = [
    path('animal-encounters/', views.AnimalEncounterList.as_view(), name='animalencounter-list'),
    path('animal-encounters/create/', views.AnimalEncounterCreate.as_view(), name='animalencounter-create'),
    path('animal-encounters/<int:pk>/', views.AnimalEncounterDetail.as_view(), name='animalencounter-detail'),
    path('animal-encounters/<int:pk>/update/', views.AnimalEncounterUpdate.as_view(), name='animalencounter-update'),
]
