# from django.http import Http404
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from Income.models import Income

# from Income.serializers import IncomeSerializer
# # Create your views here.


# class IncomeListView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     # Retrieving all the Incomes
#     def get(self, request, format=None):
#         try:
#             results = (
#                 Income.objects.all()
#                 .filter(user=request.user)
#                 # .filter(date_month = str(current_month))
#             )
#             serializer = IncomeSerializer(results, many = True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except:
#             return Response(
#                 data={"message": "Unable to retrieve income"}, status=status.HTTP_401_UNAUTHORIZED
#             )

    
#     def post(self, request):
#         try:
#             serializer = IncomeSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(user=request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response(
#                 data={"message": "Unable to create income"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )



    

    
# # === IncomeDetailView ===
# class IncomeDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Income.objects.get(pk=pk)
#         except Income.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         income = self.get_object(pk)
#         if request.user == income.user:
#             serializer = IncomeSerializer(income)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             raise Response(data={"message": "Not permitted"}, status=status.HTTP_403_FORBIDDEN)

#     def put(self, request, pk):
#         income = self.get_object(pk)
#         if request.user == income.user:
#             serializer = IncomeSerializer(income, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             raise Http404

#     def delete(self, request, pk):
#         income = self.get_object(pk)
#         if request.user == income.user:
#             income.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             raise Http404





from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from Income.models import Income

from Income.serializers import IncomeSerializer

from rest_framework.filters import SearchFilter, OrderingFilter
from .PaginationFiles.cursorPagination import myPagination
# === Creating and getting all the Incomes using generic API ===

class IncomeListView(ListAPIView, CreateAPIView ):
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    
    # === Adding Search Filter ===
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['note', 'amount', 'created_Date']
    
    # === Adding Pagination ===
    pagination_class = myPagination
    
    
    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-created_Date')
    
    # === Creating/ Posting data
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncomeDetailView(RetrieveUpdateAPIView, DestroyAPIView):
    #=== Adding permission ===
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            return Income.objects.get(pk=pk, user=self.request.user)
        except Income.DoesNotExist:
            raise Http404