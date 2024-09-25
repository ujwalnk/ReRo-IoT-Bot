class DataSentinel():
    """
    Class to encapsulate & enable datasharing
    """

    # Encoder data
    __encoder_count__ : int = 0

    # Encoder count flag
    __encoder_counting__ : bool = False

    # Singleton class implementation
    __self__ = None

    SERVER_IP_ADDRESS = "http://192.168.1.2:8082"


    def __init__():
        """ Singleton class initilization """
        if not __self__ :
            __self__ = DataSentinel()
        else:
            return __self__
        
    def get_encoder_count(self):
        """ Getter for __encoder_count__ """
        return self.__encoder_count__
    
    def set_encoder_status(self, flag):
        """Setter for __encoder_counting__ """
        self.__encoder_counting__ = flag

    def get_encoder_status(self):
        """Getter for __encoder_counting__ """
        return self.__encoder_count__

    def reset_encoder_count(self):
        """ Function to reset the encoder count """
        self.__encoder_count__ = 0

    # Comment not added into the function to increase the speed of execution, as this function will be called inside an ISR
    # Function to increment the encoder count
    def increment_encoder_count(self):
        self.__encoder_count__ += 1