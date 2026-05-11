# Code Snapshot

本目录用于保存结项阶段与报告主线直接相关的 ROS2 防护代码快照。

## 目录说明

- `ros2_overlay/`
  - 按原始包路径抽取的关键代码文件。
  - 这些文件来源于本地 `colcon_ws/src/mycobot_ros2/...` 工作区中的实际修改版本。

## 为什么不直接提交整个 `colcon_ws`

完整工作区中包含：

- 上游 `mycobot_ros2` 仓库的嵌套 `.git`
- `build/`、`install/`、`log/` 等构建产物
- 大量与本次结项主线无关的模型、资源与依赖文件

为了让仓库更轻、更清晰，这里仅保留本项目真正涉及的关键代码文件，便于审阅、比对和复现实验思路。

## 当前重点文件

- `mycobot_280/launch/test.launch.py`
- `mycobot_280/mycobot_280/joint_state_security.py`
- `mycobot_280/mycobot_280/trusted_joint_state_filter.py`
- `mycobot_280/mycobot_280/slider_control.py`
- `mycobot_280_moveit2_control/mycobot_280_moveit2_control/joint_state_security.py`
- `mycobot_280_moveit2_control/mycobot_280_moveit2_control/sync_plan.py`
- `mycobot_280_moveit2_control/mycobot_280_moveit2_control/sync_plan_arduino.py`

