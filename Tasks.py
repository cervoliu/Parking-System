import Car


class Tasks:
    # basic Attributes
    type = None  # 0 move   1 park   2 retrieve
    car = None  # car class

    # Coordinate
    st = (None, None)
    en = (None, None)

    # for retrieve
    master_car = None

    is_scheduled = False

    def __init__(self, _type: int = None, _car=None, _st=(None, None), _en=(None, None), _master_car=None) -> None:
        self.type = _type
        self.car = _car

        self.st = _st
        self.en = _en

        self.master_car=_master_car

    def get_type(self):
        return self.type

    def get_car(self) -> Car:
        return self.car

    def get_master_car(self):
        return self.master_car

    def get_st_pos(self):
        return self.st

    def get_en_pos(self):
        return self.en

    def task_is_scheduled(self):
        self.is_scheduled = True

    def get_task_schedule(self):
        return self.is_scheduled

    def reinit_task(self, _type: int = None, _car=None, _st=(None, None), _en=(None, None)) -> None:
        self.type = _type
        self.car = _car
        self.st = _st
        self.en = _en
