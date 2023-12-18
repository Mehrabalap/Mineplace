from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json



def input(key):
    if key=='l':
        for e in scene.entities:
            if isinstance(e, Voxel):
                destroy(e)
        loaded_data = load_world('world_data.json')
        if loaded_data:
            world_data = loaded_data
            # Create voxels based on the loaded data
            for pos, tex in zip(world_data['position'], world_data['texture']):
                create_voxel(pos, tex)

def create_voxel(position, texture):
    voxel_data = {
        'position': position,
        'texture': texture
    }
    # Create the voxel in the scene
    voxel = Voxel(position=position, texture=texture)

def load_world(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                loaded_world_data = json.load(file)
            print("World loaded successfully.")
            return loaded_world_data
        except Exception as e:
            print(f"Failed to load world: {str(e)}")
    else:
        print(f"File '{filename}' does not exist.")
        return None

loaded_data = None

# Define your world data as a list
world_data  =  {'position': [], 'texture': []}

def save_world(world_data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(world_data, file, indent=4)
        print("World saved successfully.")
    except Exception as e:
        print(f"Failed to save world: {str(e)}")

def load_world(filename):
    try:
        with open(filename, 'r') as file:
            loaded_world_data = json.load(file)
        print("World loaded successfully.")
        return loaded_world_data
    except Exception as e:
        print(f"Failed to load world: {str(e)}")
        return None

app = Ursina()

# Loading textures
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
leaf_texture = load_texture('assets/leaf_block.png')

# Audio
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)

# Initialize block pick
block_pick = 1

# Create an Entity to display the selected block's image
selected_block_image = Entity(parent=camera.ui, model='quad', texture=grass_texture, scale=(0.1, 0.1), position=(-0.4, 0.4))

# Create a Text entity to display the selected block's name
selected_block_name = Text(parent=camera.ui, text='Grass', position=(-0.3, 0.35), scale=0.05, origin=(0, 0))

# Disable fps counter and exit button
window.fps_counter.enabled = False
window.exit_button.visible = False

# Change the type of blocks and position of arm on mouse click
def update():
    global block_pick, loaded_data, world_data

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if loaded_data:
        # Update your world data with loaded_data
        world_data = loaded_data

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if block_pick == 1:
        selected_block_image.texture = grass_texture
        selected_block_name.text = 'Grass'
    elif block_pick == 2:
        selected_block_image.texture = stone_texture
        selected_block_name.text = 'Stone'
    elif block_pick == 3:
        selected_block_image.texture = brick_texture
        selected_block_name.text = 'Brick'
    elif block_pick == 4:
        selected_block_image.texture = dirt_texture
        selected_block_name.text = 'Dirt'
    elif block_pick == 5:
        selected_block_image.texture = leaf_texture
        selected_block_name.text = 'Leaf'

    # Example: Save the world when the player presses the 's' key
    if held_keys['k']:
        for e in scene.entities:
            if isinstance(e, Voxel):
                world_data['position'].append( (e.x , e.y, e.z) )
                world_data['texture'].append(str(e.texture))
        save_world(world_data, 'world_data.json')
    # Example: Load the world when the player presses the 'l' key


# Creating the voxel
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5)

    # Function for creating new voxels and removal of voxels
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                if block_pick == 2: voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                if block_pick == 3: voxel = Voxel(position=self.position + mouse.normal, texture=brick_texture)
                if block_pick == 4: voxel = Voxel(position=self.position + mouse.normal, texture=dirt_texture)
                if block_pick == 5: voxel = Voxel(position=self.position + mouse.normal, texture=leaf_texture)
            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)

# Creating the sky
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True)

# Creating the arm
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    # Margin by which arm moves
    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Generating initial voxels
for z in range(30):
    for y in range(3):
        for x in range(30):
            # Adjust the positions to create a 3x3x3 block grid
            voxel = Voxel(position=(x - 1, y - 1, z - 1))

# Creating the first-person controller
player = FirstPersonController()
sky = Sky()
hand = Hand()

# Run the application
app.run()
