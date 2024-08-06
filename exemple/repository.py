from config.base_repo import BaseRepository
from .models import Exemple, Exemple2
from django.conf import settings
from django.contrib.auth import get_user_model

class ExempleRepo(BaseRepository):
    def __init__(self):
        super().__init__(Exemple)
        
        # self.base_store_data['statut'] = settings.CUSTOM_STATUT_ACTIF
    
      
class Exemple2Repo(BaseRepository):
    def __init__(self):
        super().__init__(Exemple2)
        
        # self.base_store_data['statut'] = settings.CUSTOM_STATUT_ACTIF
        
    def get_current_user_email(self):
        User = get_user_model()
        return User.objects.get(id=self.request.user.id).email if self.request.user.is_authenticated else None