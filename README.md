# FlexObject

The FlexObject redefines your Python programming experience with its versatile base class, offering an array of dynamic attribute management capabilities, seamless runtime attribute manipulation, effortless JSON serialization, and streamlined JSON file/string handling. This library serves as a cornerstone for simplified data interaction, catering to a wide spectrum of scenarios.

> FlexObject is compatible only with Python 3.*.


## 🚀 Features

1. **Dynamic Attribute Management**: Enjoy the freedom to effortlessly manage object attributes on-the-fly, enhancing adaptability to evolving requirements.

2. **Runtime Attribute Addition/Removal**: Streamline your workflow by dynamically adding or removing attributes during execution, minimizing disruptions.

3. **JSON Serialization**: Seamlessly transform object attributes into the JSON format, facilitating convenient storage, sharing, or communication with external systems.

4. **JSON File/String Reading**: Effortlessly load object attributes from JSON files or strings, expediting data retrieval and utilization.



## 📋 Usage
After incorporating FlexObject into your project, the usage will follow the steps outlined below.


```Python
from flexobject import FlexObject

# Create a FlexObject instance
flex_obj = FlexObject()

# Set attributes dynamically
flex_obj.set_attrs(name='David Santana', age=21)

# Serialize attributes to JSON string
json_str = flex_obj.to_json()

# Deserialize attributes from JSON string
flex_obj.from_json(json_str)

# Store attributes in a JSON file
flex_obj.write_json_file('data.json')

# Load attributes from a JSON file
flex_obj.read_json_file('data.json')
```



## 📜 License

This project operates under the MIT License, providing you with the flexibility to integrate, modify, and distribute the library as needed.