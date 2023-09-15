import json
import time
import uuid
import bpy
import random
from mathutils import Vector
import math
import os
import sys
sys.path.append("/content/drive/MyDrive/blender_fire/")
import config
import numpy as np
cfg = config.cfg()


def random_generator(values):
    if values[1]=='list':
        return values[0]
    elif values[1]=='float':
        return random.uniform(values[0][0],values[0][1])
    elif values[1] == 'bool':
        pickup = [True, False]
        return pickup[random.choice(pickup)]
    else:
        return random.randint(values[0][0], values[0][1])
#  Remove The Default Cude Object
# bpy.ops.object.delete(use_global=False)
def delete_object():
    bpy.ops.object.delete(use_global=False, confirm=False)

def choose_random_image(folder_path):
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Filter the list to only include image files (e.g., JPG, PNG, etc.)
    image_list = [file for file in file_list if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    if not image_list:
        print("No image files found in the folder.")
        return None

    # Select a random image path from the list
    random_image_path = os.path.join(folder_path, random.choice(image_list))

    return random_image_path

# Function to add a random number of objects at random coordinates
def add_random_objects(coordinates, min_num_objects, max_num_objects):
    num_objects = random.randint(min_num_objects, max_num_objects)

    for _ in range(num_objects):
        # Create a mesh object
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD')

        # Choose a random coordinate from the array
        coord = random.choice(coordinates)

        # Set the location
        bpy.context.active_object.location = coord


# Define the coordinates and the range of the number of objects


def select_and_activate_random_obj():
    all_objects = []
    for o in bpy.context.scene.objects:
        if "Camera" not in o.name and "Light" not in o.name:
            all_objects.append(o.name)
    return all_objects
    random_index = random.randint(0, len(all_objects) - 1)
    object_name = all_objects[random_index]
    print(object_name)
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object
    '''obj = bpy.data.objects.get(object_name)
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    bpy.context.object.scale[0] = -0.119999
    bpy.context.object.scale[1] = -0.00999933
    bpy.context.object.scale[2] = -0.0199993'''
    return object_name


def add_quick_smoke(object_name):
    obj = bpy.data.objects.get(object_name)
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    #bpy.context.object.scale[0] = -0.119999
    #bpy.context.object.scale[1] = -0.00999933
    #bpy.context.object.scale[2] = -0.0199993
    bpy.ops.object.quick_smoke()
    return obj


# Call the function to add random objects at the given coordinates
def fire_simulation(sph_obj):
    smoke_obj = bpy.data.objects['Smoke Domain']
    sph_obj.modifiers["Fluid"].flow_settings.flow_type =cfg.smoke_obj['flow_settings']['flow_type']
    sph_obj.modifiers["Fluid"].flow_settings.fuel_amount = random_generator(cfg.smoke_obj['flow_settings']['fuel_amount'])
# f_amount
    bpy.context.scene.frame_end = 150
    #
    # select domain to (smoke domian)
    smoke_obj.modifiers["Fluid"].domain_settings.use_adaptive_timesteps = True
    smoke_obj.modifiers["Fluid"].domain_settings.use_adaptive_domain = True
    smoke_obj.modifiers["Fluid"].domain_settings.domain_type =cfg.smoke_dom['settings']['domain_type']

    smoke_obj.modifiers["Fluid"].domain_settings.cfl_condition = 0
    # for loop on  resolution range (6,6+2,128)
    smoke_obj.modifiers["Fluid"].domain_settings.resolution_max = 2*(random_generator(cfg.smoke_dom['settings']['resolution_max']))

    #
    # Time Scale controls the speed of the simulation.
    # Low values result in a “slow motion” simulation, while higher values result in a “faster motion”.
    ## for loop on  time scale range (0,0.10,10)
    smoke_obj.modifiers["Fluid"].domain_settings.time_scale = random_generator(cfg.smoke_dom['settings']['time_scale'])
    #
    smoke_obj.modifiers["Fluid"].domain_settings.use_dissolve_smoke = cfg.use_dissolve_smoke
    ## for loop on disslove
    smoke_obj.modifiers["Fluid"].domain_settings.dissolve_speed = random_generator(cfg.smoke_dom['Gas']['dissolve_speed'])
    #
    smoke_obj.modifiers["Fluid"].domain_settings.use_noise = cfg.use_noise
    ## for loop on noise sacle(0,10)
    bpy.context.object.modifiers["Fluid"].domain_settings.noise_pos_scale = random_generator(cfg.smoke_dom['Gas']['noise_pos_scale'])
    smoke_obj.modifiers["Fluid"].domain_settings.cache_frame_end = 150
    smoke_obj.modifiers["Fluid"].domain_settings.cache_type = 'ALL'
    smoke_obj.modifiers["Fluid"].domain_settings.cache_data_format = 'UNI'
    smoke_obj.modifiers["Fluid"].domain_settings.flame_smoke_color = (226, 88, 34)


def background():
    cam = bpy.context.scene.camera
    random_image_path = choose_random_image(cfg.folder_path)
  # os.path.join("/home/vishal/Downloads/","1.jpg")

    # Locations
    cam.location.x = -0.71
    cam.location.y = -12
    cam.location.z = 5.5

    # Rotations
    cam.rotation_euler[0] = math.radians(64)
    cam.rotation_euler[1] = math.radians(-0)
    cam.rotation_euler[2] = math.radians(-3)
    # Displaying the Background in the camera view
    img = bpy.data.images.load(random_image_path)
    cam.data.show_background_images = True
    bg = cam.data.background_images.new()
    bg.image = img
    bpy.context.scene.render.film_transparent = True
    return img


def background_steup(img):
    ### Compositing

    #bpy.context.area.ui_type = 'CompositorNodeTree'

    # scene = bpy.context.scene
    # nodetree = scene.node_tree
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    for every_node in tree.nodes:
        tree.nodes.remove(every_node)

    RenderLayers_node = tree.nodes.new('CompositorNodeRLayers')
    RenderLayers_node.location = -300, 300

    comp_node = tree.nodes.new('CompositorNodeComposite')
    comp_node.location = 400, 300

    AplhaOver_node = tree.nodes.new(type="CompositorNodeAlphaOver")
    AplhaOver_node.location = 150, 450

    Scale_node = tree.nodes.new(type="CompositorNodeScale")
    bpy.data.scenes["Scene"].node_tree.nodes["Scale"].space = 'RENDER_SIZE'
    Scale_node.location = -150, 500

    Image_node = tree.nodes.new(type="CompositorNodeImage")
    Image_node.image = img
    Image_node.location = -550, 500

    links = tree.links
    link1 = links.new(RenderLayers_node.outputs[0], AplhaOver_node.inputs[2])
    link2 = links.new(AplhaOver_node.outputs[0], comp_node.inputs[0])
    link3 = links.new(Scale_node.outputs[0], AplhaOver_node.inputs[1])
    link4 = links.new(Image_node.outputs[0], Scale_node.inputs[0])

    #bpy.context.area.ui_type = 'TEXT_EDITOR'


def shadder_nodes():
    # all_objects = []
    for o in bpy.context.scene.objects:
        # all_objects.append(o)
        if o == bpy.data.objects['Smoke Domain']:
            object_name = "Smoke Domain"
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object
    obj = bpy.data.objects.get(object_name)
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    bpy.context.scene.render.engine = cfg.render_engine
    bpy.context.scene.cycles.device = cfg.cycles_device
    #bpy.context.scene.cycles.device = 'CPU'
    # shadder node
    '''smoke density loop '''
    bpy.data.materials["Smoke Domain Material"].node_tree.nodes["Principled Volume"].inputs[2].default_value = cfg.smoke_density
    ''' black body instensity'''
    bpy.data.materials["Smoke Domain Material"].node_tree.nodes["Principled Volume"].inputs[8].default_value = 10
    bpy.data.materials["Smoke Domain Material"].node_tree.nodes["Principled Volume"].inputs[7].default_value = (1, 0.458225, 0.0118011, 1)
    bpy.data.materials["Smoke Domain Material"].node_tree.nodes["Principled Volume"].inputs[9].default_value = (1, 0.11027, 0.0355233, 1)

    obj.data.materials.clear()
    obj.data.materials.append(bpy.data.materials["Smoke Domain Material"])


def add_lights(coordinates):
    num_lights = random.randint(cfg.min_light,cfg.max_light)  # Generate a random number of lights between 1 and 10

    for _ in range(num_lights):
        coordinate = random.choice(coordinates)  # Choose a random coordinate from the given list
        l_point = random.randint(0, 1)
        l_type_point = ['POINT', 'SUN']
        # Create a new light object
        bpy.ops.object.light_add(type=l_type_point[l_point], location=coordinate)
        light = bpy.context.object
        if l_type_point == "SUN":
            bpy.context.object.data.energy = cfg.energy

        # Set random color
        light.data.color = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))

        # Set random energy
        light.data.energy = random.uniform(0.1, 5.0)

        # Set random radius
        light.data.shadow_soft_size = random.uniform(0.1, 2.0)

        # Set random falloff
        # light.data.falloff_type = random.choice(['INVERSE_LINEAR', 'INVERSE_SQUARE', 'LINEAR', 'QUADRATIC'])

        # Set random quadratic attenuation
        # if light.data.falloff_type == 'QUADRATIC':
        #   light.data.quadratic_attenuation = random.uniform(0.01, 1.0)


