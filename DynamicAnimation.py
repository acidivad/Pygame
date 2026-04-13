import pygame as pg
import json

"""

acidivad was here


"""


ANIM_EVENT_INDEX = pg.event.custom_type()
def set_next_frame_timer(index=ANIM_EVENT_INDEX, parent=None, delay=100):
    pg.time.set_timer(pg.Event(index, parent=parent), delay, loops=1)


def load_animation_config(folder_path: str):
    with open(f"{folder_path}animConfig.json", "r") as fp:
        return json.load(fp)
    

class SpriteSheetLoader:
    def __init__(self, img_path, tileSize, tileResize):
        self.img_path = img_path
        self.tileSize = tileSize
        self.tileResize = tileResize
        self.sheet = pg.image.load(img_path).convert_alpha()

    def get_slices(self, row=0):
        slices = []
        n = self.sheet.width // self.tileSize
        for i in range(n):
            offset = (-i * self.tileSize, row * self.tileSize)
            surf = pg.Surface((self.tileSize, self.tileSize))
            surf.blit(self.sheet, offset)
            
            _surf = pg.transform.scale(surf,
                (self.tileResize, self.tileResize)
            )
            slices.append(_surf)

        return slices
    
    def get_rows(self, row_names=[]):
        rows = {}
        for y, name in enumerate(row_names):
            slices = self.get_slices(row=y)
            rows.update({name: slices})
        
        return rows


def load_animation(folder_path: str):
    config = load_animation_config(folder_path)
    tileSize = config["tileSize"]
    tileResize = config["tileResize"]
    anim_name = config["animName"]
    states = config["states"]

    anims = {}

    for state_name, info in states.items():
        slices = SpriteSheetLoader(
            folder_path + info["img"],
            tileSize,
            tileResize
        ).get_slices()

        info.update({"frames": slices})
        anims.update({state_name: info})
    
    return anim_name, anims


ANIM_CACHE = {}
def store_animation_info(folder_path):
    anim_name, anim_states = load_animation(folder_path)
    ANIM_CACHE.update({anim_name: anim_states})


MAX_FRAME_INDEX = 32
class Anim:
    def __init__(self, anim_name: str):
        self.anim_name = anim_name
        self.states = ANIM_CACHE[anim_name]
        self.state = list(self.states.keys())[0]
        self.frame_index = 0
        self.facing = "right"

        self.update_frame(0)
        set_next_frame_timer(
            parent=self,
            delay=self.frame_duration
        )


    @property
    def frame_duration(self):
        return self.states[self.state]["frameDuration"]


    def set_state(self, new_state):
        state = self.states[self.state]
        if "unskipable" in state.keys(): return
        if self.state == new_state: return

        self.state = new_state
        state = self.states[new_state]

        self.frame_index = 0
        self.update_frame(0)


    def update_frame(self, _index=1):
        self.frame_index += _index
        if self.frame_index >= MAX_FRAME_INDEX:
            self.frame_index = 0

        state = self.states[self.state]
        frames = state["frames"]
        index = self.frame_index % len(frames)

        index_bigger = self.frame_index >= len(frames)
        if "nextState" in state.keys() and index_bigger:
            self.state = state["nextState"]

        self.image = frames[index]
        if self.facing == "left":
            self.image = pg.transform.flip(
                self.image,
                True, False
            )