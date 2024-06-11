from functions.tools import get_sensors_data_func,capture_and_save_image_func
tools_jsons = [
        {
            "type": "function",
            "function": {
                "name": "get_sensors_data_tool",
                "description": "retireving the sensors data",
                "parameters": {},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "capture_and_save_image_tool",
                "description": "capturing an image via camera module",
                "parameters": {},
            },
        },
    ]

tools_funcs = {
    'get_sensors_data_tool':get_sensors_data_func,
    'capture_and_save_image_tool':capture_and_save_image_func,
}

tools={
    'jsons':tools_jsons,
    'funcs':tools_funcs,
}
'''
      {
            "type": "function",
            "function": {
                "name": "get_sensors_data_tool",
                "description": "retireving the sensors data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
        
'''
