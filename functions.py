import math
import random
import xml.etree.ElementTree as ET

import numpy as np
import dm_control.mujoco
import mujoco_viewer
import time
import mujoco
import copy

############################################
# 1. GenerateCreature
# 2. fitness_function
# 3. view
############################################


############################################
# GenerateCreature
# Input: original_xml, new_xml
# Output: new_xml
# Description: This function takes in an original xml file
#              and creates a new xml file with random values for the body and legs
# Randomization: Randomizes the shape and size of the main body, the shape and size of the legs
############################################
def GenerateCreature(original_xml, new_xml):
    tree = ET.parse(original_xml)
    root = tree.getroot()

    mainbody = root.find(".//body[@name='main_body']")
    bodydistance = 0
    leghalflength_1 = 0
    leghalflength_2 = 0
    leghalflength_3 = 0
    leghalflength_4 = 0

    legshape = random.choice(["box", "cylinder"])
    # segmentnum = random.randint(0, 6)

    # randomize main body shape
    shape = random.choice(["box", "cylinder", "sphere"])

    if mainbody is not None:
        for geom in mainbody.findall("geom"):
            geom.set("rgba", "1 0 0 1")
            geom.set("type", shape)
            if shape == "box":
                x_half = round(random.uniform(0.1, 0.3), 2)
                y_half = round(random.uniform(0.2, 0.4), 2)
                z_half = round(random.uniform(0.1, 0.3), 2)
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
                bodydistance = x_half
            elif shape == "cylinder":
                radius = round(random.uniform(0.1, 0.3), 2)
                length_half = round(random.uniform(0.1, 0.3), 2)
                geom.set("size", "{0} {1}".format(radius, length_half))
                bodydistance = radius
            else:
                radius = round(random.uniform(0.1, 0.3), 2)
                geom.set("size", "{0}".format(radius))
                bodydistance = radius
    leg1 = root.find(".//body[@name='leg1']")
    leg2 = root.find(".//body[@name='leg2']")
    leg3 = root.find(".//body[@name='leg3']")
    leg4 = root.find(".//body[@name='leg4']")

    # randomize leg shape and size
    # adjust the position of the legs based on the body size
    # adjust the position of the shank based on the leg size
    # adjust the position of the hinge based on the leg size
    if leg1 is not None:
        for geom in leg1.findall("geom"):
            geom.set("type", legshape)
            leghalflength_1 = 0
            if legshape == "box":
                x_half = round(random.uniform(0.01, 0.09), 2)
                y_half = round(random.uniform(0.01, 0.09), 2)
                z_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_1 = z_half
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))

            elif legshape == "cylinder":
                radius = round(random.uniform(0.01, 0.05), 2)
                length_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_1 = length_half
                geom.set("size", "{0} {1}".format(radius, length_half))
        leg1.set(
            "pos", "{0} {1} {2}".format(-(bodydistance + leghalflength_1), -0.1, 0.1)
        )
        shank1 = leg1.find(".//body[@name='shank1']")
        for geom in shank1.findall("geom"):
            geom.set("type", legshape)
            if legshape == "box":
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                geom.set("size", "{0} {1}".format(radius, length_half))

            shank1.set(
                "pos", "{0} {1} {2}".format(0, 0, -(leghalflength_1 + leghalflength_1))
            )
        hinge1_1 = leg1.find(".//joint[@name='leg1-1']")
        hinge1_2 = leg1.find(".//joint[@name='leg1-2']")
        hinge1_1.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_1))
        hinge1_2.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_1))

    if leg2 is not None:
        for geom in leg2.findall("geom"):
            geom.set("type", legshape)
            leghalflength_1 = 0
            if legshape == "box":
                x_half = round(random.uniform(0.01, 0.09), 2)
                y_half = round(random.uniform(0.01, 0.09), 2)
                z_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_2 = z_half
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                radius = round(random.uniform(0.01, 0.05), 2)
                length_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_2 = length_half
                geom.set("size", "{0} {1}".format(radius, length_half))
        leg2.set(
            "pos", "{0} {1} {2}".format(-(bodydistance + leghalflength_2), 0.1, 0.1)
        )
        shank2 = leg2.find(".//body[@name='shank2']")
        for geom in shank2.findall("geom"):
            geom.set("type", legshape)
            if legshape == "box":
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                geom.set("size", "{0} {1}".format(radius, length_half))
            shank2.set(
                "pos", "{0} {1} {2}".format(0, 0, -(leghalflength_2 + leghalflength_2))
            )
        hinge2_1 = leg2.find(".//joint[@name='leg2-1']")
        hinge2_2 = leg2.find(".//joint[@name='leg2-2']")
        hinge2_1.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_2))
        hinge2_2.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_2))

    if leg3 is not None:
        for geom in leg3.findall("geom"):
            geom.set("type", legshape)
            leghalflength_1 = 0
            if legshape == "box":
                x_half = round(random.uniform(0.01, 0.09), 2)
                y_half = round(random.uniform(0.01, 0.09), 2)
                z_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_3 = z_half
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                radius = round(random.uniform(0.01, 0.05), 2)
                length_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_3 = length_half
                geom.set("size", "{0} {1}".format(radius, length_half))
        leg3.set(
            "pos", "{0} {1} {2}".format((bodydistance + leghalflength_3), -0.1, 0.1)
        )
        shank3 = leg3.find(".//body[@name='shank3']")
        for geom in shank3.findall("geom"):
            geom.set("type", legshape)
            if legshape == "box":
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                geom.set("size", "{0} {1}".format(radius, length_half))
            shank3.set(
                "pos", "{0} {1} {2}".format(0, 0, -(leghalflength_3 + leghalflength_3))
            )
        hinge3_1 = leg3.find(".//joint[@name='leg3-1']")
        hinge3_2 = leg3.find(".//joint[@name='leg3-2']")
        hinge3_1.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_3))
        hinge3_2.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_3))

    if leg4 is not None:
        for geom in leg4.findall("geom"):
            geom.set("type", legshape)
            leghalflength_1 = 0
            if legshape == "box":
                x_half = round(random.uniform(0.01, 0.09), 2)
                y_half = round(random.uniform(0.01, 0.09), 2)
                z_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_4 = z_half
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                radius = round(random.uniform(0.01, 0.05), 2)
                length_half = round(random.uniform(0.1, 0.3), 2)
                leghalflength_4 = length_half
                geom.set("size", "{0} {1}".format(radius, length_half))
        leg4.set(
            "pos", "{0} {1} {2}".format((bodydistance + leghalflength_4), 0.1, 0.1)
        )
        shank4 = leg4.find(".//body[@name='shank4']")
        for geom in shank4.findall("geom"):
            geom.set("type", legshape)
            if legshape == "box":
                geom.set("size", "{0} {1} {2}".format(x_half, y_half, z_half))
            elif legshape == "cylinder":
                geom.set("size", "{0} {1}".format(radius, length_half))
            shank4.set(
                "pos", "{0} {1} {2}".format(0, 0, -(leghalflength_4 + leghalflength_4))
            )
        hinge4_1 = leg4.find(".//joint[@name='leg4-1']")
        hinge4_2 = leg4.find(".//joint[@name='leg4-2']")
        hinge4_1.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_4))
        hinge4_2.set("pos", "{0} {1} {2}".format(0, 0, leghalflength_4))
    tree.write(new_xml)


