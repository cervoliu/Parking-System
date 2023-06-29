from AGV import *
from Car import *
from PathSchedule import *
from MapTools import *
from TaskSchedule import *
from Generator import *
from Tasks import *
from GUI import *
from collision_check import *
from TaskGenerate import TaskGenerate
from TaskGenerate_simple import TaskGenerateSimple
import time
import pygame


def update_cars(_cars, _exit_pos, _map_tool, task_schedule):
    for car in _cars:
        if car.get_current_pos() in _exit_pos and car.get_car_status() is None:
            x, y = car.get_current_pos()
            _map_tool.unoccupy(car.get_current_pos())
            _map_tool.get_w_map()[x][y] = _map_tool.get_basic_map()[x][y]
            _cars.remove(car)

            # 瞬间消失的情况下，不会走到这
            # print("字典中agv的坐标",task_schedule.get_dict()[car][1].get_current_pos(),"car 的坐标",car.get_current_pos())
            # if task_schedule.get_dict()[car][1].get_current_pos() != car.get_current_pos():
            #     pos_x, pos_y = car.get_current_pos()
            #     _map_tool.get_w_map()[pos_x][pos_y] = _map_tool.get_basic_map()[pos_x][pos_y]


def test_path(pather):
    agv = pather.Agv_list[0]
    agv.car_loaded = Car.Car(1, (0, 0), agv.MapTools)
    pather.add_path_to_an_agv(agv, agv.get_current_pos(), (5, 5))


def add_stack(a, b, c):
    a.append(Stacks(c))
    for i in c:
        b[i] = a[-1]


# Main method
def main():
    # map information
    buffer_pos = [(i, 0) for i in range(1, 15)]
    exit_pos = [(i, 10) for i in range(1, 15)]
    # parking_pos = [(i, j) for j in range(3, 8) for i in [ 1, 2, 5, 6, 9, 10,  13, 14]] normal parking
    parking_pos = [(i, j) for j in range(3, 8) for i in [0, 1, 2, 5, 6, 7, 8, 9, 10, 13, 14, 15]]
    stack_list = []
    cell_to_stack = {}
    for j in range(3, 8):
        add_stack(stack_list, cell_to_stack, [(i, j) for i in [0, 1, 2]])
        add_stack(stack_list, cell_to_stack, [(i, j) for i in [7, 6, 5]])
        add_stack(stack_list, cell_to_stack, [(i, j) for i in [8, 9, 10]])
        add_stack(stack_list, cell_to_stack, [(i, j) for i in [15, 14, 13]])

    map_tool = MapTools(50, 12, 16, 3, buffer_pos, exit_pos, parking_pos, stack_list, cell_to_stack)
    # constants meaning : square_size, width , height, stack_depth

    map_tool.init_map()

    generator = Generator()

    Cars_buffer = []  # 缓冲区 list
    Cars_pick = []  # 取车list
    Cars = []  # 系统内所有车辆
    AGVs = [Agv(i, (i, 1), map_tool) for i in range(4, 10)]
    map_tool.update_map_agv(AGVs)
    Path_Schedule = PathSchedule(AGVs, map_tool)

    detect_range = 2
    default_wait_time = 1
    Collision_Check = CollisionCheck(Path_Schedule, detect_range, default_wait_time)

    task_schedule = TaskSchedule([], AGVs, [])
    # task_generate = TaskGenerateSimple(map_tool)
    task_generate = TaskGenerate(map_tool)

    parking_map = GUI(map_tool)
    parking_map.draw_background(map_tool)
    update_cars(Cars, exit_pos, map_tool, task_schedule)
    parking_map.gui_run(Cars, AGVs, map_tool)

    MYEVENT01 = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENT01, 500)  # 定时器 500ms
    clock = pygame.time.Clock()
    framerate = pygame.time.Clock()  # 实例化一个之中对象

    # TODO
    # task_schedule.add_tasks_list(task_generate.get_task_list())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MYEVENT01 and (map_tool.mode == 1 or map_tool.mode == 2 or map_tool.mode == 4):
                map_tool.time_run()
                generator.read_data()
                generator.generator_car(Cars_buffer, map_tool)
                generator.get_car_out(Cars_pick, Cars)
                Cars.extend(Cars_buffer)

                task_generate.park(Cars_buffer)
                task_generate.retrieve(Cars_pick)
                task_schedule.add_tasks_list(task_generate.get_task_list())
                task_generate.task_list_clear()

                task_schedule.task_schedule_random()
                Path_Schedule.path_schedule_for_no_path_agvs()

                for each_agv in AGVs:
                    if Collision_Check.check_simple(each_agv, AGVs, cell_to_stack): each_agv.move_new(Collision_Check)

                if map_tool.mode == 2:
                    map_tool.mode = 0
                if map_tool.mode == 4:
                    map_tool.set_time_run()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if parking_map.click_button() == 1:
                    map_tool.mode = 0
                elif parking_map.click_button() == 2:
                    map_tool.mode = 1
                elif parking_map.click_button() == 3:
                    map_tool.mode = 2
                elif parking_map.click_button() == 4:
                    map_tool.mode = 3
            if map_tool.mode == 3 and event.type == pygame.KEYDOWN:
                parking_map.input_time()
            parking_map.mouse_bright_display()
            parking_map.time_display(map_tool.time_counter)
            parking_map.button_set_time()
            parking_map.mode_display()
            update_cars(Cars, exit_pos, map_tool, task_schedule)
            parking_map.gui_run(Cars, AGVs, map_tool)
            framerate.tick(60)  # 控制循环为30帧/秒
            # print(map_tool.get_w_map());


if __name__ != "__main__":
    pass
# Trigger
else:
    main()
