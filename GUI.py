import sys
import pygame
from MapTools import *


class GUI:
    map_tools: MapTools = None

    background_color = (255, 239, 213)  # 背景颜色
    dividing_line_color = (255, 222, 173)  # 分割线颜色
    entrance_color = (255, 215, 0)
    exit_color = (238, 201, 0)
    parking_color = (242, 177, 121)
    font_color = (51, 51, 255)

    # button color
    red = (200, 0, 0)
    green = (0, 200, 0)
    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)
    blue = (65, 105, 225)
    bright_blue = (0, 0, 255)

    # button pos
    red_pos = None
    green_pos = None
    blue_pos = None

    screen = None
    img_agv = None
    img_car = None
    img_font = None  # 字体类

    screen_height = 0
    screen_weight = 0
    time_screen = 50

    img_time = None
    img_time_pos = None
    time_screen_height = 50
    time_font = None
    button_pos = None

    def __init__(self, _map_tools):
        self.map_tools = _map_tools
        self.screen_weight = _map_tools.get_map_size()[0] * (
                _map_tools.get_map_size()[2] + _map_tools.get_map_size()[3])
        self.screen_height = _map_tools.get_map_size()[1] * (
                _map_tools.get_map_size()[2] + _map_tools.get_map_size()[3])
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_weight, self.screen_height + self.time_screen_height))
        pygame.display.set_caption('parking lot')
        self.img_font = pygame.font.Font('png/font.ttf', _map_tools.get_map_size()[4])
        self.time_font = pygame.font.Font('png/font.ttf', 20)
        self.img_time_pos = (0, self.screen_height + 10)
        self.button_pos = (335, self.screen_height + 5)
        pygame.display.flip()
        self.img_agv = pygame.transform.scale(pygame.image.load("png/AGV.png"),
                                              (_map_tools.get_map_size()[2], _map_tools.get_map_size()[2]))
        self.img_car = pygame.transform.scale(pygame.image.load("png/CAR.png"),
                                              (_map_tools.get_map_size()[2], _map_tools.get_map_size()[2]))

    def draw_background(self, _map_tools):
        self.screen.fill(self.background_color)
        for i in range(0, _map_tools.get_map_size()[0] + 1):
            pygame.draw.line(self.screen, self.dividing_line_color,
                             ((_map_tools.get_map_size()[2] + _map_tools.get_map_size()[3]) * i, 0),
                             ((_map_tools.get_map_size()[2] + _map_tools.get_map_size()[3]) * i,
                              self.screen_height), _map_tools.get_map_size()[3])
        for j in range(0, _map_tools.get_map_size()[1] + 1):
            pygame.draw.line(self.screen, self.dividing_line_color,
                             (0, (_map_tools.get_map_size()[2] + _map_tools.get_map_size()[3]) * j),
                             (self.screen_weight, (_map_tools.get_map_size()[2] +
                                                   _map_tools.get_map_size()[3]) * j),
                             _map_tools.get_map_size()[3])
        for i in range(0, _map_tools.get_map_size()[1]):
            for j in range(0, _map_tools.get_map_size()[0]):
                if _map_tools.get_basic_map()[i][j] == _map_tools.ENTRY_BUFFER:
                    rect_color = self.entrance_color
                elif _map_tools.get_basic_map()[i][j] == _map_tools.EXIT:
                    rect_color = self.exit_color
                elif _map_tools.get_basic_map()[i][j] == _map_tools.PARKING_LOT:
                    rect_color = self.parking_color
                else:
                    rect_color = self.background_color
                rect_position = [(j + 1) * self.map_tools.DIVIDING_LINE_WIDTH + j * self.map_tools.square_size,  # 色块的位置
                                 self.map_tools.DIVIDING_LINE_WIDTH * (i + 1) + self.map_tools.square_size * i]
                pygame.draw.rect(self.screen, rect_color, (rect_position, (self.map_tools.square_size,
                                                                           self.map_tools.square_size)), 0)  # 绘制色块
        # draw button
        self.red_pos = [12 * self.map_tools.DIVIDING_LINE_WIDTH + 11 * self.map_tools.square_size,  # 色块的位置
                        self.map_tools.DIVIDING_LINE_WIDTH * 1 + self.map_tools.square_size * 0]
        self.green_pos = [12 * self.map_tools.DIVIDING_LINE_WIDTH + 11 * self.map_tools.square_size,  # 色块的位置
                          self.map_tools.DIVIDING_LINE_WIDTH * 2 + self.map_tools.square_size * 1]
        self.blue_pos = [12 * self.map_tools.DIVIDING_LINE_WIDTH + 11 * self.map_tools.square_size,  # 色块的位置
                         self.map_tools.DIVIDING_LINE_WIDTH * 3 + self.map_tools.square_size * 2]

        pygame.draw.rect(self.screen, self.red, (self.red_pos, (self.map_tools.square_size,
                                                                self.map_tools.square_size)), 0)  # 绘制色块
        pygame.draw.rect(self.screen, self.green, (self.green_pos, (self.map_tools.square_size,
                                                                    self.map_tools.square_size)), 0)  # 绘制色块
        pygame.draw.rect(self.screen, self.blue, (self.blue_pos, (self.map_tools.square_size,
                                                                  self.map_tools.square_size)), 0)  # 绘制色块

    def gui_run(self, _car, _agv, _map_tools):
        for each_car in _car:
            each_car.update_img(self.img_car, _map_tools.get_map_size()[2] + _map_tools.get_map_size()[3], self.img_font
                                , self.font_color)
        for each_agv in _agv:
            each_agv.update_img(self.img_agv, _map_tools.get_map_size()[2] + _map_tools.get_map_size()[3], self.img_font
                                , self.font_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        self.draw_background(_map_tools)
        for i in range(0, len(_agv)):
            _agv[i].update_pos()
            _agv[i].display(self.screen, _map_tools)
        for i in range(0, len(_car)):
            if _car[i].car_state == 1 and _car[i].get_current_pos() is not None:
                _car[i].update_pos()
                _car[i].display(self.screen, _map_tools)

    def mouse_bright_display(self):
        mouse = pygame.mouse.get_pos()
        if self.red_pos[0] + self.map_tools.get_map_size()[2] > mouse[0] > self.red_pos[0] and self.red_pos[1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.red_pos[1]:
            pygame.draw.rect(self.screen, self.bright_red, (self.red_pos, (self.map_tools.square_size,
                                                                           self.map_tools.square_size)), 0)
        else:
            pygame.draw.rect(self.screen, self.red, (self.red_pos, (self.map_tools.square_size,
                                                                    self.map_tools.square_size)), 0)
        if self.green_pos[0] + self.map_tools.get_map_size()[2] > mouse[0] > self.green_pos[0] and self.green_pos[1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.green_pos[1]:
            pygame.draw.rect(self.screen, self.bright_green, (self.green_pos, (self.map_tools.square_size,
                                                                               self.map_tools.square_size)), 0)
        else:
            pygame.draw.rect(self.screen, self.green, (self.green_pos, (self.map_tools.square_size,
                                                                        self.map_tools.square_size)), 0)
        if self.blue_pos[0] + self.map_tools.get_map_size()[2] > mouse[0] > self.blue_pos[0] and self.blue_pos[1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.blue_pos[1]:
            pygame.draw.rect(self.screen, self.bright_blue, (self.blue_pos, (self.map_tools.square_size,
                                                                             self.map_tools.square_size)), 0)
        else:
            pygame.draw.rect(self.screen, self.blue, (self.blue_pos, (self.map_tools.square_size,
                                                                      self.map_tools.square_size)), 0)

    def click_button(self):
        mouse = pygame.mouse.get_pos()
        if self.red_pos[0] + self.map_tools.get_map_size()[2] > mouse[0] > self.red_pos[0] and self.red_pos[1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.red_pos[1]:
            return 1
        elif self.green_pos[0] + self.map_tools.get_map_size()[2] > mouse[0] > self.green_pos[0] and self.green_pos[1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.green_pos[1]:
            return 2
        elif self.blue_pos[0] + self.map_tools.get_map_size()[2] > mouse[0] > self.blue_pos[0] and self.blue_pos[1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.blue_pos[1]:
            return 3
        elif self.button_pos[0] + 2 * self.map_tools.get_map_size()[2] > mouse[0] > self.button_pos[0] and \
                self.button_pos[
                    1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.button_pos[1]:
            return 4
        else:
            return 0

    def time_display(self, time):
        self.img_time = self.time_font.render("time:" + str(time), True, (0, 0, 0))
        self.screen.blit(self.img_time, self.img_time_pos)


    def button_set_time(self):
        mouse = pygame.mouse.get_pos()
        white = (250, 255, 240)
        bright_white = (163, 148, 128)
        set_time_font = pygame.font.Font('png/font.ttf', 20)
        set_time_font = set_time_font.render("set time:"+str(self.map_tools.time_str), True, (0, 0, 0))
        font_pos = (335, self.screen_height + 10)
        pygame.draw.rect(self.screen, white, (self.button_pos, (2 * self.map_tools.square_size,
                                                                self.map_tools.square_size)), 0)
        if self.button_pos[0] + 2 * self.map_tools.get_map_size()[2] > mouse[0] > self.button_pos[0] and \
                self.button_pos[
                    1] + \
                self.map_tools.get_map_size()[2] > mouse[1] > self.button_pos[1]:
            pygame.draw.rect(self.screen, bright_white, (self.button_pos, (2 * self.map_tools.square_size,
                                                                           self.map_tools.square_size)), 0)
        else:
            pygame.draw.rect(self.screen, white, (self.button_pos, (2 * self.map_tools.square_size,
                                                                    self.map_tools.square_size)), 0)
        self.screen.blit(set_time_font, font_pos)

    def mode_display(self):
        mode_font = pygame.font.Font('png/font.ttf', 20)
        mode_img = mode_font.render("mode:"+str(self.map_tools.mode), True, (0, 0, 0))
        self.screen.blit(mode_img, (580, self.screen_height + 10))

    def input_time(self):
        print("-------------------输入模式")
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         exit()
        #     elif event.type == pygame.KEYDOWN:
        #
        #         # 获取所有键盘按钮的状态
        num = pygame.key.get_pressed()

        for i in range(len(num)):
            if num[i] > 0:
                print(i)
                self.map_tools.set_time(i)

        # 对键盘的一些操作比如空格是32按下空格关闭程序
        if num[13]:
            self.map_tools.mode = 4
