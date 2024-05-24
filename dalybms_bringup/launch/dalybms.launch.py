from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import os


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "serial_port",
            default_value="/dev/ttyUSB0",
            description="RS485 device, e.g. /dev/ttyUSB0",
        )
    )

    # Initialize Arguments
    serial_port = LaunchConfiguration("serial_port")

    
    dalybms_hardware_node = Node(
        package="dalybms_hardware",
        executable="dalybms_hardware",
        name="battery",
        parameters=[{"daly_serial_port": serial_port}],
    )

    return LaunchDescription(declared_arguments + [dalybms_hardware_node])
