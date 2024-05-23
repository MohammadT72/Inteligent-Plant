from datetime import datetime

def parse_sensors_data(data: dict) -> dict:
    # Get current time and season
    now = datetime.now()
    current_hour = now.hour
    month = now.month

    if 6 <= current_hour < 18:
        time_of_day = 'It is currently daytime.'
    else:
        time_of_day = 'It is currently nighttime.'

    if 3 <= month <= 5:
        season = 'We are in spring.'
    elif 6 <= month <= 8:
        season = 'We are in summer.'
    elif 9 <= month <= 11:
        season = 'We are in autumn.'
    else:
        season = 'We are in winter.'

    # moisture
    if data['moisture'] > 4:
        data['moisture'] = 'The moisture level is ' + str(data['moisture']) + '. It is too low, need more water.'
    elif data['moisture'] > 1.5:
        data['moisture'] = 'The moisture level is ' + str(data['moisture']) + '. It is high, too much water.'
    else:
        data['moisture'] = 'The moisture level is ' + str(data['moisture']) + '. It is good, it is enough for now.'

    # temperature
    if 'plant_type' not in data:
        if 15 <= data['temp'] <= 24:
            data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is suitable for most plants.'
        else:
            data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It may not be suitable for most plants.'
    else:
        if data['plant_type'] == 'tropical':
            if 21 <= data['temp'] <= 32:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is suitable.'
            else:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is not suitable.'
        elif data['plant_type'] == 'subtropical':
            if 18 <= data['temp'] <= 27:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is suitable.'
            else:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is not suitable.'
        elif data['plant_type'] == 'temperate':
            if 15 <= data['temp'] <= 24:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is suitable.'
            else:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is not suitable.'
        elif data['plant_type'] == 'cool-season':
            if 10 <= data['temp'] <= 21:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is suitable.'
            else:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is not suitable.'
        elif data['plant_type'] == 'warm-season':
            if 21 <= data['temp'] <= 35:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is suitable.'
            else:
                data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. It is not suitable.'
        else:
            data['temp'] = 'The temperature is ' + str(data['temp']) + '°C. Unknown plant type specified.'

    # brightness
    if 'plant_type' not in data:
        if 10000 <= data['brightness'] <= 20000:
            data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is suitable for most plants.'
        elif data['brightness'] < 10000:
            data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too dark for most plants.'
        else:
            data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too bright for most plants.'
    else:
        if data['plant_type'] == 'tropical':
            if 15000 <= data['brightness'] <= 30000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is suitable.'
            elif data['brightness'] < 15000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too dark.'
            else:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too bright.'
        elif data['plant_type'] == 'subtropical':
            if 10000 <= data['brightness'] <= 20000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is suitable.'
            elif data['brightness'] < 10000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too dark.'
            else:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too bright.'
        elif data['plant_type'] == 'temperate':
            if 15000 <= data['brightness'] <= 25000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is suitable.'
            elif data['brightness'] < 15000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too dark.'
            else:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too bright.'
        elif data['plant_type'] == 'cool-season':
            if 10000 <= data['brightness'] <= 20000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is suitable.'
            elif data['brightness'] < 10000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too dark.'
            else:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too bright.'
        elif data['plant_type'] == 'warm-season':
            if 20000 <= data['brightness'] <= 30000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is suitable.'
            elif data['brightness'] < 20000:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too dark.'
            else:
                data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. It is too bright.'
        else:
            data['brightness'] = 'The brightness level is ' + str(data['brightness']) + ' lux. Unknown plant type specified.'

    # Add time of day and season information
    data['info'] = time_of_day + ' ' + season

    return data