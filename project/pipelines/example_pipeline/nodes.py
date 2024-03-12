# Beispiel für Nodes, die auf den DataManager zugreifen

# Funktion für Node 1
def node_function_1(data, multiplier, data_manager) -> int:
    # Zugriff auf Daten aus dem DataManager
    some_data = data_manager.get_jetline_data("Name")
    
    # Verarbeitung der Daten und Rückgabe des Ergebnisses
    result = data * multiplier * some_data
    return result

# Funktion für Node 2
def node_function_2(data, offset) -> int:
    # Zugriff auf Daten aus dem DataManager
   
    result = data + offset
    return result
