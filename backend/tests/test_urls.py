from django.test import SimpleTestCase
from django.urls import reverse,resolve
from product.views import add_product,get_products,get_product,update_product,delete_product,CreateCheckoutSessionView
from order.views import get_order,get_single_order,add_order,process_order,delete_order,create_checkout_session

class ProductTestUrls(SimpleTestCase):
    
    def test_get_products(self):
        url = reverse('get-all-products')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,get_products)
    
    def test_get_product(self):
        url = reverse('get-product-pk',kwargs={'pk':1})
        self.assertEquals(resolve(url).func,get_product)
        
    def test_add_product(self):
        url = reverse('add-product')
        self.assertEquals(resolve(url).func,add_product)
    
    def test_update_product(self):
        url = reverse('update-product',kwargs={'pk':1})
        self.assertEquals(resolve(url).func,update_product)
        
    def test_delete_product(self):
        url = reverse('delete-product',kwargs={'pk':1})
        self.assertEquals(resolve(url).func,delete_product)
    
    def test_createcheckoutsessionview(self):
        url = reverse('create-checkout-session-product')
        self.assertEquals(resolve(url).func.view_class,CreateCheckoutSessionView)
    
class OrderTestUrls(SimpleTestCase):
    
    def test_get_orders(self):
        url = reverse('get-all-orders')
        self.assertEquals(resolve(url).func,get_order)
    
    def test_get_single_order(self):
        url = reverse('get-single-order',kwargs={'pk':1})
        self.assertEquals(resolve(url).func,get_single_order)
    
    def test_add_order(self):
        url = reverse('add-new-order')    
        self.assertEquals(resolve(url).func,add_order)
    
    def test_delete_order(self):
        url = reverse('delete-order',kwargs={'pk':1})
        self.assertEquals(resolve(url).func,delete_order)
    
    def test_update_order(self):
        url = reverse('update-order',kwargs = {'pk':1})
        self.assertEquals(resolve(url).func,process_order)
        
    def test_order_create_checkout(self):
        url = reverse('create-checkout-session')
        self.assertEquals(resolve(url).func,create_checkout_session)