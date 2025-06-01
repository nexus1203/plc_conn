# get python version
import sys
import importlib

version = sys.version_info
python_version = 'v' + str(version.major) + str(version.minor)
print("______using python version: {}_______".format(python_version))
module_path = f".__versions.{python_version}.plc_com"
plc_com = importlib.import_module(module_path, package=__package__)
plc_com.StringResources.Language = plc_com.English()

import logging, os
from datetime import datetime
from time import perf_counter as pf


class PLC:
    """
    A class that implements the PLC communication functionality.
    """

    def __init__(self,
                 instance_id: int = 0,
                 ip_address: str = '127.0.0.1',
                 port: int = 80,
                 plc_type: str = "MEL_FX5U",
                 log: bool = False):
        """Initialize the PLC class instance with an IP address and port number and plc type settings.
           instance_id is the identifier of the specific plc instance. (for example, 0 for instance 0 and similarly for instance 1 is 1)
           Total number of instances can vary depending on the network configuration and no two instances with the same identifier.

        Args:
            instance_id (int, required): The identifier of the plc instance. Defaults to 0.
            ip_address (str, required): The IP address of the PLC to be connected. Defaults to '127.0.0.1'.
            port (int, required): port number of the PLC to be connected. Defaults to 80.
            plc_type (str, required): The type of the PLC to be connected. Defaults to "MEL_FX5U".
                                      Several options are available for different PLC types. Currently supported types are
                                      "MEL_FX5U"    --> Mitsubishi FX5U,
                                      "MEL_QSER"    --> Mitsubishi Qseries,
                                      "MEL_FX3U"    --> Mitsubishi FX3U,
                                      "SMN_S300"    --> SIEMENS S300,
                                      "SMN_S1200"   --> SIEMENS S1200,
                                      "SMN_S1500"   --> SIEMENS S1500,
                                      "SMN_S200"    --> SIEMENS S200 smart,
            log (bool,optional): Whether to log the message. Defaults to False.                        
        """

        self.instance_id = instance_id
        self.plc_type = plc_type
        self.ip_address = ip_address
        self.port = port
        self.log = log  # default to False
        self.connected = False  # default to False, connection status of the PLC

        if self.log:
            self.get_logger()
            self.save_log(
                info=
                "Initializing PLC with instance_id {}, plc_type {}, ip_address {} and port {}"
                .format(self.instance_id, self.plc_type, self.ip_address,
                        self.port))

        # print(plc_type)
        assert plc_type in [
            "MEL_FX5U", "MEL_QSER", "MEL_FX3U", "SMN_S300", "SMN_S1200",
            "SMN_S1500", "SMN_S2000"
        ], "Invalid PLC type"

        self.plc = None

        if plc_type in ["MEL_FX5U", "MEL_QSER"]:
            self.plc = plc_com.MelsecMcNet(ipAddress=ip_address, port=port)
            # print(self.plc)

        elif plc_type == "MEL_FX3U":
            self.plc = plc_com.MelsecA1ENet(ipAddress=ip_address, port=port)

        elif plc_type == "SMN_S300":
            self.plc = plc_com.SiemensS7Net(plc_com.SiemensPLCS.S300,
                                            ipAddress=ip_address,
                                            port=port)

        elif plc_type == "SMN_S1200":
            self.plc = plc_com.SiemensS7Net(plc_com.SiemensPLCS.S1200,
                                            ipAddress=ip_address,
                                            port=port)

        elif plc_type == "SMN_S1500":
            self.plc = plc_com.SiemensS7Net(plc_com.SiemensPLCS.S1500,
                                            ipAddress=ip_address,
                                            port=port)

        elif plc_type == "SMN_S200":
            self.plc = plc_com.SiemensS7Net(plc_com.SiemensPLCS.S200Smart,
                                            ipAddress=ip_address,
                                            port=port)

        else:
            self.plc = plc_com.MelsecMcNet(ipAddress=ip_address, port=port)

        if self.plc.ConnectServer().IsSuccess:
            self.connected = True
            self.save_log(info="Connection Successful!")
        else:
            self.connected = False
            self.save_log(info="Connection Failed!")

    def get_logger(self):
        start_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        logger_folder = 'LOGS/{}'.format(self.instance_id)
        # create logger folder if it does not exist
        os.makedirs(logger_folder, exist_ok=True)

        handler = logging.FileHandler(
            os.path.join(logger_folder, start_time + '.log'))
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.INFO,
            handlers=[handler])
        self.logger = logging.getLogger('PLC_id{}'.format(self.instance_id))

    def save_log(self, info: str = ""):
        """Internal method to save log information if logging is enabled

        Args:
            info (str, required): information to log.
        """
        if self.log:
            self.logger.info(info)
        else:
            a = None

    def read_bool(self, register: str = "M100"):
        """function to read boolean value from plc register

        Args:
            register (str, optional): register id of the plc, can be input, output or buffer registers. Defaults to "M100".

        Returns:
            bool: return value of register if read is successful, otherwise None.
        """
        # s = pf()
        result = self.plc.ReadBool(register)
        # print('time:', pf()-s)
        if result.IsSuccess:
            self.save_log(
                info=
                "Read boolean operation : Register : {}, Result : {}, Status : {},"
                .format(register, result.Content, "Sucess"))
            return result.Content
        else:
            self.save_log(
                info=
                "Read boolean operation : Register : {}, Result : {}, Status : {},"
                .format(register, None, "Failure"))
            return None

    def read_int16(self, register: str = "D100"):
        """function to read integer16 from register from the plc register.

        Args:
            register (str, optional): register id of the plc. Defaults to "D100".

        Returns:
            return integer value if the read operation is successful else None.
        """

        result = self.plc.ReadInt16(register)
        if result.IsSuccess:
            self.save_log(
                info=
                "Read INT16 operation : Register : {}, Result : {}, Status : {},"
                .format(register, result.Content, "Sucess"))
            return result.Content
        else:
            self.save_log(
                info=
                "Read INT16 operation : Register : {}, Result : {}, Status : {},"
                .format(register, None, "Failure"))
            return None

    def read_int32(self, register: str = "D100"):
        """function to read integer32 from register from the plc register.

        Args:
            register (str, optional): register id of the plc. Defaults to "D100".

        Returns:
            return integer value if the read operation is successful else None.
        """
        result = self.plc.ReadInt32(register)
        if result.IsSuccess:
            self.save_log(
                info=
                "Read INT32 operation : Register : {}, Result : {}, Status : {},"
                .format(register, result.Content, "Sucess"))
            return result.Content
        else:
            self.save_log(
                info=
                "Read INT32 operation : Register : {}, Result : {}, Status : {},"
                .format(register, None, "Failure"))
            return None

    def write_bool(self, register: str = "M100", value: bool = True) -> str:
        """ function to write boolean and confirm the write operation is successful.

        Args:
            register (str, optional): register id of the plc. Defaults to "M100".
            value (bool, optional): boolean value to write to the register. Defaults to True.

        Returns:
            str: return of the status of the write operation : success, failure or unconfirmed.
        """
        self.plc.WriteBool(register, value)
        check = self.plc.ReadBool(register)
        # print(register, value, check.IsSuccess)

        if check.IsSuccess:
            check_value = check.Content
        else:
            check_value = None

        if check_value is None:
            self.save_log(
                info=
                "Write Bool operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Unconfirmed"))
            return "unconfirmed"
        elif check_value == value:
            self.save_log(
                info=
                "Write Bool operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Sucess"))
            return "success"
        else:
            self.save_log(
                info=
                "Write Bool operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Failure"))
            return "failure"

    def write_int16(self, register: str = "D100", value: int = 0) -> str:
        """Function to write integer16 and confirm the write operation is successful.

        Args:
            register (str, optional): register id of the plc. Defaults to "D100"..
            value (int, optional): integer value to write to the register. Defaults to 0.

        Returns:
            str:  return of the status of the write operation : success, failure or unconfirmed.
        """

        self.plc.WriteInt16(register, value)
        check = self.plc.ReadInt16(register)

        if check.IsSuccess:
            check_value = check.Content
        else:
            check_value = None

        if check_value is None:
            self.save_log(
                info=
                "Write INT16 operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Unconfirmed"))
            return "unconfirmed"
        elif check_value == value:
            self.save_log(
                info=
                "Write INT16 operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Success"))
            return "success"
        else:
            self.save_log(
                info=
                "Write INT16 operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Failure"))
            return "failure"

    def write_int32(self, register: str = "D100", value: int = 0) -> str:
        """Function to write integer32 and confirm the write operation is successful.

        Args:
            register (str, optional): register id of the plc. Defaults to "D100"..
            value (int, optional): integer value to write to the register. Defaults to 0.

        Returns:
            str:  return of the status of the write operation : success, failure or unconfirmed.
        """

        self.plc.WriteInt32(register, value)
        check = self.plc.ReadInt32(register)

        if check.IsSuccess:
            check_value = check.Content
        else:
            check_value = None

        if check_value is None:
            self.save_log(
                info=
                "Write INT32 operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Unconfirmed"))
            return "unconfirmed"
        elif check_value == value:
            self.save_log(
                info=
                "Write INT32 operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Success"))
            return "success"
        else:
            self.save_log(
                info=
                "Write INT32 operation : Register : {}, Value : {}, Status : {}"
                .format(register, value, "Failure"))
            return "failure"
