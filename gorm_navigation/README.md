# GORM Navigation Package

This package provides autonomous navigation capabilities for the GORM rover, including reinforcement learning-based navigation using Triton Inference Server.

## Overview

The `gorm_navigation` package contains:

- **RL Navigation Node**: Uses trained RL models via Triton Inference Server for autonomous navigation
- **Goal Publisher Node**: For testing and setting navigation goals
- **Launch Files**: To start the navigation system
- **Utilities**: Math and ROS conversion utilities

## Architecture

This package follows the GORM project's architectural principles:
- **Purpose**: Provides autonomous navigation capabilities using RL models
- **Language**: Python (suitable for high-level navigation logic)
- **Dependencies**: Subscribes to depth images, robot pose, and goal positions
- **Outputs**: Publishes velocity commands to `/cmd_vel`

## Dependencies

### ROS 2 Packages
- `rclpy`
- `geometry_msgs`
- `sensor_msgs` 
- `nav_msgs`
- `std_msgs`

### Python Packages
- `numpy`
- `scipy`
- `tritonclient` (optional, for RL inference)

### System Dependencies
```bash
# Install Python dependencies
pip install numpy scipy tritonclient[http]

# Install ROS 2 dependencies (if not already installed)
sudo apt install ros-${ROS_DISTRO}-geometry-msgs ros-${ROS_DISTRO}-sensor-msgs ros-${ROS_DISTRO}-nav-msgs
```

## Usage

### 1. Basic RL Navigation

Launch the RL navigation node:

```bash
ros2 launch gorm_navigation rl_navigation.launch.py
```

### 2. Full Autonomous Navigation

Launch cameras and RL navigation together:

```bash
ros2 launch gorm_navigation autonomous_navigation.launch.py
```

### 3. Testing with Goal Publisher

Test the navigation with a simple goal:

```bash
# In one terminal - start navigation
ros2 launch gorm_navigation rl_navigation.launch.py

# In another terminal - publish a test goal
ros2 run gorm_navigation goal_publisher_node --ros-args -p goal_x:=5.0 -p goal_y:=2.0
```

### 4. Manual Goal Setting

You can also publish goals manually:

```bash
ros2 topic pub /goal_pose geometry_msgs/PoseStamped "
header:
  frame_id: 'map'
pose:
  position:
    x: 5.0
    y: 2.0
    z: 0.0
  orientation:
    w: 1.0"
```

## Configuration

### Parameters

Key parameters can be configured in `config/rl_navigation_params.yaml`:

- `triton_server_url`: URL of Triton Inference Server (default: "localhost:8000")
- `model_name`: Name of the RL model (default: "BC_depth_new")
- `inference_rate`: Inference frequency in Hz (default: 5.0)
- `depth_image_height/width`: Target size for depth images (default: 90x160)
- `max_depth_value`: Maximum depth value in meters (default: 4.0)

### Launch Arguments

```bash
# Disable Triton inference (for testing)
ros2 launch gorm_navigation rl_navigation.launch.py enable_triton:=false

# Custom Triton server URL
ros2 launch gorm_navigation rl_navigation.launch.py triton_server_url:=192.168.1.100:8000

# Custom model name
ros2 launch gorm_navigation rl_navigation.launch.py model_name:=my_rl_model
```

## Topics

### Subscribed Topics

- `/zed_front/zed_node/depth/depth_registered` (sensor_msgs/Image): Depth images from ZED camera
- `/goal_pose` (geometry_msgs/PoseStamped): Navigation goal position
- `/amcl_pose` (geometry_msgs/PoseWithCovarianceStamped): Robot pose from localization
- `/odom` (nav_msgs/Odometry): Fallback robot pose from odometry

### Published Topics

- `/cmd_vel` (geometry_msgs/Twist): Velocity commands for the robot

## Triton Inference Server Setup

To use the RL navigation, you need a Triton Inference Server running with your trained model:

1. **Install Triton Server**: Follow [NVIDIA Triton documentation](https://github.com/triton-inference-server/server)

2. **Prepare Model Repository**: Place your trained RL model in Triton format

3. **Start Triton Server**:
   ```bash
   tritonserver --model-repository=/path/to/your/models
   ```

4. **Verify Connection**:
   ```bash
   curl -v localhost:8000/v2/health/ready
   ```

## Troubleshooting

### Common Issues

1. **"Triton server is not live"**
   - Check if Triton server is running: `curl localhost:8000/v2/health/ready`
   - Verify the server URL in parameters

2. **"Depth data not available"**
   - Check ZED camera is running: `ros2 topic list | grep depth`
   - Verify topic names match in launch file

3. **"Pose data not available"**
   - Ensure localization or odometry is running
   - Check topic remappings in launch file

4. **Robot not moving**
   - Verify `/cmd_vel` topic is being published: `ros2 topic echo /cmd_vel`
   - Check if base control node is subscribed to `/cmd_vel`

### Debug Mode

Run with debug logging:

```bash
ros2 launch gorm_navigation rl_navigation.launch.py --ros-args --log-level DEBUG
```

### Testing Without Triton

For testing the integration without Triton:

```bash
ros2 launch gorm_navigation rl_navigation.launch.py enable_triton:=false
```

This will publish zero velocity commands, useful for testing topic connections.

## Integration with GORM System

This package integrates with other GORM packages:

- **gorm_sensors**: Provides depth images from ZED cameras
- **gorm_base_control**: Receives velocity commands and controls the rover
- **gorm_localization**: Provides robot pose estimates
- **gorm_bringup**: Can include this navigation in system-wide launches

## Future Enhancements

- Integration with Nav2 stack for hybrid navigation
- Dynamic obstacle avoidance
- Multi-goal navigation sequences
- Integration with rover arm control
- Real-time model updates
