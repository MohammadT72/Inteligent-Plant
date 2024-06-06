import json
from test_logics import parse_sensors_data
def get_sensors_data_func(sen_list=None):
    """retireving the sensors data"""
    data={
        'temp':23,
        'moisture':0.2,
        'brightness':500,
    }
    data = parse_sensors_data(data)
    return json.dumps(data)
    # data=parse_sensors_data(data)
    # if data['temp']==None or data['moisture']==None:
      # raise ToolException('The sensors data are not available.')
    # output_text=''
    # for _,value in data.items():
    #   output_text+=value
    # return output_text