from rest_framework.authtoken.models import Token
from django.test import TestCase, Client
from django.urls import reverse
from order.models import Order
from product.models import Product
import json
from users.models import myUser
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate


class ProductTestViews(APITestCase):
    def setUp(self):  # * ---setup code
        self.client = APIClient()
        self.products_url = reverse("get-all-products")
        self.product_url = reverse("get-product-pk", kwargs={"pk": 1})
        self.add_product_url = reverse("add-product")
        self.update_product_url = reverse("update-product", kwargs={"pk": 1})
        self.delete_product_url = reverse("delete-product", kwargs={"pk": 1})

        #! --- ------------ For authentication --------->
        try:
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
            # t = myUser.objects.get(username="admin")
            # print("user created",t.username)
        except Exception as e:
            print("error creating a user")
            print(e)

        try:
            self.product1 = Product.objects.create(
                name="Premium",
                price=99.0,
                description=" this is a premium product",
                user=self.test_user,  # assign the test user as the user of the product
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
                {"name": "Premium", "description": "Features for ever", "price": 12900}
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
        # print("Response Content:", response.content)
        # print("Response Status Code:", response.status_code)
        self.assertEquals(response.status_code, 200)

    def test_views_delete_product(self):
        response = self.client.delete(self.delete_product_url)
        self.assertEquals(response.status_code, 204)


class OrderTestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_order_url = reverse("get-all-orders")
        self.order_single_url = reverse("get-single-order", kwargs={"pk": 1})
        self.add_order_url = reverse("add-new-order")
        self.update_order_url = reverse("update-order", kwargs={"pk": 1})
        self.checkout_url = reverse("create-checkout-session")
        #! ========== Authentication ==========>
        try:
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
            # t = myUser.objects.get(username="admin")
            # print("user created",t.username)
        except Exception as e:
            print("error creating a user")
            print(e)

        try:
            self.product1 = Product.objects.create(
                name="Premium",
                price=99.0,
                description=" this is a premium product",
                user=self.test_user,  # assign the test user as the user of the product
            )
        except Exception as e:
            print("error creating a product")
            print(e)

        try:
            self.order1 = Order.objects.create(
                product=self.product1,
                price=99.0,
                quantity=1,
                user=self.test_user,  # assign the test user as the user of the order
                payment_status="Pending",
            )
        except Exception as e:
            print("error creating an order")
            print(e)

    def test_views_get_orders(self):
        response = self.client.get(self.get_order_url)
        self.assertEquals(response.status_code, 200)

    def test_views_get_order(self):
        response = self.client.get(self.order_single_url)
        self.assertEquals(response.status_code, 200)

    def test_view_add_order(self):
        data = {"order": [{"product": 1, "price": 999, "quantity": 1}]}
        response = self.client.post(self.add_order_url, data=data, format="json")
        self.assertEquals(response.status_code, 201)

    def test_view_update_order(self):
        data = {"payment_status": "Paid"}
        response = self.client.put(self.update_order_url, data=data, format="json")
        self.assertEquals(response.status_code, 200)

    def test_view_checkout(self):
        data = {
            "order": [{"name": "Premium", "product": 1, "quantity": 1, "price": 9900}]
        }
        response = self.client.post(self.checkout_url,data=data,format='json')
        self.assertEquals(response.status_code,200)
    
