from MapTools import MapTools
from Car import Car
from Tasks import *


class TaskGenerate:
    task_list = []
    map_tool = None

    def __init__(self, _map_tool: MapTools) -> None:
        self.task_list = []
        self.map_tool = _map_tool

    # to parking area
    def park(self, cars, master_car=None) -> None:
        for each_car in cars:
            pos = each_car.get_object_pos()
            ban = None
            if self.map_tool.judge_in_parkinglot(pos):  # case of move
                ban = self.map_tool.cell_to_stack[pos]
            obj_stk = None
            for stk in self.map_tool.stack_list:
                if stk is ban:
                    continue
                if obj_stk == None or stk.num() < obj_stk.num():
                    obj_stk = stk
            obj_pos = obj_stk.push(each_car)
            for stk in self.map_tool.stack_list:
                print(stk.num())
            if obj_pos == False:
                print("No available parking lot, park failed")
                return
            self.map_tool.occupy(obj_pos)
            if ban is None:  # case of park
                type = 1
            else:  # case of move
                type = 2
            self.task_list.append(Tasks(type, each_car, pos, obj_pos, master_car))
            each_car.set_object_pos(obj_pos)
            cars.remove(each_car)
        # cars.clear()

    """
    def retrieve(self, cars) -> None:
        for each_car in cars:
            object_pos = self.map_tool.get_empty_exit()
            self.map_tool.add_pos_to_occupied(object_pos)
            self.map_tool.remove_pos_from_occupied(each_car.get_current_pos())
            self.task_list.append(Tasks(2, each_car, each_car.get_current_pos(), object_pos))
        cars.clear()
    
    def move(self, cars) -> None:
        for each_car in cars:
            object_pos = 
            self.task_list.append(Tasks(1, each_car, each_car.get_current_pos(), object_pos))
        cars.clear()
    """

    # parking_area to exit
    def retrieve(self, cars) -> None:
        for each_car in cars:
            pos = each_car.get_object_pos()
            current_pos = each_car.get_current_pos()
            if self.map_tool.judge_in_parkinglot(pos):
                stk = self.map_tool.cell_to_stack[pos]
                move_list = []
                while True:
                    cur_car = stk.pop()
                    if cur_car == each_car or cur_car is None:
                        break
                    move_list.append(cur_car)
                self.park(move_list, cur_car)
            obj_pos = self.map_tool.get_empty_exit()
            if obj_pos is None:
                print("no exit")
                return
            else:
                self.map_tool.occupy(obj_pos)
                self.map_tool.unoccupy(pos)
                self.task_list.append(Tasks(2, each_car, pos, obj_pos))
                each_car.set_object_pos(obj_pos)
                cars.remove(each_car)

    def get_task_list(self):
        return self.task_list

    def task_list_clear(self):
        self.task_list.clear()
