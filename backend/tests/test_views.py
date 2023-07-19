from rest_framework.authtoken.models import Token
from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product
import json
from users.models import myUser
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
 

class TestViews(APITestCase):
    def setUp(self):  # * ---setup code
        self.client = APIClient()
        self.products_url = reverse("get-all-products")
        self.product1 = Product.objects.create(name="Premium", price=99.0,description =" this is a premium product")
        self.product_url = reverse("get-product-pk", kwargs={"pk": 1})
        self.add_product_url = reverse("add-product")
        self.update_product_url=reverse("update-product",kwargs={"pk":1})
        self.delete_product_url = reverse("delete-product", kwargs={"pk": 1})

        #! --- ------------ For authentication --------->
        try:
            self.test_user = myUser.objects.create_superuser(
                email="nsichal10@gmail.com",
                username="admin",
                password="admin1234",
                fName="admin",
                lName="thapa",
                tc=True,
                date_of_birth="1998-12-29",
                phone="9876554321",
            )
            self.client.force_authenticate(user=self.test_user)
            t = myUser.objects.get(username="admin")
            print("user created",t.username)
        except Exception as e:
            print("error creating a user")
            print(e)
        
        try:
            self.product1 = Product.objects.create(
            name="Premium", 
            price=99.0,
            description =" this is a premium product",
            user=self.test_user  # assign the test user as the user of the product
        )
        except Exception as e:
            print("error creating a product")
            print(e)
            
    def test_views_get_products(self):
        response = self.client.get(self.products_url)  # * ---- test code
        self.assertEquals(response.status_code, 200)  # * ----- assertion codes

    def test_views_get_single_product(self):
        response = self.client.get(self.product_url)
        self.assertEquals(response.status_code, 200)

    def test_views_add_product(self):
        format_ = {
            "product": [
                {
                    "name": "Premium",
                    "description": "Features for ever",
                    "price": 12900
                }
            ]
        }

        response = self.client.post(self.add_product_url, data=format_, format="json")
        self.assertEquals(response.status_code, 200)

    def test_views_update_product(self):
        format_ = {
            "price": 5999,
            "name": "Premium",
            "description": "All you'll ever need",
        }
        
        response = self.client.put(self.update_product_url, data=format_, format="json")
        print("Response Content:", response.content)
        print("Response Status Code:", response.status_code)
        self.assertEquals(response.status_code, 200)

    def test_views_delete_product(self):
        response = self.client.delete(self.delete_product_url)
        self.assertEquals(response.status_code, 204)