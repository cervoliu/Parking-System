from MapTools import MapTools
from Car import Car
from Tasks import *


class TaskGenerateSimple:
    task_list = []
    map_tool = None

    # buffer to parking_area
    def __init__(self, _map_tool: MapTools) -> None:
        self.task_list = []
        self.map_tool = _map_tool

    def park(self, cars) -> None:
        for each_car in cars:
            object_pos = self.map_tool.get_empty_park_pos_random()
            if object_pos is None:
                print("no parkinglot")
            else:
                self.map_tool.occupy(object_pos)
                self.task_list.append(Tasks(1, each_car, each_car.get_current_pos(), object_pos))
                cars.remove(each_car)

    # parking_area to parking_area
    def move(self) -> None:
        pass

    # parking_area to buffer
    def retrieve(self, cars) -> None:
        for each_car in cars:
            pos = each_car.get_object_pos()
            object_pos = self.map_tool.get_empty_exit()
            if object_pos is None:
                print("no exit")
                return
            else:
                self.map_tool.occupy(object_pos)
                self.map_tool.unoccupy(pos)
                self.task_list.append(Tasks(2, each_car, pos, object_pos))
                each_car.set_object_pos(object_pos)
                cars.remove(each_car)

    def get_task_list(self):
        return self.task_list

    def task_list_clear(self):
        self.task_list.clear()
