from abc import abstractmethod

from kivy.app import App
from kivy.app import StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass

class InventoryView(Screen):
    items = []
    display_name = StringProperty("")

    def add_item(self, item):
        self.items.append(item)
        self.load_items()

    def create_new_item(self):
        AddItemView(self).open()

    @abstractmethod
    def get_required_item_fields(self):
        raise NotImplemented

    def load_items(self):
        item_access_list = self.ids.item_access_list
        item_access_list.clear_widgets()
        for item in self.items:
            item_access_list.add_widget(ItemView(name=item["name"]))

class ItemView(Button):
    name = StringProperty("") 

class FieldInputView(BoxLayout):
    field_name = StringProperty("")

class AddItemView(Popup):
    def __init__(self, inventory, **kwargs):
        super(AddItemView, self).__init__(**kwargs)
        self.inventory = inventory
        self.entries = { field_name: FieldInputView(field_name=field_name) for field_name in inventory.get_required_item_fields() }
        for entry in self.entries.values():
            self.ids.input_fields.add_widget(entry)

    def add_to_inventory(self):
        item = { field_name: self.entries[field_name].ids.text_input.text for field_name in self.entries.keys() }
        self.inventory.add_item(item)
        self.dismiss()

class EquipmentScreen(InventoryView):
    def get_required_item_fields(self):
        return [ "name" ]

class DrugsAndSolventsScreen(InventoryView):
    pass

class SafetyEquipmentScreen(InventoryView):
    pass

class LabMaterialsScreen(InventoryView):
    pass

class Geclab(ScreenManager):
    pass

class GeclabApp(App):
    def build(self):
        return Geclab()

GeclabApp().run()

