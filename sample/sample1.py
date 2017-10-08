import sys
sys.path.append('/home/pi/RPi-Farm-Mon/lib')
import sht31
import tsl2561
import boto3

NAMESPACE = 'RPi-Farm-Mon'
DEVICE_ID = 'raspberrypi'

# SHT31
SHT31_ADDRESS = 0x45
SHT31_CHANNEL = 1

# TSL2561
TSL2561_ADDRESS = 0x39
TSL2561_CHANNEL = 1

def main():
    sensor_data = {
        'temperature': None,
        'humidity': None,
        'luminosity': None
    }

    ### SHT31: Temperature and Humidity Sensor ###
    sht31_instance = sht31.SHT31(SHT31_ADDRESS, SHT31_CHANNEL)
    sht31_result = sht31_instance.read()
    sensor_data['temperature'] = round(sht31_result[0],2)
    sensor_data['humidity'] = round(sht31_result[1],2)

    ### TSL2561: Luminosity Sensor ###
    tsl2561_instance = tsl2561.TSL2561(TSL2561_ADDRESS, TSL2561_CHANNEL)
    tsl2561_result = tsl2561_instance.read()
    sensor_data['luminosity'] = round(tsl2561_result[0],1) 

    client = boto3.client('cloudwatch')
    for i in sensor_data.keys():
        metric_data = None
        metric_data = [
            {
                'MetricName': DEVICE_ID + '-' + i,
                'Value': sensor_data[i],
                'Unit': 'Count',
                'Dimensions': [
                    {
                        'Name': 'Device',
                        'Value': DEVICE_ID
                    }
                ]
            }
        ]
        client.put_metric_data( Namespace = NAMESPACE, MetricData = metric_data )

if __name__ == '__main__':
    main()

