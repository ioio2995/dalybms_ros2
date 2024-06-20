#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dalybms_interface.msg import BatteryStatus
from dalybms import DalyBMS as DalyBMSDriver

class DalyBMS(Node):
    def __init__(self):
        super().__init__("dalybms_hardware")
        self._driver: DalyBMSDriver = DalyBMSDriver()
        self._battery_status = BatteryStatus()
        self._last_battery_state = "Unknown"
        self._time_init_charging = self.get_clock().now()
        self._last_discharge_value = 3.0
        self.bms_init()

    def ros_read_params(self):
        self.declare_parameter("daly_serial_port", "/dev/ttyUSB0")
        self._port = self.get_parameter("daly_serial_port").get_parameter_value().string_value
        if not self._port:
            self.get_logger().warn(
                "No serial port provided, using default: /dev/ttyUSB0"
            )
            self._port = "/dev/ttyUSB0"

    def ros_init(self):
        self._battery_status_pub = self.create_publisher(BatteryStatus, "~/data", 10)
        timer_period = 1.0  # seconds
        self._reading_timer = self.create_timer(timer_period, self.read)
        self._publishing_timer = self.create_timer(timer_period, self.publish)

    def bms_init(self):
        self.ros_read_params()
        try:
            self._driver.connect(self._port)
        except Exception as e:
            self.get_logger().error(f"Failed to connect to BMS: {e}")
            return
        self.ros_init()

    def read(self):
        try:
            soc_data = self._driver.get_soc()
            mosfet_data = self._driver.get_mosfet_status()
            cells_data = self._driver.get_cell_voltages()
        except Exception as e:
            self.get_logger().warn(f"Skipping current read cycle: {e}")
            return

        if not soc_data or not mosfet_data or not cells_data:
            self.get_logger().warn(
                "Skipping current read cycle: Driver failed to return data"
            )
            return

        self._battery_status.level = soc_data["soc_percent"]
        self._battery_status.voltage = soc_data["total_voltage"]
        self._battery_status.current = soc_data["current"]

        if mosfet_data["mode"] == "discharging":
            self._battery_status.is_charging = False
            self._battery_status.time_charging = 0
            self._last_discharge_value = self._battery_status.current
        elif mosfet_data["mode"] in ["charging", "stationary"]:
            if self._last_battery_state in ["Unknown", "discharging"]:
                self._time_init_charging = self.get_clock().now()

            self._battery_status.is_charging = True
            elapsed_time = (
                self.get_clock().now() - self._time_init_charging
            ).nanoseconds / 1e9 / 60  # convert to minutes
            self._battery_status.time_charging = int(elapsed_time)

        # _last_discharge_value is negative in certain cases
        if self._last_discharge_value != 0:
            remaining_hours = round(
                mosfet_data["capacity_ah"] / abs(self._last_discharge_value), 0
            )
        else:
            remaining_hours = 0

        self._battery_status.time_remaining = max(
            0, int(remaining_hours) * 60
        )  # convert hours to minutes
        self._last_battery_state = mosfet_data["mode"]

        self._battery_status.cell_voltages = list(cells_data.values())

    def publish(self):
        self._battery_status_pub.publish(self._battery_status)

def main(args=None):
    rclpy.init(args=args)
    daly_bms = DalyBMS()
    daly_bms.get_logger().info(f"Starting Daly BMS Node {daly_bms.get_name()}")
    rclpy.spin(daly_bms)
    daly_bms.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
