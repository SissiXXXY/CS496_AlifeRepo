import dm_control.mujoco
import mujoco.viewer
import time

m = dm_control.mujoco.MjModel.from_xml_path("example.xml")
d = dm_control.mujoco.MjData(m)
mujoco.viewer.launch_passive(m, d)

mujoco.viewer.cam.azimuth = 180  # Azimuthal angle (in degrees)
mujoco.viewer.cam.elevation = -20  # Elevation angle (in degrees)
mujoco.viewer.cam.distance = 3.0  # Distance from the camera to the target
mujoco.viewer.cam.lookat[0] = 0.0  # X-coordinate of the target position
mujoco.viewer.cam.lookat[1] = 0.0  # Y-coordinate of the target position
mujoco.viewer.cam.lookat[2] = 0.75  # Z-coordinate of the target position


for i in range(1000):
    dm_control.mujoco.step(m, d)
    mujoco.viewer.sync()
    time.sleep(0.01)
mujoco.viewer.close()