def bake_all():
    bpy.ops.Fluid.bake_all()


# function calls


coordinates = [
    Vector((-4.15131139755249, 3.872501850128174, -0.14218425750732422)),
    Vector((9.180441856384277, 16.088272094726562, -3.8104093074798584)),
    Vector((6.510919094085693, 6.173250675201416, -6.613709926605225)),
    Vector((-2.063464641571045, -3.3883299827575684, 0.9929574131965637)),
    Vector((0.7775346040725708, 2.807274580001831, 0.8491849303245544)),
    Vector((2.0782310962677, 4.93025541305542, 0.18255919218063354)),
    Vector((6.1974968910217285, 9.780349731445312, -3.4481396675109863)),
    Vector((-1.0158607959747314, -0.2960459589958191, 1.6254340410232544)),
    Vector((0.551348090171814, 1.1877775192260742, -0.049069005995988846)),
    Vector((6.848080158233643, 8.955995559692383, -5.311561107635498)),
    Vector((2.0529532432556152, 3.44962739944458, -0.9720098376274109)),
    Vector((7.996969223022461, 13.705641746520996, -3.568819761276245)),
    Vector((5.294489860534668, 5.462098121643066, -5.292511463165283)),
    Vector((5.737847328186035, 7.4876179695129395, -4.463738918304443)),
    Vector((-0.7034692764282227, -2.4500699043273926, -0.6954605579376221)),
    Vector((6.55864143371582, 10.35261058807373, -3.6471805572509766)),
    Vector((-1.543992280960083, -2.2021350860595703, 1.0492192506790161)),
    Vector((0.0, 0.0, 0.0)),
    Vector((0.2209518551826477, -1.0099869966506958, -1.2250020503997803)),
    Vector((1.1642284393310547, 1.0495072603225708, -1.2867430448532104)),
    Vector((1.2713470458984375, 0.09433215856552124, -2.2582364082336426)),
    Vector((0.0, 0.0, 0.0)),
    Vector((0.0, 0.0, 0.0))
]


