import math
import time
import serial

# -- 7 Types of predefined commands in SCIPver2.0 --
#  Sensor Information Command (3 types)
VERSION_INFO = 'VV'
SENSOR_SPECS = 'PP'
SENSOR_STATE = 'II'

#  Measurement Enable/Disable Command
LASER_ON = 'BM'
LASER_OFF = 'QT'

#  RS232C Bit Rate Setting Command
BIT_RATE = 'SS'

#  Distance Acquisition Command (2 types)
DIST_ACQU_3CHAR = 'MD'
DIST_ACQU_2CHAR = 'MS'
DIST_CMD_2 = 'GD' #DIST_CMD_2 = 'GS'

#  Motor Speed Setting Command
MOTOR_SPEED = 'CR'

#  Time Stamp Adjusting/Acquisition Command
TIME_STAMP = 'TM'

#  RESET COMMAND
RESET = 'RS'

LINE_FEED = '\n'

SET_SCIP2    = 'SCIP2.0'

def changeVersion(serial_device, version_command=SET_SCIP2):
    serial_device.write(version_command + LINE_FEED)
    while 1:
        if serial_device.inWaiting() > 0:
            break
    response = serial_device.readall()
    status = response[9:11]
    return status

def getDataAcquisition(serial_device, starting_step=0, ending_step=768, cluster_count=1, scan_interval=1, number_of_scans=1):
    # Must be between 0 and 768
    starting_step = int(max(0, min(starting_step, 768)))
    ending_step = int(max(0, min(ending_step, 768)))

    # Must be greater
    if ending_step < starting_step: return

    starting_step = getFixedLength(str(starting_step), 4, '0', '')
    ending_step = getFixedLength(str(ending_step), 4, '0', '')

    # cluster_count is the number of adjacent steps that can be merged into single data.
    # When cluster_count is more than 1, step having minimum measurement
    # value (excluding error) in the cluster will be the output data.
    # Example: If Cluster Count is 3 and measurement values of 3 steps in this cluster are
    # 3059, 3055 and 3062, the received data from the sensor will be 3055.
    cluster_count = getFixedLength(str(int(cluster_count)), 2, '0', '')

    # Skipping the number of scans when obtaining multiple scan data can be set in Scan
    # Interval and required number of scan data in Number of Scan. If Number of Scan is set to
    # 00 the data will be supplied indefinitely unless canceled using [QT-Command] or [RS-Command]
    scan_interval = getFixedLength(str(int(scan_interval)), 1, '0', '')
    number_of_scans = getFixedLength(str(int(scan_interval)), 2, '0', '')

    # M D StartingStep EndStep ClusterCount ScanInterval NumberOfScans StringCharacters LF
    command = DIST_ACQU_2CHAR + starting_step + ending_step + cluster_count + scan_interval + number_of_scans + LINE_FEED
    serial_device.write(command)

    while 1:
        if serial_device.inWaiting() > 0:
            break

    response = serial_device.readall()
    status = response[37:39]
    time_stamp = decodeTimeStamp(response[41:45])
    
    #print "status: {0}, time_stamp: {1}".format(status, time_stamp)

    data = response[47:-6].split('\n'); measurments = []
    for d in data:
        if getAuthenticateData(d):
            measurments += decode2CharacterCoding(d)
        else:
            measurments += [None]*32
    #print measurments

    data_length = len(measurments)
    
    return {'data':measurments,'data_length':data_length,'time_stamp':time_stamp,'status':status}
    

def decodeTimeStamp(time_stamp):
    time = ''
    for char in time_stamp:
        time += getFixedLength(bin(ord(char) - 48)[2:], 6, '0', '')
    return int(time, 2)
    
def getAuthenticateData(data):
    auth_sum = data[-1]
    data_sum = 0
    for char in data[:-1]:
        data_sum += ord(char)

    data_sum = int(bin(data_sum)[2:][-6:], 2) + 48
    data_sum = chr(data_sum)

    #print 'data_sum: {0}, auth_sum: {1}'.format(data_sum, auth_sum)

    return data_sum == auth_sum

def decode2CharacterCoding(string):
    data = []
    for index in range(0, len(string)-2, 2):
        first_part = getFixedLength(bin(ord(string[index]) - 48)[2:], 6, '0', '')
        second_part = getFixedLength(bin(ord(string[index+1]) - 48)[2:], 6, '0', '')
        data.append(int(first_part + second_part, 2))
    return data

def getFixedLength(string, length=0, prefix='0', suffix=''):
    while len(string) < length:
        string = prefix + string + suffix

    return string[0:length]

def getAsBytes(string):
    byte_string = ''
    for char in string:
        byte_string += hex(ord(char))[2:]
    return byte_string

def findBaudRate(port='/dev/ttyACM0', timeout=0.5, test_command='SCIP2.0\n'):
    print test_command
    baudrates=(9600, 19200, 38400, 57600, 74880, 115200, 230400, 250000)
    for baudrate in baudrates:
        print "Checking {0} .....".format(baudrate),
        sd = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        sd.write(test_command)

        time.sleep(2)

        if sd.inWaiting() > 0:
            print "\nbaudrate: {0}, data: {1}".format(baudrate, sd.readall())
        else:
            print "None",
        
        sd.close()
        print "Done"

if __name__ == '__main__':
    uart_port = '/dev/ttyACM0'
    uart_speed = 115200

    laser_serial = serial.Serial(port=uart_port, baudrate=uart_speed, timeout=0.5)
    print "status =", changeVersion(laser_serial)
    print getDataAcquisition(laser_serial)
    laser_serial.close()
