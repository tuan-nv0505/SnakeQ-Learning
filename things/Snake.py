import numpy as np

from utils.config import WIDTH, HEIGHT, CELL_SIZE, Direction


class Snake:

    def __init__(self):
        x_head, y_head = WIDTH / 2, HEIGHT / 2
        self.body = np.array([
            [x_head, y_head],
            [x_head - CELL_SIZE, y_head],
            [x_head - CELL_SIZE * 2, y_head]
        ]).astype(np.int32)
        self.direction = Direction(np.random.randint(0, 3))

    def get_state(self, food):
        head = self.get_head()
        next_positions = self.get_next_pos(head)

        check_danger = lambda function_check, direction_int: int(
            function_check(
                next_positions[(self.direction.value + direction_int + len(Direction)) % len(Direction)]
            )
        )

        direction_food = (
            int(food.get_pos()[1] < head[1]),
            int(food.get_pos()[0] > head[0]),
            int(food.get_pos()[1] > head[1]),
            int(food.get_pos()[0] < head[0])
        )

        return (
            check_danger(self.is_collision_wall, 0), # 0 1
            check_danger(self.is_collision_wall, -1), # 0 1
            check_danger(self.is_collision_wall, 1), # 0 1
            check_danger(self.is_collision_body, -1), # 0 1
            check_danger(self.is_collision_body, 1), # 0 1
            check_danger(self.is_collision_body, 0), # 0 1
            *direction_food, # 0 1 2 3 4
            self.direction.value # 0 1 2 3 4
        )

    def move(self, food):
        # print(self.body)
        new_head = self.direction.get_straight_pos(self.get_head())
        self.body = np.insert(self.body, 0, new_head, axis=0)
        ate = False
        if self.is_eat(food):
            food.reset_position(self)
            ate = True
        else:
            self.body = np.delete(self.body, -1, axis=0)
        return ate
        # print(self.body)

    def is_collision_wall(self, head):
        return not (0 <= head[0] <= WIDTH - CELL_SIZE and 0 <= head[1] <= HEIGHT - CELL_SIZE)

    def is_collision_body(self, head):
        return np.any([np.all(head== element) for element in self.body[1:]])

    def is_alive(self):
        # print("body: {} | wall: {} | alive: {}".format(self.is_collision_body(self.get_head()), self.is_collision_wall(self.get_head()), not (self.is_collision_body(self.get_head()) or self.is_collision_wall(self.get_head()))))
        # return not (self.is_collision_body(self.get_next_pos(self.get_head())[self.direction.value]) or self.is_collision_wall(
        #     self.get_next_pos(self.get_head())[self.direction.value]))
        return not (self.is_collision_body(self.get_head()) or self.is_collision_wall(self.get_head()))

    def is_eat(self, food):
        return np.array_equal(self.get_head(), food.get_pos())

    def update_direction(self, action):
        # print(self.direction)
        self.direction = Direction((self.direction.value + int(action) + len(Direction)) % len(Direction))

    def get_head(self):
        return np.copy(self.body[0])

    def get_next_pos(self, pos):
        head = np.copy(pos)
        return np.array([
            head + [0, -CELL_SIZE],
            head + [CELL_SIZE, 0],
            head + [0, CELL_SIZE],
            head + [-CELL_SIZE, 0]
        ])