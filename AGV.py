import copy as cp
import pygame
import collision_check


class Agv:
    # basic Attributes
    ID = None  # AGV ID
    current_pos = None  # (x,y)
    direction = None  # up down left right

    # move related
    wait_time = 0
    total_waited_time = 0
    path = []
    MapTools = None
    collsionCheck = None

    # task related
    duty_type = None  # 0:Moving 1:parkCar  2:retrieve
    Task_list = []
    car_loaded = None
    Put_down_pos = None  # 1: agv put down a car last step  this is the pos
    pre_map_status = 0  # map status before agv go to the pos

    # agv_img paras
    agv_image = None
    agv_ID_image = None
    agv_rect = None
    speed = 0
    agv_state = None

    # Constructor
    def __init__(self, _id, _pos, _map_tools):
        self.ID = _id
        self.current_pos = _pos
        self.MapTools = _map_tools
        self.wait_time = 0
        self.status = 0
        self.path = []
        self.Task_list = []
        self.agv_state = 0

    # Update img information
    def update_img(self, _img, _speed, _font, _font_color):
        self.agv_image = _img
        self.agv_rect = self.agv_image.get_rect()
        self.speed = _speed
        self.agv_ID_image = _font.render(str(self.ID), True, _font_color)

    def update_pos(self):
        self.agv_rect.x = 5 + self.current_pos[1] * self.speed
        self.agv_rect.y = 5 + self.current_pos[0] * self.speed

    # img display
    def display(self, screen, map_tool):
        screen.blit(self.agv_image, self.agv_rect)
        screen.blit(self.agv_ID_image, (self.agv_rect.x + map_tool.square_size / 2 - map_tool.font_size, self.agv_rect.y
                                        + map_tool.square_size / 2 - map_tool.font_size))

    # Get ID
    def get_id(self):
        return self.ID

    # Get current position
    def get_current_pos(self):
        return self.current_pos
    
    # get end pos in path
    def get_end_pos(self):
        if self.path != []:
            return self.path[-1]
        else:
            return self.current_pos

    def get_current_task(self):
        if self.Task_list:
            current_task = self.Task_list[0]
            return current_task
        else:
            return None

    def del_current_task(self):
        del [self.Task_list[0]]

    def change_current_task(self, task):
        self.Task_list[0] = task

    def get_task_list(self):
        return self.Task_list

    def del_appoint_task(self, task):
        for each_task in self.Task_list:
            if each_task == task:
                self.Task_list.remove(each_task)

    # Get current position
    def get_direction(self):
        return self.direction

    # Get remained path length
    def get_remained_path_length(self):
        return len(self.path)

    # Get path
    def get_path(self):
        return cp.deepcopy(self.path)

    # add waiting time
    def add_waiting_time(self, _time):
        if self.wait_time == 0:
            self.wait_time += _time
            self.total_waited_time += _time

    # Add schedule path
    def add_path(self, _add_schedule):
        for each_add_schedule in _add_schedule:
            self.path.append(each_add_schedule)
            # if len(each_add_schedule) == 3:
            #     self.order.append(each_add_schedule[-1])

    # clear path
    def clear_path(self):
        self.path = []

    # add a task to task_list
    def add_task(self, _add_task):
        _add_task.task_is_scheduled()
        self.Task_list.append(_add_task)

    # Get duty type
    def get_duty(self):
        return self.duty_type

    # TODO Check for obstacles
    def check_no_obstacles(self) -> bool:
        pos = self.path[0]
        return self.check_no_obstacles_for_pos(pos)

    def check_no_obstacles_for_pos(self, pos) -> bool:
        x, y = pos
        car_map = self.MapTools.get_w_map()
        agv_map = self.MapTools.get_agv_map()
        if agv_map[x][y] != 0:
            # print(pos, "is agv", agv_map[x][y].ID)
            return False
        elif self.is_loaded() and not isinstance(car_map[x][y], int):
            # print(pos, "is car", car_map[x][y].ID)
            return False
        return True

    # TODO AGV move 增量更新 把车抬走前面点的恢复有点问题
    def move(self, _collision_check):
        if not self.wait_time == 0:
            # print("agv", self.ID, "waiting", "wait_time:", self.wait_time, "total wait:", self.total_waited_time)
            self.wait_time -= 1
        else:
            if not self.path == []:
                if self.Task_list != [] and self.current_pos == self.Task_list[0].get_st_pos() \
                        and self.car_loaded is not self.Task_list[0].get_car():
                    self.pick_up(self.Task_list[0].get_car())

                if self.check_no_obstacles():
                    # update w_map last pos
                    if self.Put_down_pos is None:
                        if self.car_loaded is None:
                            self.MapTools.recover_map(self.current_pos, self.pre_map_status)
                        else:
                            self.MapTools.recover_map(self.current_pos,
                                                      self.MapTools.get_basic_map()[self.current_pos[0]][
                                                          self.current_pos[1]])
                    else:
                        if self.current_pos not in self.MapTools.get_exit_list():
                            self.MapTools.update_map_by_agv(self.Put_down_pos, self.MapTools.Car_TEMP_NO_ACC)
                        # 退出区则瞬间恢复 此逻辑匹配退出区车辆瞬间消失
                        else:
                            self.MapTools.recover_map(self.current_pos, self.pre_map_status)
                        self.Put_down_pos = None

                    # update AGV current_pos
                    self.current_pos = self.path.pop(0)
                    self.clear_total_waiting()

                    # update w_map current pos
                    self.pre_map_status = self.MapTools.get_w_map()[self.current_pos[0]][self.current_pos[1]]
                    self.MapTools.update_map_by_agv(self.current_pos, self.MapTools.AGV_TEMP_NO_ACC)

                    if self.car_loaded is not None:  # move the car loaded
                        self.car_loaded.update_pos_by_agv(self.current_pos)
                        if not self.Task_list == [] and self.Task_list[0].get_car() \
                                is not None:  # need to pick or put
                            # if self.current_pos == self.Task_list[0].get_st_pos():
                            #     self.pick_up(self.Task_list[0].get_car())
                            if self.current_pos == self.Task_list[0].get_en_pos():
                                self.put_down(self.Task_list[0].get_car())
                                self.Task_list.pop(0)  # finish task
                    elif self.Task_list == [] and self.Task_list[0].get_type() == 0 and \
                            self.current_pos == self.Task_list[0].get_en_pos():
                        self.Task_list.pop(0)

                else:
                    if self.current_pos in self.MapTools.buffer_pos:
                        _collision_check.rearrange(self)
                    else:
                        self.wait_time = self.wait_time + 1
                        self.total_waited_time += 1
                        if self.total_waited_time > 3:
                            self.wait_time = 0
                            self.total_waited_time = 0
                            _collision_check.rearrange(self)

    def move_new(self, _collision_check):
        if not self.wait_time == 0:
            print("agv", self.ID, "waiting", "wait_time:", self.wait_time, "total wait:", self.total_waited_time)
            self.wait_time -= 1
        else:
            map_tool = self.MapTools
            car_map = map_tool.get_w_map()
            if not self.path == []:
                pre_pos = self.current_pos
                # 走前抬车
                if self.Task_list != [] and self.current_pos == self.Task_list[0].get_st_pos() \
                        and self.car_loaded is not self.Task_list[0].get_car():
                    aim_car = self.Task_list[0].get_car()
                    if car_map[pre_pos[0]][pre_pos[1]] != aim_car:
                        print("Error:", aim_car.get_id(), "not aim car")
                    self.pick_up(self.Task_list[0].get_car())

                if self.check_no_obstacles():

                    # recover AGV_map last pos
                    map_tool.recover_agv_map(pre_pos)

                    # update AGV current_pos
                    self.current_pos = self.path.pop(0)

                    # update AGV_map current pos
                    map_tool.set_agv_map(self.current_pos, self)

                    if self.car_loaded is not None:  # move the car loaded
                        self.car_loaded.update_pos_by_agv(self.current_pos)
                        if not self.Task_list == [] and self.Task_list[0].get_car() \
                                is not None:  # need to put
                            if self.current_pos == self.Task_list[0].get_en_pos():
                                self.put_down(self.Task_list[0].get_car())
                                self.Task_list.pop(0)  # finish task
                    elif not self.Task_list == [] and self.Task_list[0].get_type() == 0 and \
                            self.current_pos == self.Task_list[0].get_en_pos():
                        self.Task_list.pop(0)

                else:  # have obstacles
                    if self.current_pos in self.MapTools.buffer_pos:
                        _collision_check.rearrange(self)
                    else:
                        self.wait_time = self.wait_time + 1
                        self.total_waited_time += 1
                        if self.total_waited_time > 3:
                            self.wait_time = 0
                            self.total_waited_time = 0
                            _collision_check.rearrange(self)

    # pick up car
    def pick_up(self, _car):
        if self.car_loaded is not None:
            print("error: agv", self.get_id(), " has car and cant pick up")
        else:
            self.car_loaded = _car
            _car.update_agv_status(self.ID)

    # put down car
    def put_down(self, _car):
        if self.car_loaded is None:
            print("error: agv", self.get_id(), " has no car can put down")
        else:
            self.car_loaded = None
            self.Put_down_pos = self.current_pos
            _car.update_agv_status(None)

    def is_loaded(self) -> bool:
        if self.car_loaded is None:
            return False
        else:
            return True

    def get_car_load(self):
        return self.car_loaded

    def get_total_waiting(self):
        return self.total_waited_time

    def clear_total_waiting(self):
        self.total_waited_time = 0

    def get_map_tools(self):
        return self.MapTools
