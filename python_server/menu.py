import os

menu = {
  "menu": [
    {
      "label": "Configuration",
      "click": None,
      "submenu": [
        {
          "label": "test",
          "click": lambda: print("test")
        }
      ]
    },
    {
      "label": "Manage targets",
      "submenu": []
    },
    {
      "label": "Quit",
      "click": lambda: os._exit(0)
    }
  ]
}

serializedFunctions = []

def serializeFunctions(menuContainer):
    for menuItem in menuContainer:
          if "click" in menuItem and callable(menuItem["click"]):
              serializedFunctions.append(menuItem["click"])
              menuItem["click"] = len(serializedFunctions)
          if "submenu" in menuItem:
              serializeFunctions(menuItem["submenu"])

serializeFunctions(menu["menu"])


