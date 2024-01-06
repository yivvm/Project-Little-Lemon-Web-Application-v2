from django.test import TestCase
from LittleLemonDRF.models import Menu

class  MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="ChocolateIceCream", price=8, inventory=100)
        self.assertEqual(item, "ChocolateIceCream : 8")
    
    def test_get_all():
        items = Menu.objects.all()