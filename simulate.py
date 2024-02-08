import dm_control.mujoco
import mujoco_viewer
import time
import mujoco

m = dm_control.mujoco.MjModel.from_xml_path("example.xml")
d = dm_control.mujoco.MjData(m)
viewer = mujoco_viewer.MujocoViewer(m, d)

viewer.cam.azimuth = 180  # Azimuthal angle (in degrees)
viewer.cam.elevation = -20  # Elevation angle (in degrees)
viewer.cam.distance = 3.0  # Distance from the camera to the target
viewer.cam.lookat[0] = 0.0  # X-coordinate of the target position
viewer.cam.lookat[1] = 0.0  # Y-coordinate of the target position
viewer.cam.lookat[2] = 0.75  # Z-coordinate of the target position


for i in range(1000):
    if viewer.is_alive:
        mujoco.mj_step(m, d)
        viewer.render()
    else:
        break
viewer.close()
