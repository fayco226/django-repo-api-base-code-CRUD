from django.db import models, transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from rest_framework import serializers
from django.db.models import QuerySet

class BaseRepository:
    def __init__(self, model):
        self.model = model
        self.base_filters = {}
        self.base_orders = [('id', 'asc')]
        self.base_store_data = {}
        self.base_save_data = {}
        
        self.create_route = 'create'
        self.index_route = 'index'
        self.created_message = 'Créé !'
        self.updated_message = 'Mis à jour !'
        self.serializer = BaseSerializer(self.model)

    def get_all(self, options=None):
        if options is None:
            options = {}
        
        filters = {**self.base_filters, **options.get('filters', {})}
        orders = options.get('orders', self.base_orders)
        fields = options.get('fields', ['*'])
        criterias = options.get('criterias', {})
        search = options.get('search')
        search_criterias = options.get('search_criterias', [])
        
        queryset = self.model.objects.filter(**filters)
        
        if criterias:
            queryset = queryset.filter(**criterias)
        
        if search and search_criterias:
            search_query = Q()
            for criteria in search_criterias:
                search_query |= Q(**{f"{criteria}__icontains": search})
            queryset = queryset.filter(search_query)
        
        for order in orders:
            queryset = queryset.order_by(f"{'-' if order[1] == 'desc' else ''}{order[0]}")
        
        if fields != ['*']:
            queryset = queryset.values(*fields)
        
        total = queryset.count() if options.get('count', False) else 0
        
        if 'offset' in options:
            queryset = queryset[options['offset']:]
        if 'limit' in options:
            queryset = queryset[:options['limit']]
        

        result = self.serializer.serialize_list(queryset)
        
        return {'total': total, 'rows': result} if options.get('count', False) else result

    def get_one(self, options):
        filters = options.get('filters', {})
        fields = options.get('fields', ['*'])
        
        try:
            if fields == ['*']:
                result = self.model.objects.filter(**filters).first()
                return self.serializer.serialize_list(result)
            else:
                result = self.model.objects.filter(**filters).values(*fields).first()
                return self.serializer.serialize_list(result)
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération : {str(e)}")

    def before_store(self, inputs):
        return inputs

    @transaction.atomic
    def store(self, inputs):
        inputs = {**inputs, **self.base_store_data}
        inputs = self.before_store(inputs)
        
        isolated_data = inputs.pop('_isolated_', {})
        
        
        # Valider les données d'entrée
        instance = self.model(**inputs)
        instance.save()
        instance_dict = self.serializer.serialize_list(instance)
        if isolated_data:
            inputs['_isolated_'] = isolated_data
        
        return self.after_store({'_store_': instance_dict, **inputs})

    def after_store(self, entity):
        return entity['_store_']

    def before_save(self, id, inputs):
        return inputs

    @transaction.atomic
    def save(self, id, inputs):
        inputs = {**inputs, **self.base_save_data}
        inputs = self.before_save(id, inputs)
        
        isolated_data = inputs.pop('_isolated_', {})
        
        instance = self.model.objects.filter(id=id).first()
        if not instance:
            raise ObjectDoesNotExist("Instance non trouvée")
        
        for key, value in inputs.items():
            setattr(instance, key, value)
        instance.save()
        
        if isolated_data:
            inputs['_isolated_'] = isolated_data
        
        return self.after_save(id, {'_save_': self.serializer.serialize_list(instance), **inputs})

    def after_save(self, id, inputs):
        return inputs['_save_']

    def before_delete(self, id, options):
        return options

    @transaction.atomic
    def delete(self, id):
        options = {'filters': {'id': id}, 'fields': ['*']}
        options = self.before_delete(id, options)
        
        instance = self.get_one(options)
        print(instance)
        if not instance:
            raise ObjectDoesNotExist("Instance non trouvée")
        
        get_object_or_404(self.model, pk=id).delete()
        
        return self.after_delete(id, self.serializer.serialize_list(instance), options)

    def after_delete(self, id, output, options):
        return output

    def validate(self, id):
        self.model.objects.filter(id=id).update(etat='valide')  # Assurez-vous d'avoir un champ 'etat'

    def activate(self, id):
        self.model.objects.filter(id=id).update(statut='actif')  # Assurez-vous d'avoir un champ 'statut'

    def cancel(self, id):
        self.model.objects.filter(id=id).update(statut='inactif')  # Assurez-vous d'avoir un champ 'statut'


class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.Meta.model = self.model
        self.Meta.fields = '__all__'

    class Meta:
        model = None
        fields = None

    @classmethod
    def serialize_list(cls, object_list):
        serializer = cls(model=cls.Meta.model)
        return serializer.to_representation(object_list)

    def to_representation(self, instance):
        if isinstance(instance, QuerySet):
            return [super().to_representation(item) for item in instance]
        return super().to_representation(instance)
