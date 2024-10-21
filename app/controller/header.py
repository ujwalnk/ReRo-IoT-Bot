from ..main import push_2_server
from .controller import Motor


# r_motor = Motor(7)
# l_motor = Motor(6)

max_speed = 300

def dump(value:str):
    """
    Print the value to the dashboard console, should be used in place of python default print. 
    Can be used for debugging purposes, does not have the default attributes of the python print function

    @param:
        value: str - Value to be printed to the console

    """
    print("Printing some value: ", value)
    push_2_server(value, "print")


def set_right_speed(speed: int):
    """
    Function to set the speed of the motors
    
    @param:
        speed: int - Speed of the right motor 

    @return:
        bool - Speed set success or failure

    speed  should be a number between -100 and 100,
    speed < 0 : moving backwards
    speed = 0 : stop
    speed > 0 : moving forward

    """

    if not (-100 <= speed <= 100):
        return False
    
    if speed == 0:
        r_motor.halt_motor()
    
    return r_motor.set_speed(max_speed * speed / 100)

    
    # TODO: Code to set the motor speed goes here
    return True
    
def set_left_speed(speed: int):
    """
    Function to set the speed of the left motor
    
    @param:
        speed: int - Speed of the left motor 

    @return:
        bool - Speed set success or failure

    speed should be a number between -100 and 100,
    speed < 0 : moving backwards
    speed = 0 : stop
    speed > 0 : moving forward

    """

    if not -100 <= speed <= 100:
        return False
    
    if speed == 0:
        l_motor.halt_motor()
    
    return l_motor.set_speed(max_speed * speed / 100)
    


def get_speed():
    """
    Function to get the speed of the motors
    
    @return: [right_speed, left_speed]
        right_speed: int - Speed of the right motor 
        left_speed: int - Speed of the left motor

    right_speed & left_speed will be a number between -100 and 100,
    speed < 0 : moving backwards
    speed = 0 : stop
    speed > 0 : moving forward

    """

    # TODO: Code to reading the current motor speed
    return [r_motor.get_speed(), l_motor.get_speed()]

def get_color_grid():
    """
    Function to get the color values of the sensor array
    
    @return:
        color: [bool, bool, bool, bool, bool] - Ground color white or black

        white will be represented by a value of True, 
        and black will be represented by the value False

    """

    return [random.choice([True, False]) for _ in range(5)]
