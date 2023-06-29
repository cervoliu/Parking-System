from normal_astar import *
from AGV import *

# # TODO finish astar
# def a_star(_start: (int, int), _end: (int, int)):
#     return None


class PathSchedule:
    Agv_list = []
    map_tool = None

    def __init__(self, _agv, _map_tool):
        self.Agv_list = _agv
        self.map_tool = _map_tool

    def path_schedule_for_no_path_agvs(self):
        for each_agv in self.Agv_list:
            if (each_agv.get_path() == []) and each_agv.get_current_task() is not None:
                current_task = each_agv.get_current_task()
                # each_agv.del_current_task()
                self.add_path_to_an_agv(each_agv, each_agv.get_current_pos(), current_task.get_st_pos())
                self.add_path_to_an_agv(each_agv, current_task.get_st_pos(), current_task.get_en_pos())

    def add_path_to_an_agv(self, _agv, _st_pos, _ed_pos):
        print("agv", _agv.get_id(), "start use best path", _st_pos, _ed_pos)
        Path_to_add = BestPath(_st_pos, _ed_pos, self.map_tool, _agv.is_loaded(),_agv)
        _agv.add_path(Path_to_add)
        print("agv", _agv.get_id(), "after add path", _agv.get_path())
        
    

    def temp_add_path_to_an_agv(self, _agv, _path):
        _agv.add_path(_path)

    #重新规划一个AGV的路径
    def re_schedule_for_an_agv(self, _agv):
        _agv.clear_path()
        if _agv.get_current_task() is not None:
            current_task = _agv.get_current_task()
            if not _agv.get_car_loaded() == current_task.get_car():
                self.add_path_to_an_agv(_agv, _agv.get_current_pos(), current_task.get_st_pos())
                self.add_path_to_an_agv(_agv, current_task.get_st_pos(), current_task.get_ed_pos())
            else:
                self.add_path_to_an_agv(_agv, _agv.get_current_pos(), current_task.get_ed_pos())

    
    # def add_path_to_an_agv_tea(self,_agv):
    #     Path_to_add = BestPath_TEA(_st_pos, _ed_pos, self.map_tool, _agv.is_loaded(),_agv)
    #     _agv.add_path(Path_to_add)
    
    def schedule_all_tasks_path_for_agvs(self):
        for each_agv in self.Agv_list:
            self.schedule_all_path_for_agv(each_agv)
    
    def schedule_all_path_for_agv(self,_agv):
        _agv.clear_path()
        for task in _agv.get_task_list():
            if not _agv.get_car_loaded() == task.get_car():
                self.add_path_to_an_agv_tea(_agv, _agv.get_end_pos(), task.get_st_pos())
                self.add_path_to_an_agv_tea(_agv, task.get_st_pos(), task.get_ed_pos())
            else:
                self.add_path_to_an_agv_tea(_agv, _agv.get_end_pos(), task.get_ed_pos())
        
    def add_agv_list(self, _agv_list):
        self.Agv_list = _agv_list
