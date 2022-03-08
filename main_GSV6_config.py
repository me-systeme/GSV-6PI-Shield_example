import serial
import GSV_convert
import GSV_commands
from time import sleep


def getDataRate():
    serialConnection.write(GSV_commands.ReadDataRate())
    AnswFrame = serialConnection.read(8)
    DataRate = GSV_convert.bytesTofloat(AnswFrame[3:7])
    return DataRate


def setDataRate(DataRate):
    serialConnection.write(GSV_commands.WriteDataRate(DataRate))
    AnswFrame = serialConnection.read(4)
    print("AnswFrame: ", AnswFrame.hex())


def getUserScale(Channel):
    serialConnection.write(GSV_commands.ReadUserScale(Channel))
    AnswFrame = serialConnection.read(8)
    UserScale = GSV_convert.bytesTofloat(AnswFrame[3:7])
    return UserScale


def setUserScale(Channel, UserScale):
    serialConnection.write(GSV_commands.WriteUserScale(Channel, UserScale))
    AnswFrame = serialConnection.read(4)
    print("AnswFrame: ", AnswFrame.hex())

def getInputType(Channel):
    serialConnection.write(GSV_commands.ReadInputType(Channel))
    AnswFrame = serialConnection.read(8)
    InputType = GSV_convert.bytesTouint32(AnswFrame[3:7])
    return InputType

def setInputType(Channel, InputType):
    serialConnection.write(GSV_commands.WriteInputType(Channel, InputType*100))
    AnswFrame = serialConnection.read(4)

    print("AnswFrame: ", AnswFrame.hex())

def SetZero(Channel):
    serialConnection.write(GSV_commands.SetZero(Channel))
    AnswFrame = serialConnection.read(4)
    print("AnswFrame: ", AnswFrame.hex())


def getMeasValues():
    serialConnection.write(GSV_commands.GetValue())
    MeasFrame = serialConnection.read(28)
    MeasValues = MeasFrameToMeasValues(MeasFrame)
    return MeasValues


def MeasFrameToMeasValues(MeasFrame):
    MeasValues = []
    for i in range(6):
        MeasValues.append(GSV_convert.bytesTofloat(MeasFrame[i * 4 + 3:i * 4 + 7]))
    return MeasValues


if __name__ == '__main__':
    serialConnection = serial.Serial("COM11", 230400, timeout=1)
    serialConnection.isOpen()

    serialConnection.write(GSV_commands.StopTransmission())
    sleep(0.1)
    serialConnection.reset_input_buffer()

    """
    print("MeasValues: ", getMeasValues())
    sleep(0.1)
    SetZero(Channel=1)  # SetZero channel 1
    sleep(0.1)
    print("MeasValues: ", getMeasValues())
    sleep(0.1)
    SetZero(Channel=0)  # SetZero all channels
    sleep(0.1)
    print("MeasValues: ", getMeasValues())

    setUserScale(Channel=2, UserScale=2.0)
    print("UserScale - channel 2: ", getUserScale(Channel=2))
    setUserScale(Channel=2, UserScale=1.0)
    print("UserScale - channel 2: ", getUserScale(Channel=2))

    print("DataRate: ", getDataRate())
    setDataRate(100)
    print("DataRate: ", getDataRate())
    """

    print("getInputType(2): ", getInputType(Channel=2))
    # mögliche Werte für InputType: 1, 2, 4, 8 [mV/V]
    print("setInputType(2): ", setInputType(Channel=2, InputType=2))
    # anschliessend muss UserScale angepasst werden
    #    wenn vorher UserScale = 1 und InputType = 1 -> wenn InputType = 2, dann UserScale = 2
    setUserScale(Channel=2, UserScale=2.0)

    serialConnection.write(GSV_commands.Reset())
    serialConnection.write(GSV_commands.StopTransmission())
    sleep(0.1)
    serialConnection.reset_input_buffer()


    print("getInputType(2): ", getInputType(Channel=2))


    serialConnection.close()