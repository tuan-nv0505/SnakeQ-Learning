import numpy as np

from utils.config import WIDTH, HEIGHT, CELL_SIZE, Direction


class Snake:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if Snake.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

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
        next_positions = np.array([
            head + [0, -CELL_SIZE],
            head + [CELL_SIZE, 0],
            head + [0, CELL_SIZE],
            head + [-CELL_SIZE, 0]
        ])

        check_danger = lambda function_check, direction_int: int(
            function_check(
                next_positions[(self.direction.value + direction_int + len(Direction)) % len(Direction)]
            )
        )

        direction_food = "{}{}{}{}".format(
            int(food.position[1] < head[1]),
            int(food.position[0] > head[0]),
            int(food.position[1] > head[1]),
            int(food.position[0] < head[0])
        )

        return "{}{}{}{}{}{}{}{}".format(
            check_danger(self.is_collision_wall, 0),
            check_danger(self.is_collision_wall, -1),
            check_danger(self.is_collision_wall, 1),
            check_danger(self.is_collision_body, 0),
            check_danger(self.is_collision_body, -1),
            check_danger(self.is_collision_body, 1),
            direction_food,
            self.direction.value
        )

    def move(self, food):
        new_head = self.direction.go_straight(self.body[0])
        self.body = np.insert(self.body, 0, new_head, axis=0)
        if self.is_eat(food):
            food.reset_position(self)
        else:
            self.body = np.delete(self.body, -1, axis=0)

    def is_collision_wall(self, head):
        return not (0 <= head[0] <= WIDTH - CELL_SIZE and 0 <= head[1] <= HEIGHT - CELL_SIZE)

    def is_collision_body(self, head):
        return np.any([np.all(head == element) for element in self.body[1:]])

    def is_eat(self, food):
        return np.array_equal(self.get_pos_head(), food.position)

    def update_direction(self, action):
        self.direction = Direction[(self.direction.value + action + len(Direction)) % len(Direction)]

    def is_alive(self):
        return not (self.is_collision_body(self.get_head()) or self.is_collision_wall(self.get_head()))

    def get_pos_head(self):
        return self.body[0]

    def get_head(self):
        return self.body[0]
