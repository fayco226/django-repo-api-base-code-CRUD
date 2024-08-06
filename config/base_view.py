from django.db import transaction
from django.http import JsonResponse
import json
from rest_framework import viewsets


class BaseView( viewsets.ViewSet):
    def get_repository(self, ressource):
        raise NotImplementedError("Cette méthode doit être implémentée dans les classes filles")
    
    def get_url_element(self, request, element):
        return request.resolver_match.kwargs.get(element)

    def get_one(self, request, **kwargs):
        print(request.resolver_match.kwargs.get('ressource'))
        repository = self.get_repository(self.get_url_element(request,'ressource'))
        options = {
            'filters': json.loads(request.GET.get('filters', '{}')),
            'fields': request.GET.get('fields', '').split(',') if request.GET.get('fields') else ['*']
        }
        
        try:
            result = repository.get_one(options)
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get_many(self, request, **kwargs):
        # print(request.resolver_match.kwargs.get('ressource'))
        ressource = self.get_url_element(request,'ressource')
        repository = self.get_repository(ressource)
        
        options = {
            'filters': json.loads(request.GET.get('filters', '{}')),
            'fields': request.GET.get('fields', '').split(',') if request.GET.get('fields') else ['*'],
            'criterias': json.loads(request.GET.get('criterias', '{}')),
            'search': request.GET.get('search'),
            'search_criterias': self.get_criterias(ressource),
            'count': request.GET.get('count') == 'true',
            'offset': int(request.GET.get('offset', 0)),
            'limit': int(request.GET.get('limit', 100))
        }
        
        try:
            result = repository.get_all(options)
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    @transaction.atomic
    def store(self, request, ressource=None):
        ressource = request.resolver_match.kwargs.get('ressource')
        repository = self.get_repository(ressource)
        data = json.loads(request.POST.get('data', '{}'))
        print(data)
        
        try:
            entity = repository.store(data)
            return JsonResponse({'status': 'success', ressource: entity})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    @transaction.atomic
    def save(self, request, ressource=None, id=None):
        repository = self.get_repository(self.get_url_element(request,'ressource'))
        instance_id = self.get_url_element(request,'id')
        data = json.loads(request.POST.get('data', '{}'))
        
        try:
            entity = repository.save(instance_id, data)
            return JsonResponse({'status': 'success', self.get_url_element(request,'ressource'): entity})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    @transaction.atomic
    def delete(self, request, ressource=None, id=None):
        repository = self.get_repository(self.get_url_element(request,'ressource'))
        instance_id = self.get_url_element(request,'id')
        
        try:
            repository.delete(instance_id)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get_criterias(self, ressource):
        return []