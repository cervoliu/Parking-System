from copy import copy
from tkinter.messagebox import NO
import main
from AGV import *
from Car import *
from MapTools import *
from TaskSchedule import *
from Tasks import *
from GUI import *
import time
from PathSchedule import *


class CollisionCheck:
    Path_Schedule = None
    Default_wait_time = 1  # const///////////////////改成1应该没问题
    range = 2

    def __init__(self, _path_schedule, _range=2, _default_wait_time=3):
        self.Path_Schedule = _path_schedule
        self.range = _range
        self.Default_wait_time = _default_wait_time

    def agv_dis(self, agv_1, agv_2):
        return abs(agv_1.current_pos[0] - agv_2.current_pos[0]) + abs(agv_1.current_pos[1] - agv_2.current_pos[1])
    def point_dis(self, P1, P2):
        return abs(P1[0] - P2[0]) + abs(P1[1] - P2[1])

    def get_new_path(self, agv, st_pos, ed_pos):
        origin_path_size = len(agv.get_path())  # agv当前的路径长度
        if agv.is_loaded():
            self.Path_Schedule.add_path_to_an_agv(agv, st_pos, ed_pos)  # loaded的a星
        else:
            self.Path_Schedule.add_path_to_an_agv(agv, st_pos, ed_pos)  # 没有load的a星
        if not len(agv.get_path()) == origin_path_size: return True  # 成功找到了新的路径
        return False

    def rearrange(self, agv):  # 进行重新规划
        origin_path = agv.get_path()  # 保存原来的路径
        agv.clear_path()  # 清空路径，进行重新规划
        ok = True
        current_task = agv.get_current_task()  # 会有无task的情况吗？agv.get_current_task() is not None
        if current_task is not None:
            if agv.is_loaded():
                print(current_task.get_en_pos())
                ok = ok and self.get_new_path(agv, agv.current_pos, current_task.get_en_pos())  # 已经带车直奔终点
            else:
                if agv.get_current_pos() != current_task.get_st_pos():
                    ok = ok and self.get_new_path(agv, agv.current_pos, current_task.get_st_pos())  # 先去起点取车
                ok = ok and self.get_new_path(agv, current_task.get_st_pos(), current_task.get_en_pos())  # 取车后直奔终点
            if ok:  # 每一步重新规划均成功
                return True
            agv.clear_path()  # 清除可能存在的不完全成功路径，还原路径
            agv.add_path(origin_path)
            agv.add_waiting_time(self.Default_wait_time)  # 重新规划失败，agv等待
        else:
            agv.add_waiting_time(self.Default_wait_time)
        # if agv.get_total_waiting() > 10:  # 调用瞎走方法
        #     print("agv", agv.ID, "trial")
        #     return self.trial_step(agv)
        return False

    def check_simple(self, agv_1, agvs, cell_stkid):
        if not agv_1.path: return True
        if agv_1.wait_time != 0: return True
        
        # 终点所在栈是否被占用 + 范围试探
        stack_range=1000 # 距离栈多远开始考虑判断
        current_task = agv_1.get_current_task()  # 既然有路径，应该有任务
        if current_task is not None:
            end_pos = current_task.get_en_pos()
            stk = cell_stkid.get(end_pos)
            if stk is not None:
                if self.point_dis(stk.pos[0], agv_1.current_pos) <= stack_range: #在范围内，需要判断
                    #print("checking if stack occupied")
                    for each_agv in agvs :
                        if each_agv.ID == agv_1.ID: continue
                        if not each_agv.path: continue
                        if each_agv.current_pos in stk.pos: #正在走且在终点栈中，相当于终点栈正在被占用
                            return False
        
        
        # constants
        done = False
        no_collision = True
        # //////地图障碍
        if not agv_1.check_no_obstacles():
            if self.rearrange(agv_1):  # 有障碍，直接试图重新规划
                done = True  # 规划成功
            else:  # 无路可走
                print("agv", agv_1.ID, "checked false")
                # self.wait_new(agv_1, justwait)
                return False
        else:
            return True

        #预留的方向内容
        #now_pos = agv_1.get_current_pos() 
        #agv_1_dir= 1*(nxt_pos[0]-now_pos[0]) + 2*(nxt_pos[1]-now_pos[1])
            #2:上 -2:下 -1:左 1:右 

        agv_1_nxt_pos = agv_1.path[0]   #agv_1的下一位置
        # /////Agv之间
        for each_agv in agvs:
            if agv_1.ID == each_agv.ID: continue

            if each_agv.path == [] : continue   #each_agv静止相当于地图障碍，已经判断过，不会产生冲突
            else :
                #预留的方向内容
                #now_pos = each_agv.get_current_pos()
                #nxt_pos = each_agv.path[0]
                #each_agv_dir=1*(nxt_pos[0]-now_pos[0]) + 2*(nxt_pos[1]-now_pos[1])
                #and not each_agv_dir==agv_1_dir
                
                each_agv_nxt_pos = each_agv.path[0] #each_agv的下一位置
                #在range<=2时，当且仅当两者下一位置相同时产生冲突
            if self.agv_dis(agv_1, each_agv) <= self.range and agv_1_nxt_pos==each_agv_nxt_pos:  # 确定与agv1发生冲突的each_agv
                if not each_agv.get_task_list():###当前开启试探步
                    self.trial_step(each_agv)###
                no_collision = False  # agv之间存在冲突
                if done == False:  # 未进行重新规划
                    if self.rearrange(agv_1):
                        done = True  # 重新规划成功
                    else:
                        break  # 重新规划失败，让agv_1等待即可，同时跳出循环不影响其他agv
                if done == True: each_agv.add_waiting_time(self.Default_wait_time)  # 重新规划成功，让其他可能与agv1冲突的each_agv等待
        # 最后总结
        if done == True or no_collision == True:  # 重新规划成功或未发生冲突
            return True
        else:
            print("agv", agv_1.ID, "cannot go")
            # self.wait_new(agv_1, justwait)
            return False

    # 试探步 长时间等待后试探的往周围走一下
    def trial_step(self, agv):
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dir in dirs:
            dir1 = agv.get_current_pos()[0] + dir[0]
            dir2 = agv.get_current_pos()[1] + dir[1]
            if 0 <= dir1 < agv.get_map_tools().get_height() and 0 <= dir2 < agv.get_map_tools().get_width() and \
                    agv.check_no_obstacles_for_pos((dir1, dir2)):
                agv.clear_path()
                agv.add_path([(dir1, dir2)])
                # agv.move_new(self)
                print("agv", agv.ID, "trial", agv.path)
                agv.clear_total_waiting()
                return True
        return False
