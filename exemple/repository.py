from config.base_repo import BaseRepository
from .models import Exemple
from django.conf import settings
from django.contrib.auth import get_user_model

class ExempleRepo(BaseRepository):
    def __init__(self):
        super().__init__(Exemple)
        
        self.base_store_data['statut'] = settings.CUSTOM_STATUT_ACTIF
        self.base_store_data['created_by'] = self.get_current_user_email()
        self.base_store_data['updated_by'] = self.get_current_user_email()
        
        self.base_save_data['updated_by'] = self.get_current_user_email()
    
    def get_current_user_email(self):
        User = get_user_model()
        return User.objects.get(id=self.request.user.id).email if self.request.user.is_authenticated else None