def set_output_directory(output_dir):
    bpy.context.scene.render.filepath = output_dir


def set_render_settings(output_format, color_mode, compression, resolution_x, resolution_y):
    bpy.context.scene.render.image_settings.file_format = output_format
    bpy.context.scene.render.image_settings.color_mode = color_mode
    bpy.context.scene.render.image_settings.compression = compression
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y


def set_frame_range(start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame


def render_frames(output_dir):
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4().hex)
    folder_name = f"{timestamp}_{unique_id}"
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # bpy.ops.render.render(animation=True)

    # Create a list to store the annotations in COCO format
    annotations = {}

    # Iterate over the animation frames
    for frame in range(cfg.first_frame, bpy.context.scene.frame_end + 1,(bpy.context.scene.frame_end-cfg.first_frame)//cfg.save_count):
        # Set the current frame
        bpy.context.scene.frame_set(frame)
        # Render the image for the current frame
        bpy.context.scene.render.filepath = os.path.join(folder_path, "frame_{:04d}".format(frame))
        bpy.ops.render.render(write_still=True)
        annotations["frame_{:04d}".format(frame)] = find_bounding_box()

    with open(os.path.join(folder_path,'annotation.json'), 'w') as f:
        json.dump(annotations, f)


def find_bounding_box():
    """
    Returns camera space bounding box of the mesh object.

    Gets the camera frame bounding box, which by default is returned without any transformations applied.
    Create a new mesh object based on self.carre_bleu and undo any transformations so that it is in the same space as the
    camera frame. Find the min/max vertex coordinates of the mesh visible in the frame, or None if the mesh is not in view.

    :param scene:
    :param camera_object:
    :param mesh_object:
    :return:
    """
    obj = bpy.data.objects.get("Smoke Domain")

    """ Get the inverse transformation matrix. """
    scene = bpy.data.scenes['Scene']
    camera = bpy.data.objects['Camera']
    matrix = camera.matrix_world.normalized().inverted()
    """ Create a new mesh data block, using the inverse transform matrix to undo any transformations. """
    mesh = obj.to_mesh(preserve_all_data_layers=True)
    mesh.transform(obj.matrix_world)
    mesh.transform(matrix)

    """ Get the world coordinates for the camera frame bounding box, before any transformations. """
    frame = [-v for v in camera.data.view_frame(scene=scene)[:3]]

    lx = []
    ly = []

    for v in mesh.vertices:
        co_local = v.co
        z = -co_local.z

        if z <= 0.0:
            """ Vertex is behind the camera; ignore it. """
            continue
        else:
            """ Perspective division """
            frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    """ Image is not in view if all the mesh verts were ignored """
    if not lx or not ly:
        return None

    min_x = np.clip(min(lx), 0.0, 1.0)
    min_y = np.clip(min(ly), 0.0, 1.0)
    max_x = np.clip(max(lx), 0.0, 1.0)
    max_y = np.clip(max(ly), 0.0, 1.0)

    """ Image is not in view if both bounding points exist on the same side """
    if min_x == max_x or min_y == max_y:
        return None

    """ Figure out the rendered image size """
    render = scene.render
    fac = render.resolution_percentage * 0.01
    dim_x = render.resolution_x * fac
    dim_y = render.resolution_y * fac

    ## Verify there's no coordinates equal to zero
    coord_list = [min_x, min_y, max_x, max_y]
    if min(coord_list) == 0.0:
        indexmin = coord_list.index(min(coord_list))
        coord_list[indexmin] = coord_list[indexmin] + 0.0000001

    return (min_x, min_y), (max_x, max_y)


# Example usage:


delete_object()
min_num_objects = 1
max_num_objects = 3
add_random_objects(coordinates, min_num_objects, max_num_objects)
add_lights(coordinates)
object_name = select_and_activate_random_obj()
obj=add_quick_smoke(object_name)
fire_simulation(obj)
img= background()
background_steup(img)
bake_all()
shadder_nodes()

output_dir = cfg.output_dir
set_output_directory(output_dir)
resolution_x=cfg.resolution_x
resolution_y=cfg.resolution_y
output_format=cfg.output_format
color_mode=cfg.color_mode
compression=cfg.compression
set_render_settings(output_format, color_mode, compression,resolution_x, resolution_y)

start_frame = cfg.start_frame
end_frame = cfg.end_frame
set_frame_range(start_frame, end_frame)

render_frames(output_dir)
