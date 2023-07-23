from django.core.management.base import BaseCommand
from Limit.views import CompareCategoryView
from django.test import RequestFactory
from users.models import myUser
import time

class Command(BaseCommand):
    help = 'Runs the CompareCategoryView function continuously'

    def handle(self, *args, **options):
        #create a request object
        factory  = RequestFactory()
        
        
        while True:
            users = myUser.objects.all()
            for user in users:
                #create a mock request
                mock_request = factory.get('/')
            
                #add a user to the request
                mock_request.user = user
            
                CompareCategoryView().get(mock_request)
                
                # time.sleep(3600)
                
    
                