from abc import abstractmethod

from pydantic import ValidationError
from kivy.app import App
from kivy.app import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from common.items import Item, EquipmentItem

NAME_VIEW = {
    "name": "Nombre",
    "serial": "Código serial",
    "first_operational_date": "Primer uso",
    "equipment": "Equipamiento",
    "drugs_and_solvents": "Drogas y Solventes",
    "safety_equipment": "Equipos de Seguridad e Higene",
    "lab_materials": "Materiales de Laboratorio"
}

class HomeScreen(Screen):
    name = StringProperty("home")

    def screen_display_name(self, name):
        return NAME_VIEW[name]

class InventoryView(Screen):
    display_name = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = []
        self.display_name = NAME_VIEW[self.name]

    @abstractmethod
    def get_item_model(self):
        return Item

    def add_item(self, item):
        item = self.get_item_model().model_validate(item)
        self.items.append(item)
        self.load_items()
        item_view = ItemView(item)
        item_view.set_previous_screen(self)
        self.manager.add_widget(item_view)

    def create_new_item(self):
        AddItemView(self).open()

    def get_required_item_fields(self):
        return self.get_item_model().model_fields.keys()

    def load_items(self):
        item_access_list = self.ids.item_access_list
        item_access_list.clear_widgets()
        for item in self.items:
            item_access_list.add_widget(ItemEntryView(name=item.name, inventory=self))

class ItemView(Screen):
    def __init__(self, item, **kwargs):
        super().__init__(name=item.name, **kwargs)
        for k, v in item.model_dump().items():
            self.ids.item_data.add_widget(FieldView(text=f"{NAME_VIEW[k]}: {v}"))

    def set_previous_screen(self, previous_screen):
        self.previous_screen = previous_screen

class FieldView(Label):
    pass

class ItemEntryView(Button):
    name = StringProperty("") 
    inventory = ObjectProperty()

class FieldInputView(BoxLayout):
    field_name = StringProperty("")
    popup = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_name = NAME_VIEW[self.field_name]

    def highlight_field(self):
        self.ids.field_input_name.color = (1, 0.1, 0, 1)

    def reset_highlight(self):
        self.ids.field_input_name.color = (1, 1, 1, 1)

    def add_to_inventory(self):
        self.popup.add_to_inventory()

class AddItemView(Popup):
    def __init__(self, inventory, **kwargs):
        super().__init__(**kwargs)
        self.inventory = inventory
        self.entries = { field_name: FieldInputView(field_name=field_name, popup=self) for field_name in inventory.get_required_item_fields() }
        for entry in self.entries.values():
            self.ids.input_fields.add_widget(entry)

    def add_to_inventory(self):
        item = { field_name: self.entries[field_name].ids.text_input.text for field_name in self.entries.keys() }
        for field_name in self.entries.keys():
            self.entries[field_name].reset_highlight()
        try:
            self.inventory.add_item(item)
            self.dismiss()
        except ValidationError as e:
            for bad_field in e.errors():
                self.entries[bad_field["loc"][0]].highlight_field()


class EquipmentScreen(InventoryView):
    name = StringProperty("equipment")

    def get_item_model(self):
        return EquipmentItem

class DrugsAndSolventsScreen(InventoryView):
    name = StringProperty("drugs_and_solvents")

class SafetyEquipmentScreen(InventoryView):
    name = StringProperty("safety_equipment")

class LabMaterialsScreen(InventoryView):
    name = StringProperty("lab_materials")

class Geclab(ScreenManager):
    pass

class GeclabApp(App):
    def build(self):
        return Geclab()

GeclabApp().run()

