from abc import abstractmethod

from kivy.app import App
from kivy.app import StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass

class Item:
    name = ""

    def get_name(self):
        return self.name

    @classmethod
    @abstractmethod
    def required_fields(cls):
        raise NotImplemented

    @classmethod
    @abstractmethod
    def from_input_entries(cls, entries):
        raise NotImplemented

class EquipmentItem(Item):
    def __init__(self, name, serial):
        self.name = name
        self.serial = serial

    @classmethod
    def required_fields(cls):
        return [ "name", "serial" ]

    @classmethod
    def from_input_entries(cls, entries):
        return cls(entries["name"], entries["serial"])

class InventoryView(Screen):
    items = []
    display_name = StringProperty("")

    @abstractmethod
    def add_item(self, item):
        raise NotImplemented

    def create_new_item(self):
        AddItemView(self).open()

    @abstractmethod
    def get_required_item_fields(self):
        raise NotImplemented

    def load_items(self):
        item_access_list = self.ids.item_access_list
        item_access_list.clear_widgets()
        for item in self.items:
            item_access_list.add_widget(ItemView(name=item.get_name()))

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
        return EquipmentItem.required_fields()

    def add_item(self, item):
        self.items.append(EquipmentItem.from_input_entries(item))
        self.load_items()

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