############################################
# FitnessFunction
# Input: startpos, endpos, total_distance
# Output: efficency(fitness score)
# Description: Calculates the fitness score of the creature based on the efficency of the movement
############################################
def FitnessFunction(startpos, endpos, total_distance):
    if total_distance == 0:
        return 0
    absdist = math.sqrt((endpos[0] - startpos[0]) ** 2 + (endpos[1] - startpos[1]) ** 2)
    efficency = absdist / total_distance
    return efficency


############################################
# View
# Input: xml_file, creature_num
# Output: txt file with fitness score
# Description: run the simulation of the creature and calculate the fitness score
############################################
def View(file, creature_num, round):
    m = dm_control.mujoco.MjModel.from_xml_path(file)
    d = dm_control.mujoco.MjData(m)
    viewer = mujoco_viewer.MujocoViewer(m, d)

    motors = m.nu
    step = 3
    d.ctrl[:motors] = step
    duration_per_direction = 500
    total_distance = 0
    startpos = copy.copy(d.qpos[:2])
    initialpos = copy.copy(d.qpos[:2])

    for i in range(500):
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
            total_distance += np.sum(np.abs(copy.copy(d.qpos[:2]) - initialpos))
            initialpos = copy.copy(d.qpos[:2])
            viewer.render()
        else:
            break
    endpos = copy.copy(d.qpos[:2])
    print(total_distance)
    with open(f"fitness{round}.txt", "a") as f:
        f.write(
            f"Creature:{creature_num},fitness:{FitnessFunction(startpos, endpos, total_distance)}\n"
        )
