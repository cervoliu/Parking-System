###############################
#
# Car
#
#
#
#
###############################
import pygame


class Car:
    # basic Attributes
    ID = None
    Estimated_exit_time = None
    current_pos = None
    object_pos = None

    # Internal Variable
    status = None
    On_AGV = None  # AGV ID
    Map_tools = None

    # Constructor

    # agv_img paras
    car_image = None
    car_ID_image = None
    car_rect = None
    speed = None
    car_state = None

    def __init__(self, _id, _pos, _tools):
        self.ID = _id
        self.current_pos = _pos

        self.status = "nothing"
        self.on_AGV = None
        self.Map_tools = _tools

        self.car_state = 1

    def update_pos_by_agv(self, _pos):
        x, y = self.current_pos
        self.Map_tools.get_w_map()[x][y] = self.Map_tools.get_basic_map()[x][y]
        self.current_pos = _pos
        self.Map_tools.get_w_map()[self.current_pos[0]][self.current_pos[1]] = self

    def update_img(self, _img, _speed, _font, _font_color):
        self.car_image = _img
        self.car_rect = self.car_image.get_rect()
        self.speed = _speed
        self.car_ID_image = _font.render(str(self.ID), True, _font_color)

    def update_pos(self):
        self.car_rect.x = 5 + self.current_pos[1] * self.speed
        self.car_rect.y = 5 + self.current_pos[0] * self.speed

    # img display
    def display(self, screen, map_tool):
        screen.blit(self.car_image, self.car_rect)
        screen.blit(self.car_ID_image, (self.car_rect.x + map_tool.square_size / 2 - map_tool.font_size, self.car_rect.y
                                        + map_tool.square_size / 2 - map_tool.font_size))

    # Set self status
    def update_status(self, _status):
        self.status = _status

    # Update on AGV status
    def update_agv_status(self, _agv_id):
        self.On_AGV = _agv_id

    def get_car_status(self):
        return self.On_AGV

    # Coloring the shelf
    def update_coloring(self):
        if self.status == "nothing":
            self.tools.ChangeColorObject(self.ID, color=self.tools.GetShelfNothing_Color())
        elif self.status == "waiting":
            self.tools.ChangeColorObject(self.ID, color=self.tools.GetShelfWaiting_Color())
        elif self.status == "moving":
            self.tools.ChangeColorObject(self.ID, color=self.tools.GetShelfMoving_Color())

    # Update
    def update(self, _each_shelf_occupancy):
        self.update_agv_status(_each_shelf_occupancy)
        if self.on_AGV is None and not len(self.orders) == 0:
            self.update_status("waiting")
        elif self.on_AGV is not None:
            self.update_status("moving")
        else:
            self.update_status("nothing")
        self.update_coloring()

    def get_current_pos(self):
        return self.current_pos
    
    def get_object_pos(self):
        if self.object_pos == None:
            return self.current_pos
        else:
            return self.object_pos

    def set_object_pos(self, obj_pos) -> None:
        self.object_pos = obj_pos

    def get_id(self):
        return self.ID

    def judge_in_buffer(self):
        return not self.current_pos[1]