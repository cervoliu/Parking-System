from Car import *
from GUI import *
from AGV import *


class Generator:
    input_data = []
    input_line_data = []
    file = None

    MAX_STRING = 100  # 同一时刻最多有多少辆车进入和出去

    def __init__(self, _file_name='input.txt'):
        self.file = open(_file_name)

    def read_data(self):
        line = self.file.readline(self.MAX_STRING)
        self.input_line_data = line.strip().split(" ")
        self.input_data.append(self.input_line_data[:])

    def get_line_data(self):
        return self.input_line_data

    def get_car_in(self):
        if self.input_line_data == ['']:
            return False
        if self.input_line_data[0] != '0':
            return self.input_line_data[2:2 + int(self.input_line_data[0])]
        else:
            return []

    def get_car_out(self, _cars_out, _cars):
        if self.input_line_data == ['']:
            return False
        if self.input_line_data[1] != '0':
            cars_str = self.input_line_data[2 + int(self.input_line_data[0]):2 + int(self.input_line_data[0]) + int(
                self.input_line_data[1])]
            for car_id in cars_str:
                for each_car in _cars:
                    if each_car.get_id() == int(car_id):
                        _cars_out.append(each_car)

    def generator_car(self, _cars: [], _map):
        if not self.get_car_in():
            return _cars
        car_in = self.get_car_in()
        for car in car_in:
            _cars.append(Car(int(car), _map.get_empty_buffer(), _map))
            _map.update_map_car(_cars)






# buffer_pos = [(i, 0) for i in range(1, 15)]
# exit_pos = [(i, 10) for i in range(1, 15)]
# parking_pos = [(i, j) for j in range(3, 8) for i in [0, 1, 2, 5, 6, 7, 8, 9, 10, 13, 14, 15]]
#
# map_tool = MapTools(50, 11, 16, buffer_pos, exit_pos, parking_pos)  # square_size, width , height
# map_tool.init_map()
# generator = Generator()
# Cars = []
# AGVs = [Agv(1, (0, 0), map_tool)]
# generator.read_data()
# print(generator.generator_car(Cars, map_tool))
