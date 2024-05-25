# DalyBMS ROS 2 Integration

This project provides tools to integrate a Daly Battery Management System (BMS) with ROS 2.

## Project Structure

- **dalybms_bringup**: Launch files to start ROS 2 nodes.
- **dalybms_hardware**: Hardware interface to communicate with Daly BMS, adapted from [RobotnikAutomation's code](https://github.com/RobotnikAutomation/daly_bms/blob/main/src/daly_bms/daly_bms_ros.py) which uses the [python-daly-bms library](https://github.com/dreadnought/python-daly-bms).
- **dalybms_interface**: ROS 2 interfaces for BMS communication.

## Prerequisites

- ROS 2 (Foxy or later)
- Python 3.6+
- Build tools (CMake)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ioio2995/dalybms_ros2.git
   cd dalybms_ros2
   ```

2. Create a ROS 2 workspace and navigate into it:
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   ```

3. Clone the repository into the workspace:
   ```bash
   git clone https://github.com/ioio2995/dalybms_ros2.git
   cd ..
   ```

4. Install dependencies:
   ```bash
   sudo apt update
   rosdep update
   rosdep install --from-paths src --ignore-src -r -y
   ```

5. Install Python dependencies:
   ```bash
   pip install -r src/dalybms_ros2/requirements.txt
   ```

6. Build the workspace:
   ```bash
   colcon build
   ```

7. Source the setup script:
   ```bash
   source install/setup.bash
   ```

## Usage

To launch the system:
```bash
ros2 launch dalybms_bringup bringup.launch.py
```

## License and Attribution

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Contributions are welcome. Please submit pull requests and open issues for suggestions or bugs.