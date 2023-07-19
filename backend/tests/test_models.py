from django.test import TestCase
from users.models import myUser
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase,APIClient
from product.models import Product
from order.models import Order,UserSubscription


class ProductTestModels(TestCase):
    
    def setUp(self):
        self.product1 = Product.objects.create(name="Premium", price=99.0,description =" this is a premium product")
    
    def test_product_is_created(self):
        self.assertEquals(self.product1.name,"Premium")
        self.assertEquals(self.product1.price,99.0)
        self.assertEquals(self.product1.description," this is a premium product")

class OrderTestModuel(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.test_user = myUser.objects.create_superuser(
                email="nischal10@gmail.com",
                username="admin",
                password="admin1234",
                fName="admin",
                lName="thapa",
                tc=True,
                date_of_birth="1998-12-29",
                phone="9876554321",
            )
        self.client.force_authenticate(user=self.test_user)
        self.product1 = Product.objects.create(name="Premium", price=99.0,description =" this is a premium product",user=self.test_user)
        self.order1= Order.objects.create(product = self.product1,total_amount=99.00,payment_status = "Unpaid",payment_mode='Card',price=99.00,quantity=1,user=self.test_user)  

        # try:
        #     self.order1= Order.objects.create(product = 1,total_amount=99.00,payment_status = "Unpaid",payment_mode='Card',price=99.00,quantity=1)  
        # except Exception as e:
        #     print("error crating order table")
        #     print(e)
    # def 
    def test_order_is_created(self):
        self.assertEquals(self.order1.product,self.product1)
        self.assertEquals(self.order1.total_amount,99.00)
        self.assertEquals(self.order1.payment_status,"Unpaid")
        self.assertEquals(self.order1.payment_mode,"Card")
        self.assertEquals(self.order1.price,99.00)
        self.assertEquals(self.order1.quantity,1)