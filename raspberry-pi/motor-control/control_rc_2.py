import asyncio
#from gpiozero.pins import lgpio
import lgpio
import time
import sys
from multiprocessing import Pipe
import time
from adafruit_servokit import ServoKit

IN1 = 18
IN2 = 27
FREQ_HZ = 20

SERVO = 23
SERVO_HZ = 250

# Constants
nbPCAServo = 16

# Objects
pca = ServoKit(channels=16)

async def connect_stdin():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader

async def poll_gamepad(queue):
    reader = await connect_stdin()
    while True:
        res = await reader.readuntil()
        res_as_str = res.decode("utf-8")
        #print("res_as_str ",res_as_str)
        line = res_as_str.split(' ')
        length = len(line)
        if length == 6 and line[0] == 'servo':
            # servo 42 in1 34 in2 23
            await queue.put((float(line[1]), float(line[3]), float(line[5])))
        else:
            print(f"not it {res}")


def convert_integer(n, a, b, c, d):
    # verfication if n is in range [a, b]
    if n < a or n > b:
        raise ValueError("n is out of range")
    # scaling
    scale = (d - c) / (b - a)
    # Convert n in m in range [c, d]
    m = int((n - a) * scale + c)
    return m



async def display_values(servo, in1, in2):
    print("Converted values :")
    servo = convert_integer(servo,500,1000,120,180)
    in1 = convert_integer(in1,0,75,90,0)
    in2 = convert_integer(in2,0,75,90,180)
    print("SERVO =", servo)
    print("IN1 =", in1)
    print("IN2 =", in2)
    vspeed=90
    if in1!=90:
        speed=in1
    elif in2!=90:
        speed=in2
    motor(0,speed)
    motor(1,servo)

async def print_stick(queue):
    motor = lgpio.gpiochip_open(0)
    while True:
        (servo, in1, in2) = await queue.get()
        #lgpio.tx_servo(motor, SERVO, round(servo), SERVO_HZ)
        #lgpio.tx_pwm(motor, IN1, FREQ_HZ, 100 if in1 > 0 else 0)
        #lgpio.tx_pwm(motor, IN2, FREQ_HZ, 100 if in2 > 0 else 0)
        await display_values(servo, in1, in2)
        #await asyncio.sleep(0.1)

# Function init
def init():
    MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
    MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
    for i in range(16):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i], MAX_IMP[i])


def motor(i, j):
    print("Send angle {} to Servo {}".format(j, i))
    pca.servo[i].angle = j
    time.sleep(0.01)


if __name__ == "__main__":
    print('starting')
    init()
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(100)
    loop.create_task(poll_gamepad(queue))
    loop.create_task(print_stick(queue))
    loop.run_forever()