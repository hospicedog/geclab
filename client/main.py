from abc import abstractmethod

from kivy.app import App
from kivy.app import StringProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass

class InventoryScreen(Screen):
    display_name = StringProperty("")

    @abstractmethod
    def get_items(self):
        raise NotImplemented

    @abstractmethod
    def add_item(self):
        raise NotImplemented

    def load_items(self):
        item_access_list = self.ids.item_access_list
        item_access_list.clear_widgets()
        for item in self.get_items():
            item_access_list.add_widget(item)

class DisplayableItem(Button):
    name = StringProperty("") 
    def __init__(self, **kwargs):
        super(DisplayableItem, self).__init__(**kwargs)

    @classmethod
    def from_response_item(cls, response_item):
        return cls(name=response_item.name)

class FieldEntry(BoxLayout):
    field_name = StringProperty("")
    def __init__(self, **kwargs):
        super(FieldEntry, self).__init__(**kwargs)

class AddItemPopup(Popup):
    def __init__(self, inventory, **kwargs):
        super(AddItemPopup, self).__init__(**kwargs)
        self.inventory = inventory
        for field_name in inventory.get_required_item_fields():
            self.ids.input_fields.add_widget(FieldEntry(field_name=field_name))

    def add_to_inventory(self):
        for field_name in self.inventory.get_required_item_fields():
            print(self.ids[field_name].text)

class EquipmentScreen(InventoryScreen):
    class Item():
        def __init__(self, name):
            self.name = name

    def get_required_item_fields(self):
        return [ "Equipment name" ]

    def add_item_popup(self):
        AddItemPopup(self).open()

    def get_items(self):
        return []

class DrugsAndSolventsScreen(InventoryScreen):
    display_name = "Drogas y Solventes"
    def get_items(self):
        return "drogas y solventes"

class SafetyEquipmentScreen(InventoryScreen):
    display_name = "Equipos de Seguridad e Higene"
    def get_items(self):
        return "seh"

class LabMaterialsScreen(InventoryScreen):
    display_name = "Materiales de Laboratorio"
    def get_items(self):
        return "materiales de labo"

class Geclab(ScreenManager):
    pass

class GeclabApp(App):
    def build(self):
        return Geclab()

GeclabApp().run()

