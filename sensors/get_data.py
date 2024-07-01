import time
import serial
import asyncio

class SerialReader:
    def __init__(self, port='/dev/ttyUSB0', baudrate=12500, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.result = None
    def parse_result(self,result):
        data={
                'temp':23,
                'brightness':500,
            }
        if result!=None:
            list_data=result.split(',')
            for item in list_data:
                if 'Moist' in item:
                    data['moisture']=float(item.split(':')[-1])
        return data


    def open_serial(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(3)
            self.ser.reset_input_buffer()
            print('Serial OK')
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")

    def get_data(self):
        if self.ser is None:
            self.open_serial()

        if self.ser is not None:
            try:
                while isinstance(self.result,type(None)):
                    if self.ser.in_waiting > 0:
                        line = self.ser.readline().decode('utf-8', errors='ignore')
                        self.result=self.parse_result(line)
                        break
            except KeyboardInterrupt:
                print("Close Serial communication.")
                self.ser.close()

    def close_serial(self):
        if self.ser is not None:
            self.ser.close()

# Usage example
def main():
    reader = SerialReader()
    reader.open_serial()
    reader.get_data()
    print(reader.result)
    reader.close_serial()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Close Serial communication.")
