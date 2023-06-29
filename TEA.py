



class TEAstar:
    
    Map_Tool = None
    Time_window = 100
    map_width = 0
    map_height = 0
    
    def __init__(self, _agv, _map_tool):
        self.Agv_list = _agv
        self.Map_Tool = _map_tool
        self.map_width = _map_tool.get_width()
        self.map_height = _map_tool.get_height()
    
    
    class Cpoint():
        def __init__(self, x=0, y=0, t=0):
            self.x = x
            self.y = y
            self.f = t
            self.t = 0
            self.g = 0
            self.h = 0
            self.parent = None
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f <= other.f

    def __str__(self):
        return f'x={self.x} y={self.y}'

    def __repr__(self):
        return self.__str__()


    class List():
        def __init__(self, parent, next):
            self.parent = parent
            self.next = next


    vec = []


    def Exsit(self,vec, p):
        for cpoint in vec:
            if cpoint.x == p.x and cpoint.y == p.y:
                return True
        return False


    def FindItem(self,vec, p):
        if self.Exsit(vec, p):
            for cpoint in vec:
                if cpoint.x == p.x and cpoint.y == p.y:
                    return cpoint
            return None
        return None


    def FindItemIter(self,vec, p):
        if self.Exsit(vec, p):
            for index, cpoint in enumerate(vec):
                if cpoint.x == p.x and cpoint.y == p.y:
                    return index
            return len(vec) - 1
        return len(vec) - 1


    def Score(beginner, ended, cur):
        cur.g = abs(beginner.x - cur.x) + abs(beginner.y - cur.y)
        cur.h = abs(ended.x - cur.x) + abs(ended.y - cur.y)
        cur.f = cur.g + cur.h
        # print(f'g = {cur.g}')
        # print(f'h = {cur.h}')
        # print(f'f = {cur.f}')


    def check(pos, map_tool, is_loaded, _agv) -> bool:
        x = pos[0]
        y = pos[1]
        car_map = map_tool.get_w_map()
        agv_map = map_tool.get_agv_map()
        if agv_map[x][y] != 0 and agv_map[x][y] != _agv:
            return False
        elif is_loaded and not isinstance(car_map[x][y], int):
            return False
        return True


    def check_all_buffer_or_exit(pos1, pos2, map_tool) -> bool:
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos1[1]
        if pos1 in map_tool.get_buffer_list() and pos2 in map_tool.get_buffer_list():
            return False
        if pos1 in map_tool.get_exit_list() and pos2 in map_tool.get_exit_list():
            return False
        return True


    def FindChildren(self,first, map_tool, beginner, ended, open, close, height, width, is_loaded, _agv):
        bValid = False
        x = first.x
        y = first.y
        if first.x - 1 >= 0 and self.check((first.x - 1, first.y), map_tool, is_loaded, _agv) \
                and self.check_all_buffer_or_exit((x, y), (x - 1, y), map_tool):
            left = self.Cpoint(first.x - 1, first.y)
            self.Score(beginner, ended, left)
            if not self.Exsit(open, left) and not self.Exsit(close, left):
                left.parent = first
                open.append(left)
                bValid = True
            elif self.Exsit(open, left):
                old_open = self.FindItem(open, left)
                if left.f < old_open.f:
                    old_open.f = left.f
                    old_open.parent = first
            else:
                old_close = self.FindItem(close, left)
                if left.f < old_close.f:
                    old_close.f = left.f
                    old_close.parent = first
                    close.pop(self.FindItemIter(close, left))
                    open.append(left)

        if first.x + 1 < height and self.check((first.x + 1, first.y), map_tool, is_loaded, _agv) \
                and self.check_all_buffer_or_exit((x, y), (x + 1, y), map_tool):
            right = self.Cpoint(first.x + 1, first.y)
            self.Score(beginner, ended, right)
            if not self.Exsit(open, right) and not self.Exsit(close, right):
                right.parent = first
                open.append(right)
                bValid = True
            elif self.Exsit(open, right):
                old_open = self.FindItem(open, right)
                if right.f < old_open.f:
                    old_open.f = right.f
                    old_open.parent = first
            else:
                old_close = self.FindItem(close, right)
                if right.f < old_close.f:
                    old_close.f = right.f
                    old_close.parent = first
                    close.pop(self.FindItemIter(close, right))
                    open.append(right)

        if first.y - 1 >= 0 and self.check((first.x, first.y - 1), map_tool, is_loaded, _agv) \
                and self.check_all_buffer_or_exit((x, y), (x, y - 1), map_tool):
            bottom = self.Cpoint(first.x, first.y - 1)
            self.Score(beginner, ended, bottom)
            if not self.Exsit(open, bottom) and not self.Exsit(close, bottom):
                bottom.parent = first
                open.append(bottom)
                bValid = True
            elif self.Exsit(open, bottom):
                old_open = self.FindItem(open, bottom)
                if bottom.f < old_open.f:
                    old_open.f = bottom.f
                    old_open.parent = first
            else:
                old_close = self.FindItem(close, bottom)
                if bottom.f < old_close.f:
                    old_close.f = bottom.f
                    old_close.parent = first
                    close.pop(self.FindItemIter(close, bottom))
                    open.append(bottom)

        if first.y + 1 < width and self.check((first.x, first.y + 1), map_tool, is_loaded, _agv) \
                and self.check_all_buffer_or_exit((x, y), (x, y + 1), map_tool):
            top = self.Cpoint(first.x, first.y + 1)
            self.Score(beginner, ended, top)
            if not self.Exsit(open, top) and not self.Exsit(close, top):
                top.parent = first
                open.append(top)
                bValid = True
            elif self.Exsit(open, top):
                old_open = self.FindItem(open, top)
                if top.f < old_open.f:
                    old_open.f = top.f
                    old_open.parent = first
            else:
                old_close = self.FindItem(close, top)
                if top.f < old_close.f:
                    old_close.f = top.f
                    old_close.parent = first
                    close.pop(self.FindItemIter(close, top))
                    open.append(top)
        # if not bValid:
        #     # print("4个点都不能走", x, y)
        #     # print("cant find path", map_tool.get_w_map())
        #     # for list in map_tool.get_agv_map():
        #     #     print(list)
        #     # print(map_tool.get_agv_map())
        return bValid


    def Mysort(p0, p1):
        if p0.f < p1.f:
            return -1
        else:
            return 1


    def BestPath(self,beginner, ended, map_tool, _is_loaded: bool, _agv):
        open = []
        close = []
        path = []
        bValidPoint = False
        beginner = self.Cpoint(beginner[0], beginner[1])
        ended = self.Cpoint(ended[0], ended[1])
        open.append(beginner)
        while open:
            open.sort(key=self.cmp_to_key(self.Mysort))
            first = open[0]
            if first == ended:
                node = first
                path.clear()
                # print(node.parent)
                while node.parent is not None:
                    path.append((node.x, node.y))
                    node = node.parent
                path.reverse()  # 得到的路径是反着的 翻转一下
                return path
            close.append(first)
            open.pop(0)
            bValidPoint = self.FindChildren(first, map_tool, first, ended, open, close,
                                    map_tool.get_height(), map_tool.get_width(), _is_loaded, _agv)
        if not bValidPoint:
            return []
        return path.reverse()