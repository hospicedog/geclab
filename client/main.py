from abc import abstractmethod
from datetime import date

from pydantic import BaseModel, ValidationError, Field
from kivy.app import App
from kivy.app import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


TRANSLATIONS = {
    "name": "Nombre",
    "serial": "Código serial",
    "first_operational_date": "Primer uso",
}

class HomeScreen(Screen):
    pass

class Item(BaseModel):
    name: str = Field(min_length=1)

class EquipmentItem(Item):
    serial: int
    first_operational_date: date

class InventoryView(Screen):
    items = []
    display_name = StringProperty("")

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
        super(ItemView, self).__init__(name=item.name, **kwargs)
        for k, v in item.model_dump().items():
            self.ids.item_data.add_widget(FieldView(text=f"{TRANSLATIONS[k]}: {v}"))

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
        super(FieldInputView, self).__init__(**kwargs)
        self.field_name = TRANSLATIONS[self.field_name]

    def add_to_inventory(self):
        self.popup.add_to_inventory()

class AddItemView(Popup):
    def __init__(self, inventory, **kwargs):
        super(AddItemView, self).__init__(**kwargs)
        self.inventory = inventory
        self.entries = { field_name: FieldInputView(field_name=field_name, popup=self) for field_name in inventory.get_required_item_fields() }
        for entry in self.entries.values():
            self.ids.input_fields.add_widget(entry)

    def add_to_inventory(self):
        item = { field_name: self.entries[field_name].ids.text_input.text for field_name in self.entries.keys() }
        try:
            self.inventory.add_item(item)
            self.dismiss()
        except ValidationError as e:
            for bad_field in e.errors():
                print(bad_field["loc"][0])


class EquipmentScreen(InventoryView):
    def get_item_model(self):
        return EquipmentItem

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

