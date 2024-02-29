import pandas as pd

class Data:
    def __init__(self, name, data, description=None):
        """
        Initialisiert eine Datenklasse.
        
        :param name: Der Name der Daten.
        :param data: Die Daten selbst.
        :param description: Eine optionale Beschreibung der Daten.
        """
        self.name = name
        self.data = data
        self.description = description

class DataManager:
    def __init__(self, data_classes):
        self.data = {}
        self.auto_add(data_classes)

    def auto_add(self, data_classes):
        for data_class in data_classes:
            instance = data_class()
            self.add(instance.name, instance, instance.description)


    def add(self, name, value, description=None):
        """
        Fügt dem DataManager ein neues Datenobjekt hinzu.
        :param name: Der Name des Datenobjekts.
        :param value: Der Wert des Datenobjekts.
        :param description: Die optionale Beschreibung des Datenobjekts.
        """
        self.data[name] = {'value': value, 'description': description}

    def get(self, name):
        """
        Ruft ein gespeichertes Datenobjekt aus dem DataManager ab.
        :param name: Der Name des abzurufenden Datenobjekts.
        :return: Das abgerufene Datenobjekt.
        """
        return self.data.get(name)

    def update(self, name, new_value):
        """
        Aktualisiert ein gespeichertes Datenobjekt im DataManager.
        :param name: Der Name des zu aktualisierenden Datenobjekts.
        :param new_value: Der neue Wert für das Datenobjekt.
        """
        if name in self.data:
            self.data[name]['value'] = new_value
            print(f"Datenobjekt '{name}' erfolgreich aktualisiert.")
        else:
            print(f"Datenobjekt '{name}' nicht gefunden. Kann nicht aktualisiert werden.")

    def list(self):
        """
        Listet alle gespeicherten Datenobjekte im DataManager auf.
        """
        print("Gespeicherte Datenobjekte:")
        for name, data_info in self.data.items():
            value_type = type(data_info['value'])
            description = data_info['description']
            print(f"{name}: {value_type} - {description}")


# Beispielklassen für Daten
"""
class SapData(Data):
    def __init__(self):
        super().__init__(
            name="SAP-Daten",
            data="asd",
            description="Daten aus dem SAP-System"
        )

class DrcData(Data):
    def __init__(self):
        super().__init__(
            name="DRC-Daten",
            data=None,
            description="Daten aus dem DRC-System"
        )

# Beispielverwendung des DataManager

def main():
    data_manager = DataManager([SapData, DrcData])
    data_manager.list()

if __name__ == "__main__":
    main()
"""