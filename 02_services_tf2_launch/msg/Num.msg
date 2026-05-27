# EU_02 Custom Message Definition: Num.msg
# Location: my_pubsub_package_interfaces/msg/Num.msg
#
# Theory:
#   ROS2 IDL (Interface Definition Language) uses .msg files
#   to define custom message types. Each field is declared as:
#     <type> <field_name>
#   Supported primitive types: bool, int8, int16, int32, int64,
#     uint8, uint16, uint32, uint64, float32, float64, string, etc.
#
#   After building, the message is accessible in C++ as:
#     #include "my_pubsub_package_interfaces/msg/num.hpp"
#   and in Python as:
#     from my_pubsub_package_interfaces.msg import Num

# A custom message carrying a single 64-bit number
int64 num
