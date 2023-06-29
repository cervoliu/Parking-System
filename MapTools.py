###############################
#
# Map tools
#
# size = 50  # 每个方格的大小
#     row = 16
#     col = 11
#     dividing_line_width = 5  # 分割线宽度
###############################
import copy
import random

from Car import Car


class Stacks:
    depth = 0  # max element number, constant
    pos = []  # list of positions, e.g. [(1,3), (2,3), (3,3)], constant
    car = []  # list of cars

    def __init__(self, _pos) -> None:
        self.pos = _pos
        self.car = []
        self.depth = len(_pos)

    def num(self) -> int:  # number of element
        return len(self.car)

    def push(self, _car: Car):  # push a car
        if self.num() >= self.depth:
            print("stack is full, push failed")
            return False
        self.car.append(_car)
        return self.pos[self.num() - 1]

    def pop(self):
        if self.car != []:
            return self.car.pop()
        else:
            return None



class MapTools:
    width = 0
    height = 0
    square_size = 0
    font_size = 10
    stackDepth = 0

    DIVIDING_LINE_WIDTH = 5
    # Internal Variables
    w_map = None
    basic_map = None  # map no agv and car
    AGV_map = None
    # -3:  entry buffer
    # -2 :  exit
    #  -5 :  Temporary no access AGV
    #  -6 :  Temporary no access Car
    #   0 :  Open
    #  -1 :  parking lot
    #  -7 :  Temporary no access AGV and CAR
    ENTRY_BUFFER = -3
    EXIT = -2
    OPEN = 0
    PARKING_LOT = -1
    Car_TEMP_NO_ACC = -5
    AGV_TEMP_NO_ACC = -6
    TEMP_NO_ACC = -7

    AGVs = None
    parkingLotStacks = {}
    parking_space_pos = []
    occupied = set()
    buffer_pos = []
    Buffer_Size=0
    exit_pos = []
    stack_list = []
    cell_to_stack = {}

    # time counter
    time_counter = 0
    time_set_flag = False
    time_set = 0
    time_str = ""
    mode = 0  # 0 暂停   1 连续运行    2 非连续运行  3  设定时间   4   运行到指定时间

    # Constructor
    def __init__(self,
                 _square_size,
                 _width,
                 _height,
                 _depth,
                 _buffer,
                 _exit,
                 _parking_space,
                 _stack_list,
                 _cell_to_stack
                 ):

        self.square_size = _square_size
        self.width = _width
        self.height = _height
        self.stackDepth = _depth
        self.buffer_pos = _buffer
        self.Buffer_Size = len( self.buffer_pos )#.size()
        self.exit_pos = _exit
        self.parking_space_pos = _parking_space
        self.stack_list = _stack_list
        self.cell_to_stack = _cell_to_stack

        # self.stackDepth = _stack_depth
        # self.init_map()

    # Building map
    def init_map(self):
        self.w_map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.AGV_map = [[0 for i in range(self.width)] for j in range(self.height)]
        for each_buffer in self.buffer_pos:
            self.w_map[each_buffer[0]][each_buffer[1]] = self.ENTRY_BUFFER
        for each_exit in self.exit_pos:
            self.w_map[each_exit[0]][each_exit[1]] = self.EXIT
        for each_parking in self.parking_space_pos:
            self.w_map[each_parking[0]][each_parking[1]] = self.PARKING_LOT

            # 这部分改成 self.w_map[each_buffer] = self.ENTRY_BUFFER 等等是否更好 ?

        self.basic_map = copy.deepcopy(self.w_map)

        # for each_w in range(self.width):
        #     for each_h in range(self.height):
        #         if each_w == 0 and 1 <= each_h <= self.height - 2:
        #             self.w_map[each_w][each_h] = self.ENTRY_BUFFER
        #         if each_w == self.width-1 and 1 <= each_h <= self.height - 2:
        #             self.w_map[each_w][each_h] = self.EXIT

    # def init_stack(self):
    #     for()

    # add pos to occupied used by TskG simple
    def is_occupied(self, _pos):
        return _pos in self.occupied

    def occupy(self, _pos):
        self.occupied.add(_pos)

    def unoccupy(self, _pos):
        self.occupied.discard(_pos)

    def judge_in_parkinglot(self, _pos) -> bool:
        return _pos in self.parking_space_pos

    # Update w_map
    def update_map_car(self, _car):
        for each_car in _car:
            # 可能有的car还没有具体位置
            if each_car.get_current_pos() is not None :
                self.w_map[each_car.get_current_pos()[0]][each_car.get_current_pos()[1]] = each_car

    def update_map_agv(self, _agv):
        for each_agv in _agv:
            current_pos = each_agv.get_current_pos()
            self.w_map[current_pos[0]][current_pos[1]] = self.AGV_TEMP_NO_ACC
            # 直接就是AGV 不用ID
            self.AGV_map[current_pos[0]][current_pos[1]] = each_agv

    # Update map
    def update_map_by_agv(self, pos, status):
        self.w_map[pos[0]][pos[1]] = status

    def recover_map(self, _pos, _pre_status):
        self.w_map[_pos[0]][_pos[1]] = _pre_status

    def recover_map_to_basic(self, _pos):
        self.w_map[_pos[0]][_pos[1]] = self.basic_map[_pos[0]][_pos[1]]

    def recover_agv_map(self, _pos):
        self.AGV_map[_pos[0]][_pos[1]] = 0

    def set_agv_map(self, _pos, _agv):
        self.AGV_map[_pos[0]][_pos[1]] = _agv

    # def init_parking_stacks(self):
    def get_map_size(self):
        return self.width, self.height, self.square_size, self.DIVIDING_LINE_WIDTH, self.font_size

    def get_w_map(self):
        return self.w_map

    def get_basic_map(self):
        return self.basic_map

    def get_agv_map(self):
        return self.AGV_map

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_empty_buffer(self):
        for buffer in self.buffer_pos:
            if self.w_map[buffer[0]][buffer[1]] == self.ENTRY_BUFFER:
                return buffer

    def get_buffer_list(self):
        return self.buffer_pos

    def get_exit_list(self):
        return self.exit_pos

    def get_empty_exit(self):
        for exit in self.exit_pos:
            if exit not in self.occupied and self.get_agv_map()[exit[0]][exit[1]] == 0:
                print(exit, "is a empty exit")
                print(self.occupied, self.get_agv_map()[exit[0]][exit[1]])
                return exit
        return None

    def get_empty_park_pos_random(self):
        num = random.randint(0, len(self.parking_space_pos) - 1)
        while self.parking_space_pos[num] in self.occupied:
            num = random.randint(0, len(self.parking_space_pos) - 1)
        return self.parking_space_pos[num]

    def set_time(self, time):
        if time != 13:
            self.time_str += str(time - 48)
        else:
            self.time_set = int(self.time_str)
            print(self.time_str)
            self.time_str = ""

    def time_run(self):
        self.time_counter += 1

    def set_time_run(self):
        if self.time_counter >= self.time_set:
            self.mode = 0
