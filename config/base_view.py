from django.db import transaction
from django.http import JsonResponse
import json


class BaseController:
    def get_repository(self, resource):
        raise NotImplementedError("Cette méthode doit être implémentée dans les classes filles")

    def get_one(self, request):
        repository = self.get_repository(request.GET.get('resource'))
        options = {
            'filters': json.loads(request.GET.get('filters', '{}')),
            'fields': request.GET.get('fields', '').split(',') if request.GET.get('fields') else ['*']
        }
        
        try:
            result = repository.get_one(options)
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get_many(self, request):
        repository = self.get_repository(request.GET.get('resource'))
        options = {
            'filters': json.loads(request.GET.get('filters', '{}')),
            'fields': request.GET.get('fields', '').split(',') if request.GET.get('fields') else ['*'],
            'criterias': json.loads(request.GET.get('criterias', '{}')),
            'search': request.GET.get('search'),
            'search_criterias': self.get_criterias(request.GET.get('resource')),
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
    def store(self, request):
        repository = self.get_repository(request.POST.get('resource'))
        data = json.loads(request.POST.get('data', '{}'))
        
        try:
            entity = repository.store(data)
            return JsonResponse({'status': 'success', request.POST.get('resource'): entity})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    @transaction.atomic
    def save(self, request):
        repository = self.get_repository(request.POST.get('resource'))
        instance_id = request.POST.get('id')
        data = json.loads(request.POST.get('data', '{}'))
        
        try:
            entity = repository.save(instance_id, data)
            return JsonResponse({'status': 'success', request.POST.get('resource'): entity})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    @transaction.atomic
    def delete(self, request):
        repository = self.get_repository(request.POST.get('resource'))
        instance_id = request.POST.get('id')
        
        try:
            repository.delete(instance_id)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    def get_criterias(self, resource):
        return []

