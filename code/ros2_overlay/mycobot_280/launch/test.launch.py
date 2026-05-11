import os

from ament_index_python import get_package_share_path
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration


def generate_launch_description():
    res = []

    model_launch_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            get_package_share_path("mycobot_description"),
            "urdf/mycobot_280_m5/mycobot_280_m5.urdf"
        )
    )
    res.append(model_launch_arg)

    rvizconfig_launch_arg = DeclareLaunchArgument(
        name="rvizconfig",
        default_value=os.path.join(
            get_package_share_path("mycobot_280"),
            "config/mycobot.rviz"
        )
    )
    res.append(rvizconfig_launch_arg)

    gui_launch_arg = DeclareLaunchArgument(
        name="gui",
        default_value="true"
    )
    res.append(gui_launch_arg)

    raw_topic_launch_arg = DeclareLaunchArgument(
        name="raw_joint_states_topic",
        default_value="_joint_states_authorized_source"
    )
    res.append(raw_topic_launch_arg)

    trusted_topic_launch_arg = DeclareLaunchArgument(
        name="trusted_joint_states_topic",
        default_value="_joint_states_trusted"
    )
    res.append(trusted_topic_launch_arg)

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        remappings=[('joint_states', LaunchConfiguration('trusted_joint_states_topic'))]
    )
    res.append(robot_state_publisher_node)

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui')),
        remappings=[('joint_states', LaunchConfiguration('raw_joint_states_topic'))]
    )
    res.append(joint_state_publisher_node)

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui')),
        remappings=[('joint_states', LaunchConfiguration('raw_joint_states_topic'))]
    )
    res.append(joint_state_publisher_gui_node)

    trusted_joint_state_filter_node = Node(
        package='mycobot_280',
        executable='trusted_joint_state_filter',
        parameters=[{
            'raw_topic': LaunchConfiguration('raw_joint_states_topic'),
            'trusted_topic': LaunchConfiguration('trusted_joint_states_topic'),
            'max_message_age_seconds': 0.5,
            'enforce_single_publisher': True,
        }]
    )
    res.append(trusted_joint_state_filter_node)

    rviz_node = Node(
        name="rviz2",
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=['-d', LaunchConfiguration("rvizconfig")],
    )
    res.append(rviz_node)

    return LaunchDescription(res)
