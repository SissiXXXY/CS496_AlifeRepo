import math
import random
import xml.etree.ElementTree as ET
import functions

import numpy as np


def SelectBest(recordfile, round):
    max_score = -1
    best_creature = None
    with open(recordfile, "r") as file:
        for line in file:
            if line == "\n":
                continue
            parts = line.strip().split(",")
            creature_num = int(parts[0].split(":")[1].strip())
            fitness_score = float(parts[1].split(":")[1].strip())

            if fitness_score > max_score:
                max_score = fitness_score
                best_creature = creature_num
    print(
        f"Creature with the highest fitness score: {best_creature}, Fitness Score: {max_score}"
    )
    with open(recordfile, "a") as file:
        file.write(
            f"Round {round}:\n"
            f"Creature with the highest fitness score: {best_creature}, Fitness Score: {max_score}\n"
        )
    return best_creature


def MakeCopy(creature_num, copyname):
    original_file_name = f"new_creature{creature_num}.xml"
    with open(original_file_name, "r") as original_file, open(
        copyname, "w"
    ) as new_file:
        content = original_file.read()
        new_file.write(content)


def MutateWeightMass(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    mainbody = root.find(".//body[@name='main_body']")
    geom = mainbody.find("geom")
    geom.set("rgba", "1 0 0 0.5")
    mainbody_type = mainbody.find("geom").attrib["type"]
    mainbody_size = mainbody.find("geom").attrib["size"]
    size = mainbody_size.split(" ")
    # randomize the mass of the weightmass
    mass = random.uniform(3, 20)
    # print(mainbody_size)
    # print(f"0{size[0]}, 1:{size[1]}, 2:{size[2]}")
    weight_mass = ET.SubElement(mainbody, "body", attrib={"name": "weightmass"})
    if mainbody_type == "sphere":
        pos = size[0]
        weight_mass.set("pos", f"0 0 -{pos}")
        ET.SubElement(
            weight_mass,
            "geom",
            attrib={
                "type": "sphere",
                "size": "0.05",
                "rgba": "0 1 0 1",
                "mass": f"{mass}",
            },
        )
    elif mainbody_type == "box":
        pos = size[2]
        posx = 0.5 * float(size[0])
        # print(f"pos: {pos}")
        weight_mass.set("pos", f"{posx} 0 -{pos}")
        ET.SubElement(
            weight_mass,
            "geom",
            attrib={"type": "sphere", "size": "0.05", "rgba": "0 1 0 1"},
        )
    elif mainbody_type == "cylinder":
        pos = size[0]
        weight_mass.set("pos", f"0 0 -{pos}")
        ET.SubElement(
            weight_mass,
            "geom",
            attrib={"type": "sphere", "size": "0.05", "rgba": "0 1 0 1"},
        )
    # new_body.add('geom', type='sphere', size='0.25', rgba='1 0 0 1')

    tree.write(file_name)


def MutateExtendShank(file_name):
    # randomize the coefficient
    # randomly extend the length of the shank on one side
    tree = ET.parse(file_name)
    root = tree.getroot()
    leg1 = root.find(".//body[@name='leg1']")
    leg1_size = leg1.find("geom").attrib["size"].split(" ")
    leg1_length = 0
    leg2 = root.find(".//body[@name='leg2']")
    leg2_size = leg2.find("geom").attrib["size"].split(" ")
    leg2_length = 0
    if leg1.find("geom").attrib["type"] == "box":
        leg1_length = float(leg1_size[2])
    elif leg1.find("geom").attrib["type"] == "cylinder":
        leg1_length = float(leg1_size[1])

    if leg2.find("geom").attrib["type"] == "box":
        leg2_length = float(leg2_size[2])
    elif leg2.find("geom").attrib["type"] == "cylinder":
        leg2_length = float(leg2_size[1])

    shank1 = leg1.find(".//body[@name='shank1']")
    hinge1 = shank1.find(".//joint[@name='leg1-2']")

    shank2 = leg2.find(".//body[@name='shank2']")
    hinge2 = shank2.find(".//joint[@name='leg2-2']")
    coefficient = random.uniform(1.5, 2)

    # print(f"coefficient: {coefficient}")
    # print(f"type coefficient: {type(coefficient)}")
    shank1_size = shank1.find("geom").attrib["size"].split(" ")
    shank2_size = shank2.find("geom").attrib["size"].split(" ")
    if shank1.find("geom").attrib["type"] == "box":
        shank1.find("geom").set(
            "size",
            f"{shank1_size[0]} {shank1_size[1]} {coefficient*float(shank1_size[2])}",
        )
        shank1.set("pos", f"0 0 -{leg1_length+coefficient*float(shank1_size[2])}")
        hinge1.set("pos", f"0 0 {coefficient*float(shank1_size[2])}")
    elif shank1.find("geom").attrib["type"] == "cylinder":
        # print(f"shank1_size: {shank1_size}")
        # print(f"shank2_size: {shank2_size}")
        # print(f"shank1_size[1]{shank1_size[1]}")
        # print(f"type shank1_size[1]: {type(shank1_size[1])}")
        shank1.find("geom").set(
            "size", f"{shank1_size[0]} {coefficient*float(shank1_size[1])}"
        )
        shank1.set("pos", f"0 0 -{leg1_length+coefficient*float(shank1_size[1])}")
        hinge1.set("pos", f"0 0 {coefficient*float(shank1_size[1])}")
    if shank2.find("geom").attrib["type"] == "box":
        shank2.find("geom").set(
            "size",
            f"{shank2_size[0]} {shank2_size[1]} {coefficient*float(shank2_size[2])}",
        )
        shank2.set("pos", f"0 0 -{leg2_length+coefficient*float(shank2_size[2])}")
        hinge2.set("pos", f"0 0 {coefficient*float(shank2_size[2])}")
    elif shank2.find("geom").attrib["type"] == "cylinder":
        shank2.find("geom").set(
            "size", f"{shank2_size[0]} {coefficient*float(shank2_size[1])}"
        )
        shank2.set("pos", f"0 0 -{leg2_length+coefficient*float(shank2_size[1])}")
        hinge2.set("pos", f"0 0 {coefficient*float(shank2_size[1])}")

    tree.write(file_name)


def MutateMass(filename):
    random_mass = random.uniform(3, 50)
    tree = ET.parse(filename)
    root = tree.getroot()
    mainbody = root.find(".//body[@name='main_body']")
    geom = mainbody.find("geom")
    geom.set("mass", f"{random_mass}")
    tree.write(filename)


def MutateTail(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    random_angle_lowerbound = random.uniform(-45, 0)
    random_angle_upperbound = random.uniform(0, 45)
    mainbody = root.find(".//body[@name='main_body']")
    mainbody_type = mainbody.find("geom").attrib["type"]
    mainbody_size = mainbody.find("geom").attrib["size"]
    mbsize = mainbody_size.split(" ")
    tail = ET.SubElement(mainbody, "body", attrib={"name": "tail"})
    ET.SubElement(
        tail,
        "geom",
        attrib={"type": "box", "size": "0.02 0.15 0.02", "rgba": "0.5 0 0 1"},
    )
    ET.SubElement(
        tail,
        "joint",
        attrib={
            "name": "tail1",
            "type": "hinge",
            "pos": "0 -0.05 0",
            "axis": "1 0 0",
            "range": f"{random_angle_lowerbound} {random_angle_upperbound}",
        },
    )
    if mainbody_type == "box":
        tail.set("pos", f"0 {float(mbsize[1])+0.15} 0")
    elif mainbody_type == "cylinder":
        tail.set("pos", f"0 {float(mbsize[1])+0.15} 0")
    elif mainbody_type == "sphere":
        tail.set("pos", f"0 {float(mbsize[0])+0.15} 0")

    actuators = root.find(".//actuator")
    ET.SubElement(actuators, "motor", attrib={"joint": "tail1", "name": "tail1j"})

    tree.write(filename)
