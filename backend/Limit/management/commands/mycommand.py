from django.core.management.base import BaseCommand
from Limit.views import CompareCategoryView,OverallLimitView
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
                mock_request_1 = factory.get('/limit/OverallLimitView/')
                mock_request_2 = factory.get('/limit/categoryLimitView/')
            
                #add a user to the request
                mock_request_1.user = user
                mock_request_2.user = user
                
                CompareCategoryView().get(mock_request_2)
                OverallLimitView().get(mock_request_1)
                time.sleep(5)
                
            time.sleep(3600)
                
    
                