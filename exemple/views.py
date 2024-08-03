from django.shortcuts import render
from django.http import JsonResponse  
from config.base_view import BaseController
from exemple.repository import ExempleRepo
from exemple.models import Exemple

class ExempleController(BaseController):
    def index(self, request):
        data = {'current_page': 'Exemple'}
        return render(request, self.get_index(request.GET.get('resource')), data)

    def display(self, request):
        repository = self.get_repository(request.GET.get('resource'))
        options = {
            'filters': {'id': request.GET.get('id')},
            'fields': ['*']
        }
        
        try:
            data = repository.get_one(options)
            return render(request, f'backoffice/exemple/{self.get_index(request.GET.get("resource"))}/display.html', {
                'id': request.GET.get('id'),
                'resource': request.GET.get('resource'),
                'data': data
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get_repository(self, resource):
        if resource == 'exemples':
            return ExempleRepo(Exemple)
        return None

    def get_index(self, resource):
        if resource == 'exemples':
            return 'backoffice/exemple/index'
        return None