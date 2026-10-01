# my_robot — Домашнее задание №2

ROS 2 (Jazzy) пакет с моделью шарнирного манипулятора с тремя степенями свободы: URDF-модель,
визуализация в RViz и узел управления положением робота.

![URDF Tree](docs/urdf_tree.png)

## Где что лежит

| Пункт задания | Файл / папка | Описание |
|---|---|---|
| 1. ROS пакет | `package.xml`, `setup.py`, `setup.cfg`, `resource/` | пакет `my_robot` (ament_python) |
| 2. URDF файл | [`my_robot/urdf/my_robot.urdf`](my_robot/urdf/my_robot.urdf) | 5 звеньев, 3 вращательных шарнира и жёсткое крепление захвата |
| 3–4. Код Python, управление положением | [`my_robot/my_robot/arm_controller.py`](my_robot/my_robot/arm_controller.py) | узел `arm_controller`: перебирает опорные конфигурации и принимает целевую конфигурацию из топика `/target_position` |
| 5. Launch файлы | [`my_robot/launch/display.launch.py`](my_robot/launch/display.launch.py) | RViz + robot_state_publisher + joint_state_publisher_gui (ползунки) |
| | [`my_robot/launch/move.launch.py`](my_robot/launch/move.launch.py) | RViz + robot_state_publisher + arm_controller (автоматическое движение) |
| 6. Видео | [`my_robot/docs/demo.mp4`](my_robot/docs/demo.mp4) | запуск визуализации и движение робота |
| 7. URDF Tree | [`my_robot/docs/urdf_tree.png`](my_robot/docs/urdf_tree.png) | также `urdf_tree.pdf` и исходник `urdf_tree.gv` |
| 8. Отчёт | [`my_robot/docs/report.docx`](my_robot/docs/report.docx) | описание робота, структура, прямая задача кинематики, описание движения |
| — | [`my_robot/rviz/robot.rviz`](my_robot/rviz/robot.rviz) | настройки RViz |
| — | `my_robot/test/` | стандартные тесты ament (flake8, pep257, copyright) |

## Запуск

Пакет нужно положить в `src/` рабочего пространства ROS 2 Jazzy:

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -y
colcon build --packages-select my_robot
source install/setup.bash

# визуализация, обобщённые координаты задаются ползунками
ros2 launch my_robot display.launch.py

# автоматическое движение по опорным конфигурациям
ros2 launch my_robot move.launch.py

# переход в заданную конфигурацию (q1, q2, q3 в радианах), во втором терминале
ros2 topic pub --once /target_position std_msgs/msg/Float64MultiArray "{data: [1.0, 0.5, -0.8]}"
```
