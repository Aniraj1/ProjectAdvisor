
from calendar import month_name
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

from Expenses.models import Expenses
from django.db.models import Sum
from datetime import date, datetime, timedelta

from Expenses_Category.models import ExpensesCategory


from .models import Limit
from .serializers import LimitSerializer


### === Creating and Retrieving all Limit ===
class LimitListView(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Limit.objects.all().order_by("-id")
    
    serializer_class = LimitSerializer
    
    def get_queryset(self):
        return Limit.objects.filter(user=self.request.user).order_by("-created_date")
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    


### === Manipulating specific Limits ===
class LimitDetailView(RetrieveUpdateAPIView, DestroyAPIView):
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]
    queryset = Limit.objects.all()
    serializer_class = LimitSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            return Limit.objects.get(pk=pk, user=self.request.user)
        except Limit.DoesNotExist:
            raise Http404



### === Comapring with overall Limit ===
class OverallLimitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_month = date.today().month
        limit = Limit.objects.filter(user=request.user, overall_limit__gt=0).first()
        if limit is None:
            return Response({"message": "Limit not set"}, status=400)

        expenses_total = Expenses.objects.filter(user=request.user, created_date__month=current_month).aggregate(total=Sum('amount'))['total']
        overall_limit = limit.overall_limit

        if expenses_total is None:
            expenses_total = 0

        if overall_limit is None:
            overall_limit = 0

        # Calculate the used limit (0 if within the limit, otherwise the exceeded amount)
        limit_diff = overall_limit - expenses_total
        
        #! === Total Limit left for use
        limit_Left = max(limit_diff, 0)
        
        #! == Total Limit used/spend
        limit_used = overall_limit - limit_Left
        
        #! === category_limit_used in percentage
        limit_used_percent = round(abs(limit_used / overall_limit) * 100, 2) if overall_limit != 0 else 0
        
        #! === Total Expenses after Overall_budget Limit 
        limit_exceeded_by = expenses_total - overall_limit
        #! == Making sure amount is non negative
        limitExceeded = max(limit_exceeded_by, 0)
        
        #! === Total Expenses after Overall_budget Limit in percentage
        limit_exceeded_percent = round(abs(limitExceeded  / overall_limit) * 100, 2) if overall_limit != 0 else 0

        #! === Calculating the budget status ===
        if overall_limit == 0:
            budget_status = "Budget limit not set"
        elif expenses_total <= overall_limit:
            budget_status = "Under the budget"
        else:
            budget_status = "Over the budget"

        data = {
            'Month': month_name[current_month],
            'overall_limit': overall_limit,
            'expenses_total': expenses_total,
            'limit_Left': limit_Left,
            'Limit_used': limit_used,
            'limit_used_percent': limit_used_percent,
            'limit_exceeded_by': limitExceeded,
            'limit_exceeded_percent': limit_exceeded_percent,
            'budget_status': budget_status,
        }

        return Response(data)


### === Comparing with each category with limit ===
class CompareCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_month = datetime.now().month

        categories = ExpensesCategory.objects.filter(user=request.user)
        data = []

        for category in categories:
            category_limit = Limit.objects.filter(user=request.user, expenses_Category=category).first()

            # if category_limit:
            if category_limit and category_limit.category_limit != 0:
                category_limit_value = category_limit.category_limit
                category_expenses_total = Expenses.objects.filter(user=request.user, exCategory=category, created_date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
                
                
                # limit_diff = overall_limit - expenses_total
                
                limit_diff = category_limit_value - category_expenses_total 

                #! === Total Category Limit left for use
                category_limit_Left = max(limit_diff, 0)
               
                               
                #! == Total Category Limit used/spend
                category_limit_used = category_limit_value - category_limit_Left
                
                #! === category_limit_used in percentage
                category_limit_used_percent = round(abs(category_limit_used / category_limit_value) * 100, 2) if category_limit_value != 0 else 0
                
                #! === Total Expenses after Category_budget Limit is spent 
                category_limit_exceeded_by = category_expenses_total - category_limit_value
                #! == Making sure amount is non negative
                category_limit_Exceeded = max(category_limit_exceeded_by, 0)
                
                #! === Total Expenses after Overall_budget Limit in percentage
                category_limit_exceeded_percent = round(abs(category_limit_Exceeded  / category_limit_value) * 100, 2) if category_limit_value != 0 else 0

                
                #! === Calculating the budget status
                budget_status = "Under the Budget" if category_limit_Exceeded <= 0 else "Over the Budget"
                
                
                
                category_data = {
                    'Month': month_name[current_month],
                    'category_name': category.name,
                    'category_limit': category_limit_value,
                    'category_expenses_total': category_expenses_total,
                    'category_limit_Left': category_limit_Left,
                    'category_limit_used': category_limit_used,
                    'category_limit_used_percent': category_limit_used_percent,
                    'category_limit_Exceeded': category_limit_Exceeded,                    
                    'category_limit_exceeded_percent': category_limit_exceeded_percent,
                    'budget_status': budget_status,
                }

                data.append(category_data)

        return Response(data)







# class LimitListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         try:
#             results = Limit.objects.all().filter(user=request.user).order_by("-id")
#             serializer = LimitSerializer(results, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response(
#                 data={"message": "Unable to retrieve settings"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     def post(self, request):
#         serializer = LimitSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LimitDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Limit.objects.get(pk=pk)
#         except Limit.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         limit = self.get_object(pk)
#         if request.user == limit.user:
#             serializer = LimitSerializer(limit)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             raise Http404

#     def put(self, request, pk):
#         settings = self.get_object(pk)
#         if request.user == settings.user:
#             serializer = LimitSerializer(settings, data=request.data, partial = True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             raise Http404

#     def delete(self, request, pk):
#         settings = self.get_object(pk)
#         if request.user == settings.user:
#             settings.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             raise Http404