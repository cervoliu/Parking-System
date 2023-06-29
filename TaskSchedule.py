import random


class TaskSchedule:
    agv_seq = []
    task_seq = []
    path = []
    car_to_task_agv = {}  # car:(task ,agv)

    def __init__(self, _tasks, _agv, _path):
        self.task_seq = _tasks
        self.agv_seq = _agv
        self.path = _path

    def task_schedule_random(self):
        for each_task in self.task_seq:
            if each_task.get_type() == 2: #retrieve
                if each_task.get_car().get_car_status() is not None:  # car 在路上
                    agv_id = each_task.get_car().get_car_status()
                    car_id = each_task.get_car().get_id()
                    for each_agv in self.agv_seq:
                        if each_agv.get_car_load() is not None and each_agv.get_car_load().get_id() == car_id:
                            self.car_to_task_agv[each_task.get_car()] = (each_task, each_agv)
                            each_agv.clear_path()
                            each_agv.change_current_task(each_task)
                            print("Car 在路上,",agv_id,"exit:",car_id,each_task.get_st_pos(),each_task.get_en_pos())
                elif each_task.get_car().get_car_status() is None and each_task.get_car().judge_in_buffer(): # car在buffer
                    current_agv = self.car_to_task_agv[each_task.get_car()][1]
                    current_car = each_task.get_car()
                    if current_agv.get_current_task().get_car() is not current_car:         # Pick 的agv 有其他任务
                        for each_agv_task in current_agv.get_task_list():
                            if each_agv_task.get_car() == each_task.get_car():
                                current_agv.del_appoint_task(each_agv_task)
                        num = random.randint(0, len(self.agv_seq) - 1)
                        self.car_to_task_agv[current_car] = (each_task, self.agv_seq[num])
                        self.agv_seq[num].add_task(each_task)
                        print("Car 在buffer,", self.agv_seq[num].get_id(), "exit:", each_task.get_car().get_id(), each_task.get_st_pos(),
                              each_task.get_en_pos())
                        print(len(self.agv_seq[num].get_task_list()))
                    else:                                                               # Pick 的agv 正在pick current car
                        current_agv.clear_path()
                        current_agv.get_task_list()[0] = each_task
                        self.car_to_task_agv[current_car] = (each_task, current_agv)
                        print("Car 在buffer,", current_agv.get_id(), "exit:", current_car.get_id(), each_task.get_st_pos(),
                              each_task.get_en_pos())
                else:
                    for each_agv in self.agv_seq:
                        if each_agv.get_current_pos() == each_task.get_st_pos():
                            self.add_task_to_agv(each_agv, each_task)
                            each_task.task_is_scheduled()
                    if not each_task.get_task_schedule():
                        num = random.randint(0, len(self.agv_seq) - 1)
                        for each_task_2 in self.task_seq:
                            if each_task_2.get_master_car() == each_task.get_car():
                                self.add_task_to_agv(self.agv_seq[num], each_task_2)
                                self.task_seq.remove(each_task_2)
                        self.add_task_to_agv(self.agv_seq[num], each_task)
                    print("Car 在park,")
            if each_task.get_type() == 1: #park
                num = random.randint(0, len(self.agv_seq) - 1)
                self.add_task_to_agv(self.agv_seq[num], each_task)

        # self.agv_seq[num].add_path(self.path)
        self.task_seq.clear()

    # def no_task_agv_check(self):
    #     for each_agv in self.agv_seq:
    #         if not each_agv.get_task_list() :
    #             cur_pos=each_agv.get_current_pos()
    #             MapTools=each_agv.get_map_tools()
    #             if cur_pos in MapTools.is_occupied() :



    def add_a_task(self, _task):
        self.task_seq.append(_task)

    def add_tasks_list(self, _task_list):
        self.task_seq += _task_list

    def add_task_to_agv(self, agv, task):
        agv.add_task(task)
        current_car = task.get_car()
        self.car_to_task_agv[current_car] = (task, agv)
        print("car", current_car.get_id(), "assigned to agv:", self.car_to_task_agv[current_car][1].get_id())

    def get_dict(self):
        return self.car_to_task_agv
