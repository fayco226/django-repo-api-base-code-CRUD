from django.shortcuts import render
from django.http import JsonResponse  
from config.base_view import BaseView
from exemple.repository import ExempleRepo, Exemple2Repo

class ExempleView(BaseView):
    def index(self, request, ressource=None):
        data = {'current_page': 'Exemple'}
        return render(request, self.get_index(self.get_url_element(request,'ressource')), data)

    def display(self, request):
        repository = self.get_repository(self.get_url_element(request,'ressource'))
        options = {
            'filters': {'id': self.get_url_element(request,'id')},
            'fields': ['*']
        }
        
        try:
            data = repository.get_one(options)
            return render(request, f'backoffice/exemple/{self.get_index(request.GET.get("ressource"))}/display.html', {
                'id': self.get_url_element(request,'id'),
                'ressource': self.get_url_element(request,'ressource'),
                'data': data
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get_repository(self, ressource):
        if ressource == 'exemples':
            return ExempleRepo()
        if ressource == 'exemples2':
            return Exemple2Repo()
        return JsonResponse({'status': 'error', 'message': "Ressources inexistant"}, status=404)

    def get_index(self, ressource):
        if ressource == 'exemples':
            return 'index.html'
        return None