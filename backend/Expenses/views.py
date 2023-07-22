# === Using Generic API
from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

# ==Import from Locals==
from Expenses.models import Expenses
from Expenses.serializers import ExpenseSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from .PaginationFiles.cursorPagination import myPagination


##! === for signal ===
from notifications.signals import notify
# === Creating and getting all Expenses usuing generic API ===
class ExpensesListView(ListAPIView, CreateAPIView):
    
    # ==== Adding Permission ====
    permission_classes = [IsAuthenticated]
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer
    
    # === Adding Search Filter ===
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','note', 'amount', 'created_date']
    
    # === Adding Pagination ===
    pagination_class = myPagination
    
    
    # # === Fetching data created by the user
    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user).order_by('-created_date')

         # .filter(date__month=str(current_month))
#                 .order_by("id")
    
    
    
    # === Creating/ Posting data
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        notify.send(self.request.user, recipient=self.request.user, verb='limit_almost_spent', target=serializer.instance, description="80 percent of the budget used")
        



# === Class that handles specific Expenses ===
class ExpensesDetailView(RetrieveUpdateAPIView, DestroyAPIView):
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            return Expenses.objects.get(pk=pk, user=self.request.user)
        except Expenses.DoesNotExist:
            raise Http404
        
        
        

# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve notifications for the currently logged-in user
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        
        # Serialize the notifications and return the response
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)