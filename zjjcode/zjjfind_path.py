class Find_Path:
    def __init__(self, sensor_data):
        import math
        self.now_map = [[0 for j in range(8)] for i in range(16)]
        data_num = len(sensor_data)
        if data_num <= 20:
            self.wrong_laser = True
            return
        else:
            self.wrong_laser = False
        per_degree = math.pi / data_num
        for i in range(data_num):
            x = 7.5 + sensor_data[i] / 10.0 * math.cos(per_degree * i)
            y = sensor_data[i] / 10.0 * math.sin(per_degree * i)
            self.now_map[int(x)][int(y)] += 1

    def get_ans(self):
        import math
        go_straight_speed = 0.4
        turn_front_speed = 0.2
        turn_base_speed = 2.0
        point_limit = 5
        if self.wrong_laser:
            return turn_front_speed, 0.0
        for i in range(2, 8):
            for j in range(5):
                if self.now_map[7-j][i] >= point_limit:
                    angle_speed = turn_base_speed * ( 2 - j / math.sqrt(j**2+i**2) ) / 2.0
                    return turn_front_speed, -angle_speed
                elif self.now_map[8+j][i] >= point_limit:
                    angle_speed = turn_base_speed * ( 2 - j / math.sqrt(j**2+i**2) ) / 2.0
                    return turn_front_speed, angle_speed
        '''angle_speed = 0.0
        near_limit = 40
        for i in range(near_limit):
            for j in range(10):
                if self.now_map[79-i][j] >= point_limit:
                    angle_speed -= turn_base_speed
                if self.now_map[80+i][j] >= point_limit:
                    angle_speed += turn_base_speed
                if angle_speed != 0:
                    return go_straight_speed, angle_speed
        '''
        angle_speed = 0.0
        
        #if (self.now_map[0][0] >= point_limit or self.now_map[0][1] >= point_limit) and (self.now_map[15][0] <= 1 and self.now_map[15][1] <= 1):
        #    angle_speed = -0.05
        #if (self.now_map[15][0] >= point_limit or self.now_map[15][1] >= point_limit) and (self.now_map[0][0] <= 1 or self.now_map[0][1] <= 1):
        #    angle_speed = -0.05
        return go_straight_speed, angle_speed