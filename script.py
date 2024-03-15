import dm_control.mujoco
import mujoco_viewer
import time
import mujoco

m = dm_control.mujoco.MjModel.from_xml_path("round5_cr8.xml")
d = dm_control.mujoco.MjData(m)
viewer = mujoco_viewer.MujocoViewer(m, d)

motors = m.nu
step = 3
d.ctrl[:motors] = step
duration_per_direction = 500

for i in range(10000):
    current_step = i // duration_per_direction
    if viewer.is_alive:
        if i % 2 == 0:
            d.ctrl[:3] = step * 1000
            d.ctrl[4:] = -step * 1000
            mujoco.mj_step(m, d)
        else:
            d.ctrl[:3] = -step * 1000
            d.ctrl[4:] = step * 1000
            mujoco.mj_step(m, d)
        viewer.render()
    else:
        break
