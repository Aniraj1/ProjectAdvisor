from django.test import TestCase

from product.models import Product
from order.models import Order,UserSubscription


class TestModels(TestCase):
    
    def setUp(self):
        self.product1 = Product.objects.create(name="Premium", price=99.0,description =" this is a premium product")
    
    def test_product_is_created(self):
        self.assertEquals(self.product1.name,"Premium")
        self.assertEquals(self.product1.price,99.0)
        self.assertEquals(self.product1.description," this is a premium product")
        
    # def test_order_is_created(self):
    #     self.assertEquals(self.order1.name,"Premium")