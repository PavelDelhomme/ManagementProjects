from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Sérialiseur de tâche pour l'API REST de Django REST Framework (DRF)
    """
    class Meta: # définit les champs à inclure dans la sérialisation
        model = Task # le model sur lequel on va travailler (ici Task)
        fields = '__all__' # les champs du model sur lesquels on va travailler (ici tous les champs)
