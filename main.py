import random
from tkinter.filedialog import asksaveasfilename

import pygame
from litemapy import BlockState, Region

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Minecraft Maze Generator")

COLORS = {
    "TCELL": pygame.Color(30, 30, 30),  # true cell
    "FCELL": pygame.Color(200, 200, 200),  # false cell
    "GRIDLINE": pygame.Color(0, 0, 0),  # the lines on the grid
    "MENUBG": pygame.Color(166, 166, 166),  # menu background
    "BI": pygame.Color(217, 217, 217),  # button inactive
    "BIH": pygame.Color(197, 197, 197),  # button inactive hover
    "BA": pygame.Color(84, 84, 84),  # button active
    "BAH": pygame.Color(64, 64, 64),  # button active
    "BGENI": pygame.Color(99, 189, 146),  # button generation inactive
    "BGENH": pygame.Color(119, 209, 166),  # button generation hover
    "BGENA": pygame.Color(139, 229, 186),  # button generation active
    "TEXT": pygame.Color(0, 0, 0),  # font colour
}

FONTS = {
    "DEFAULT": pygame.font.SysFont("Calibri", 19),
    "HEADER": pygame.font.SysFont("Arial", 30, bold=True),
}


class Grid:
    def __init__(self):
        self.active = True
        self.grid_size = 20
        self.grid_line_width = 1
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.grid_resolution = 720
        self.displayed_cell_size = (
            self.grid_resolution - self.grid_size * self.grid_line_width
        ) / self.grid_size

    def draw_grid(self):
        for row_index in range(self.grid_size):
            for col_index in range(self.grid_size):
                if self.grid[row_index][col_index] is True:
                    cell_colour = COLORS["TCELL"]
                else:
                    cell_colour = COLORS["FCELL"]
                cumulative_x_pos = col_index * self.displayed_cell_size + col_index * self.grid_line_width
                cumulative_y_pos = row_index * self.displayed_cell_size + row_index * self.grid_line_width
                pygame.draw.rect(
                    screen,
                    cell_colour,
                    (
                        cumulative_x_pos,
                        cumulative_y_pos,
                        self.displayed_cell_size,
                        self.displayed_cell_size,
                    ),
                )

    def new_grid(self):
        self.grid_size = canvas_menu.number_input_boxes["GRIDSIZE"].get_user_input()
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.displayed_cell_size = (
            self.grid_resolution - self.grid_size * self.grid_line_width
        ) / self.grid_size


class Canvas(Grid):
    def __init__(self):
        super().__init__()
        self.equipped_tool = "pencil"
        self.hollow_shapes = False

    def process_clicks(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if x < 720 and y < 720:
                canvas.use_equipped()

        if pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            if x < 720 and y < 720:
                canvas.use_eraser(1)

    def mouse_pos_to_grid_index(self):
        x, y = pygame.mouse.get_pos()
        clicked_x_index = int(x / (self.displayed_cell_size + self.grid_line_width))
        clicked_y_index = int(y / (self.displayed_cell_size + self.grid_line_width))
        return clicked_x_index, clicked_y_index

    def draw_on_grid(self, new_state, brush_width):
        x, y = self.mouse_pos_to_grid_index()
        for i in range(-brush_width, brush_width):
            for j in range(-brush_width, brush_width):
                distance = (i ** 2 + j ** 2) ** 0.5
                if (
                    distance < brush_width - 0.5
                    and x + i >= 0
                    and y + j >= 0
                ):
                    try:
                        self.grid[y + j][x + i] = new_state
                    except IndexError:
                        pass

    def use_pencil(self, pencil_width):
        self.draw_on_grid(True, pencil_width)

    def use_eraser(self, eraser_width):
        self.draw_on_grid(False, eraser_width)

    def use_fill(self):
        x, y = self.mouse_pos_to_grid_index()
        valid = not self.grid[y][x]
        node = (y, x)
        if valid:
            stack = [node]
            while stack:
                node = stack[-1]
                stack.pop()

                self.grid[node[0]][node[1]] = True

                if node[0] + 1 < len(self.grid):
                    if self.grid[node[0] + 1][node[1]] is False:
                        stack.append((node[0] + 1, node[1]))

                if node[1] + 1 < len(self.grid):
                    if self.grid[node[0]][node[1] + 1] is False:
                        stack.append((node[0], node[1] + 1))

                if node[0] - 1 >= 0:
                    if self.grid[node[0] - 1][node[1]] is False:
                        stack.append((node[0] - 1, node[1]))

                if node[1] - 1 >= 0:
                    if self.grid[node[0]][node[1] - 1] is False:
                        stack.append((node[0], node[1] - 1))

    def set_hollow(self):
        self.hollow_shapes = not self.hollow_shapes

    def equip_pencil(self):
        self.equipped_tool = "pencil"

    def equip_eraser(self):
        self.equipped_tool = "eraser"

    def equip_fill(self):
        self.equipped_tool = "fill"

    def equip_move(self):
        self.equipped_tool = "move"

    def equip_circle(self):
        self.equipped_tool = "circle"

    def equip_rectangle(self):
        self.equipped_tool = "rectangle"

    def equip_line(self):
        self.equipped_tool = "line"

    def use_equipped(self):
        if self.equipped_tool == "pencil":
            self.use_pencil(canvas_menu.number_input_boxes["PENCILWIDTH"].get_user_input())
        elif self.equipped_tool == "eraser":
            self.use_eraser(canvas_menu.number_input_boxes["PENCILWIDTH"].get_user_input())
        elif self.equipped_tool == "fill":
            self.use_fill()
        elif self.equipped_tool == "move":
            pass
        elif self.equipped_tool == "circle":
            pass
        elif self.equipped_tool == "rectangle":
            pass
        elif self.equipped_tool == "line":
            pass

    def invert_grid(self):
        for row_index in range(canvas.grid_size):
            for col_index in range(canvas.grid_size):
                self.grid[row_index][col_index] = not self.grid[row_index][col_index]


class Maze(Grid):
    def __init__(self):
        super().__init__()
        self.active = False

    def create_maze(self):
        grid = self.scale_up(
            canvas.grid,
            generation_menu.number_input_boxes["SCALE"].get_user_input(),
        )
        grid = self.downsize_canvas(grid)
        grid = self.convert_bool_to_dict(grid)
        starting_index = self.find_starting_value(grid)
        if starting_index:
            maze_layout = self.generate_maze_paths(
                grid,
                generation_menu.number_input_boxes["HORIZONTALBIAS"].get_user_input(),
                generation_menu.number_input_boxes["CURLINESS"].get_user_input(),
                starting_index,
            )
            self.generate_maze_grid(
                maze_layout,
                generation_menu.number_input_boxes["WALLWIDTH"].get_user_input(),
                generation_menu.number_input_boxes["HALLWAYWIDTH"].get_user_input(),
                generation_menu.number_input_boxes["DOORWAYWIDTH"].get_user_input(),
            )
        else:
            print("No maze was drawn!")

    def downsize_canvas(self, grid):
        top_most = len(grid)
        left_most = len(grid[0])
        bottom_most = 0
        right_most = 0

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j]:
                    top_most = min(top_most, i)
                    left_most = min(left_most, j)
                    bottom_most = max(bottom_most, i)
                    right_most = max(right_most, j)

        max_dimension = max(bottom_most - top_most, right_most - left_most)
        square_size = max_dimension + 1

        square_grid = [[False for _ in range(square_size)] for _ in range(square_size)]
        for i in range(top_most, bottom_most + 1):
            for j in range(left_most, right_most + 1):
                square_grid[i - top_most][j - left_most] = grid[i][j]

        return square_grid

    def scale_up(self, grid, scale):
        scaled_grid = []
        for row in grid:
            scaled_row = []
            for cell in row:
                scaled_cell = [cell] * scale
                scaled_row.extend(scaled_cell)
            scaled_grid.extend([scaled_row] * scale)

        return scaled_grid

    def convert_bool_to_dict(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] is True:
                    grid[i][j] = {
                        "visited": False,
                        "blacklisted": False,
                        "north": True,
                        "east": True,
                        "south": True,
                        "west": True,
                    }
                elif grid[i][j] is False:
                    grid[i][j] = {
                        "visited": False,
                        "blacklisted": True,
                        "north": False,
                        "east": False,
                        "south": False,
                        "west": False,
                    }
        return grid

    def find_starting_value(self, grid):
        cells = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if not grid[i][j]["blacklisted"]:
                    cells.append((i, j))
        if cells:
            return random.choice(cells)
        return None

    def next_node_probs(
        self,
        grid,
        grid_size,
        node,
        previous_direction,
        horizontal_weighting,
        curliness,
    ):
        probabilities = [0, 0, 0, 0]

        vertical_weighting = 1 - horizontal_weighting
        i = node[0]
        j = node[1]

        if previous_direction in {"north", "south"}:
            curl_chance = curliness
            inverse_curl_chance = 1 - curliness
        elif previous_direction in {"east", "west"}:
            curl_chance = 1 - curliness
            inverse_curl_chance = curliness
        else:
            curl_chance = 1
            inverse_curl_chance = 1

        if node[0] - 1 >= 0:
            if not grid[i - 1][j]["blacklisted"] and not grid[i - 1][j]["visited"]:
                probabilities[0] = vertical_weighting * inverse_curl_chance
        if node[1] + 1 < grid_size:
            if not grid[i][j + 1]["blacklisted"] and not grid[i][j + 1]["visited"]:
                probabilities[1] = horizontal_weighting * curl_chance
        if node[0] + 1 < grid_size:
            if not grid[i + 1][j]["blacklisted"] and not grid[i + 1][j]["visited"]:
                probabilities[2] = vertical_weighting * inverse_curl_chance
        if node[1] - 1 >= 0:
            if not grid[i][j - 1]["blacklisted"] and not grid[i][j - 1]["visited"]:
                probabilities[3] = horizontal_weighting * curl_chance

        total_probability = sum(probabilities)
        if total_probability > 0:
            probabilities = [prob / total_probability for prob in probabilities]

        return probabilities

    def is_maze_connected(self, grid, visited_count):
        true_cell_count = 0
        for row in grid:
            for cell in row:
                if not cell["blacklisted"]:
                    true_cell_count += 1

        if visited_count < true_cell_count:
            print("Maze wasn't fully connected!")

    def generate_maze_paths(self, grid, horizontal_weighting, curliness, starting_point_index):
        grid_size = len(grid)
        directions = ["north", "east", "south", "west"]
        previous_direction = ""
        visited_count = 0

        stack = [starting_point_index]
        while stack:
            node = stack[-1]
            i = node[0]
            j = node[1]

            grid[i][j]["visited"] = True

            if previous_direction == "north":
                grid[i][j]["south"] = False
            elif previous_direction == "east":
                grid[i][j]["west"] = False
            elif previous_direction == "south":
                grid[i][j]["north"] = False
            elif previous_direction == "west":
                grid[i][j]["east"] = False

            probabilities = self.next_node_probs(
                grid,
                grid_size,
                node,
                previous_direction,
                horizontal_weighting,
                curliness,
            )

            total_probability = sum(probabilities)
            if total_probability > 0:
                new_direction = random.choices(directions, weights=probabilities)[0]
                grid[i][j][new_direction] = False

                if new_direction == "north":
                    stack.append((i - 1, j))
                elif new_direction == "east":
                    stack.append((i, j + 1))
                elif new_direction == "south":
                    stack.append((i + 1, j))
                elif new_direction == "west":
                    stack.append((i, j - 1))

                previous_direction = new_direction
            else:
                visited_count += 1
                previous_direction = ""
                stack.pop()

        self.is_maze_connected(grid, visited_count)

        return grid

    def generate_maze_grid(self, maze_layout_grid, wall_width, hallway_width, doorway_width):
        solid_wall = "1" * ((hallway_width - doorway_width) // 2)
        doorway_pattern = solid_wall + ("0" * doorway_width) + solid_wall
        doorway_pattern = ("1" * wall_width) + doorway_pattern + ("1" * wall_width)

        wall_length = len(doorway_pattern)
        segment = wall_length - wall_width
        grid_size = (wall_length - wall_width) * len(maze_layout_grid) + wall_width

        self.grid_size = grid_size
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.displayed_cell_size = (
            self.grid_resolution - (self.grid_size - 1) * self.grid_line_width
        ) / self.grid_size

        for i in range(len(maze_layout_grid)):
            for j in range(len(maze_layout_grid)):
                cell = maze_layout_grid[i][j]
                if not cell["blacklisted"]:
                    if cell["north"]:
                        for y in range(wall_width):
                            for x in range(wall_length):
                                self.grid[y + i * segment][x + j * segment] = True
                    else:
                        for y in range(wall_width):
                            for x in range(wall_length):
                                if doorway_pattern[x] == "1":
                                    self.grid[y + i * segment][x + j * segment] = True

                    if cell["east"]:
                        for x in range(wall_width):
                            for y in range(wall_length):
                                self.grid[y + i * segment][x + j * segment + segment] = True
                    else:
                        for x in range(wall_width):
                            for y in range(wall_length):
                                if doorway_pattern[y] == "1":
                                    self.grid[y + i * segment][x + j * segment + segment] = True

                    if cell["south"]:
                        for y in range(wall_width):
                            for x in range(wall_length):
                                self.grid[y + i * segment + segment][x + j * segment] = True
                    else:
                        for y in range(wall_width):
                            for x in range(wall_length):
                                if doorway_pattern[x] == "1":
                                    self.grid[y + i * segment + segment][x + j * segment] = True

                    if cell["west"]:
                        for x in range(wall_width):
                            for y in range(wall_length):
                                self.grid[y + i * segment][x + j * segment] = True
                    else:
                        for x in range(wall_width):
                            for y in range(wall_length):
                                if doorway_pattern[y] == "1":
                                    self.grid[y + i * segment][x + j * segment] = True

    def shrink_grid(self, grid):
        min_row = len(grid)
        max_row = -1
        min_col = len(grid[0])
        max_col = -1

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j]:
                    min_row = min(min_row, i)
                    max_row = max(max_row, i)
                    min_col = min(min_col, j)
                    max_col = max(max_col, j)

        return [row[min_col : max_col + 1] for row in grid[min_row : max_row + 1]]

    def generate_litematic_file(self, grid, height, block_id):
        if grid:
            grid_size_z = len(grid)
            grid_size_x = len(grid[0])
            reg = Region(0, 0, 0, grid_size_z, height, grid_size_x)
            schem = reg.as_schematic(name="Maze", description="Made with Litemapy and Litematica Maze Gen")

            block = BlockState(block_id)

            for x in range(len(grid)):
                for z in range(len(grid[x])):
                    for y in range(height):
                        if grid[x][-z - 1]:
                            reg.setblock(x, y, z, block)

            filename = asksaveasfilename(
                defaultextension=".litematic",
                filetypes=[("Litematic files", "*.litematic"), ("All files", "*.*")],
            )

            if filename:
                try:
                    schem.save(filename)
                    print("File saved successfully as", filename)
                except Exception as exc:
                    print("Error saving file:", exc)
            else:
                print("Save operation cancelled")
        else:
            print("Maze has not been generated yet")

    def create_litematic(self):
        grid = self.grid
        grid = self.shrink_grid(grid)
        self.generate_litematic_file(
            grid,
            generation_menu.number_input_boxes["WALLHEIGHT"].get_user_input(),
            generation_menu.text_input_boxes["BLOCKID"].get_user_input(),
        )

    def generate_mcfunction_file(self, grid, height, block_id):
        if grid:
            grid_size_x = len(grid)
            grid_size_z = len(grid[0])

            data = "# Clear maze blocks\n"
            data += f"fill ~ ~ ~ ~{grid_size_x - 1} ~{height - 1} ~{-grid_size_z + 1} minecraft:air\n"
            data += "# Fill maze blocks\n"
            for x in range(len(grid)):
                for z in range(len(grid[x])):
                    if grid[x][z]:
                        data += f"fill ~{x} ~ ~{-z} ~{x} ~{height - 1} ~{-z} {block_id}\n"

            filename = asksaveasfilename(
                defaultextension=".mcfunction",
                filetypes=[("mcfunction files", "*.mcfunction"), ("All files", "*.*")],
            )

            if filename:
                try:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(data)
                    print("Data saved to", filename)
                except Exception as exc:
                    print("Error saving file:", exc)
            else:
                print("Save operation cancelled")
        else:
            print("Maze has not been generated yet")

    def create_mcfunction(self):
        grid = self.grid
        grid = self.shrink_grid(grid)
        self.generate_mcfunction_file(
            grid,
            generation_menu.number_input_boxes["WALLHEIGHT"].get_user_input(),
            generation_menu.text_input_boxes["BLOCKID"].get_user_input(),
        )


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        inactive_colour,
        hover_colour,
        active_colour,
        active_hover_colour,
        callback,
        text,
        default_value=False,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_colour = inactive_colour
        self.hover_colour = hover_colour
        self.active_colour = active_colour
        self.active_hover_colour = active_hover_colour
        self.callback = callback
        self.font = FONTS["DEFAULT"]
        self.font_colour = COLORS["TEXT"]
        self.text = text
        self.state = default_value

        self.mouse_pos_state = "invalid"
        self.current_colour = inactive_colour
        self.previously_clicked = False

    def draw_element(self):
        pygame.draw.rect(screen, self.current_colour, self.rect)

        text_surface = self.font.render(self.text, True, self.font_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def set_mouse_pos_state(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.mouse_pos_state = "click"
        elif self.rect.collidepoint(pos):
            self.mouse_pos_state = "hover"
        else:
            self.mouse_pos_state = "invalid"

    def set_colour(self):
        if self.state is True and self.mouse_pos_state == "hover":
            self.current_colour = self.active_hover_colour
        elif self.state is True:
            self.current_colour = self.active_colour
        elif self.mouse_pos_state == "hover":
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.inactive_colour

    def process(self):
        if self.mouse_pos_state == "click" and self.previously_clicked is False:
            self.state = True
            self.previously_clicked = True
            self.callback()
        elif self.mouse_pos_state != "click":
            self.state = False
            self.previously_clicked = False

    def update(self):
        self.set_mouse_pos_state()
        self.set_colour()
        self.process()


class ToggleButton(Button):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        inactive_colour,
        hover_colour,
        active_colour,
        active_hover_colour,
        callback,
        text,
        default_value=False,
    ):
        super().__init__(
            x,
            y,
            width,
            height,
            inactive_colour,
            hover_colour,
            active_colour,
            active_hover_colour,
            callback,
            text,
            default_value,
        )

    def process(self):
        if self.mouse_pos_state == "click" and self.previously_clicked is False:
            self.state = not self.state
            self.previously_clicked = True
            self.callback()
        elif self.mouse_pos_state != "click":
            self.previously_clicked = False


class GroupToggleButton(Button):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        inactive_colour,
        hover_colour,
        active_colour,
        active_hover_colour,
        callback,
        text,
        group,
        default_value=False,
    ):
        super().__init__(
            x,
            y,
            width,
            height,
            inactive_colour,
            hover_colour,
            active_colour,
            active_hover_colour,
            callback,
            text,
            default_value,
        )
        self.group = group

    def process(self, group_toggle_buttons):
        if self.mouse_pos_state == "click" and self.previously_clicked is False:
            for key in group_toggle_buttons:
                if group_toggle_buttons[key].group == self.group:
                    group_toggle_buttons[key].state = False
            self.state = True
            self.previously_clicked = True
            self.callback()
        elif self.mouse_pos_state != "click":
            self.previously_clicked = False

    def update(self, group_toggle_buttons):
        self.set_mouse_pos_state()
        self.set_colour()
        self.process(group_toggle_buttons)


class TextBox:
    def __init__(self, x, y, width, height, box_colour, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.box_colour = box_colour
        self.font = FONTS["HEADER"]
        self.text = text

    def draw_element(self):
        pygame.draw.rect(screen, self.box_colour, self.rect)

        text_to_render = self.text
        text_surface = self.font.render(text_to_render, True, COLORS["TEXT"])

        text_rect = text_surface.get_rect()
        text_rect.left = self.rect.left
        text_rect.centery = self.rect.centery

        screen.blit(text_surface, text_rect)


class TextInputBox:
    def __init__(self, x, y, width, height, inactive_colour, hover_colour, active_colour, text, char_limit, default_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_colour = inactive_colour
        self.hover_colour = hover_colour
        self.active_colour = active_colour
        self.font = FONTS["DEFAULT"]
        self.text = text
        self.text_padding = 5
        self.char_limit = char_limit + len(self.text)

        self.mouse_pos_state = "invalid"
        self.current_colour = inactive_colour
        self.state = False
        self.user_text = default_value

    def get_user_input(self):
        return str(self.user_text)

    def draw_element(self):
        pygame.draw.rect(screen, self.current_colour, self.rect)

        text_to_render = self.text + self.user_text
        text_surface = self.font.render(text_to_render, True, COLORS["TEXT"])

        text_rect = text_surface.get_rect()
        text_rect.left = self.rect.left + self.text_padding
        text_rect.centery = self.rect.centery

        screen.blit(text_surface, text_rect)

    def set_mouse_pos_state(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.mouse_pos_state = "click"
        elif not self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.mouse_pos_state = "clickOff"
        elif self.rect.collidepoint(pos):
            self.mouse_pos_state = "hover"
        else:
            self.mouse_pos_state = "invalid"

    def set_colour(self):
        if self.state is True:
            self.current_colour = self.active_colour
        elif self.mouse_pos_state == "hover":
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.inactive_colour

    def text_input(self, events):
        for event in events:
            if self.state is True and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    if event.unicode.isalnum() and len(self.text + self.user_text) < self.char_limit:
                        self.user_text += event.unicode
                    elif event.unicode in {":", "_"}:
                        self.user_text += event.unicode

    def process(self):
        if self.mouse_pos_state == "click":
            self.state = True
        elif self.mouse_pos_state == "clickOff":
            self.state = False

    def update(self, events):
        self.set_mouse_pos_state()
        self.set_colour()
        self.text_input(events)
        self.process()


class NumberInputBox(TextInputBox):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        inactive_colour,
        hover_colour,
        active_colour,
        text,
        char_limit,
        default_value,
        decimal,
    ):
        super().__init__(
            x,
            y,
            width,
            height,
            inactive_colour,
            hover_colour,
            active_colour,
            text,
            char_limit,
            default_value,
        )
        self.decimal = decimal
        if self.decimal:
            self.text = text + "0."
            self.char_limit = len(self.text) + char_limit

    def get_user_input(self):
        if self.decimal:
            if self.user_text != "" and int(self.user_text) != 0:
                return float("0." + self.user_text)
            return 0.5

        if self.user_text != "":
            return int(self.user_text)
        return 1

    def text_input(self, events):
        for event in events:
            if self.state is True and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    if self.decimal is True:
                        if event.unicode.isnumeric() and len(self.text + self.user_text) < self.char_limit:
                            self.user_text += event.unicode
                    else:
                        if event.unicode.isnumeric() and len(self.text + self.user_text) < self.char_limit:
                            if event.unicode != "0" and len(self.user_text) == 0:
                                self.user_text += event.unicode
                            elif len(self.user_text) > 0:
                                self.user_text += event.unicode


class Menu:
    def __init__(
        self,
        active=False,
        buttons=None,
        toggle_buttons=None,
        group_toggle_buttons=None,
        text_input_boxes=None,
        number_input_boxes=None,
        text_boxes=None,
    ):
        self.active = active
        self.buttons = buttons or {}
        self.toggle_buttons = toggle_buttons or {}
        self.group_toggle_buttons = group_toggle_buttons or {}
        self.text_input_boxes = text_input_boxes or {}
        self.number_input_boxes = number_input_boxes or {}
        self.text_boxes = text_boxes or {}
        self.width = 560
        self.height = 720

    def draw_menu(self):
        pygame.draw.rect(screen, COLORS["MENUBG"], (720, 0, self.width, self.height))
        for key in self.buttons:
            self.buttons[key].draw_element()
        for key in self.toggle_buttons:
            self.toggle_buttons[key].draw_element()
        for key in self.group_toggle_buttons:
            self.group_toggle_buttons[key].draw_element()
        for key in self.text_input_boxes:
            self.text_input_boxes[key].draw_element()
        for key in self.number_input_boxes:
            self.number_input_boxes[key].draw_element()
        for key in self.text_boxes:
            self.text_boxes[key].draw_element()

    def update(self, events):
        for key in self.buttons:
            self.buttons[key].update()
        for key in self.toggle_buttons:
            self.toggle_buttons[key].update()
        for key in self.group_toggle_buttons:
            self.group_toggle_buttons[key].update(self.group_toggle_buttons)
        for key in self.text_input_boxes:
            self.text_input_boxes[key].update(events)
        for key in self.number_input_boxes:
            self.number_input_boxes[key].update(events)


def get_active_menu():
    if canvas_menu.active:
        return canvas_menu
    if generation_menu.active:
        return generation_menu
    return canvas_menu


def get_active_grid():
    if canvas.active:
        return canvas
    if maze.active:
        return maze
    return canvas


def switch_menu():
    canvas_menu.active = not canvas_menu.active
    generation_menu.active = not generation_menu.active


def switch_grid():
    canvas.active = not canvas.active
    maze.active = not maze.active


def switch_screen():
    switch_menu()
    switch_grid()


def display_all():
    screen.fill(COLORS["GRIDLINE"])
    get_active_grid().draw_grid()
    get_active_menu().draw_menu()

    pygame.display.flip()


canvas = Canvas()
maze = Maze()

canvas_menu = Menu(
    active=True,
    buttons={
        "NEWGRID": Button(732, 379, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.new_grid, "New grid"),
        "INVERT": Button(869, 379, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.invert_grid, "Invert cells"),
        "GENMAZE": Button(732, 516, 125, 125, COLORS["BGENI"], COLORS["BGENH"], COLORS["BGENA"], COLORS["BAH"], switch_screen, "Generate maze"),
    },
    toggle_buttons={
        "HOLLOW": ToggleButton(1097.33, 58, 170.67, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.set_hollow, "Hollow shapes"),
    },
    group_toggle_buttons={
        "PENCIL": GroupToggleButton(732, 105, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_pencil, "Pencil", 1, True),
        "ERASER": GroupToggleButton(869, 105, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_eraser, "Eraser", 1),
        "FILL": GroupToggleButton(1006, 105, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_fill, "Fill", 1),
        "MOVE": GroupToggleButton(1143, 105, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_move, "Move", 1),
        "CIRCLE": GroupToggleButton(732, 242, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_circle, "Circle", 1),
        "RECTANGLE": GroupToggleButton(869, 242, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_rectangle, "Rectangle", 1),
        "LINES": GroupToggleButton(1006, 242, 125, 125, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], canvas.equip_line, "Line", 1),
    },
    number_input_boxes={
        "GRIDSIZE": NumberInputBox(732, 58, 170.67, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Grid size: ", 3, "20", False),
        "PENCILWIDTH": NumberInputBox(914.67, 58, 170.67, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Pencil Width: ", 3, "1", False),
    },
    text_boxes={
        "HEADER": TextBox(733, 30, 1, 1, COLORS["MENUBG"], "Draw maze layout"),
    },
)

generation_menu = Menu(
    active=False,
    buttons={
        "BACK": Button(732, 434, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], switch_screen, "Go back"),
        "GENMAZE": Button(732, 481, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], COLORS["BAH"], maze.create_maze, "Generate maze"),
        "GENLITEMATIC": Button(732, 528, 536, 35, COLORS["BGENI"], COLORS["BGENH"], COLORS["BGENA"], COLORS["BAH"], maze.create_litematic, "Generate LITEMATIC file"),
        "GENMCFUNCTION": Button(732, 575, 536, 35, COLORS["BGENI"], COLORS["BGENH"], COLORS["BGENA"], COLORS["BAH"], maze.create_mcfunction, "Generate MCFUNCTION file"),
    },
    text_input_boxes={
        "BLOCKID": TextInputBox(732, 58, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Block ID: ", 100, "minecraft:cobblestone"),
    },
    number_input_boxes={
        "SCALE": NumberInputBox(732, 105, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Scale: ", 3, "1", False),
        "WALLHEIGHT": NumberInputBox(732, 152, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Wall height: ", 3, "1", False),
        "WALLWIDTH": NumberInputBox(732, 199, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Wall width: ", 3, "1", False),
        "HALLWAYWIDTH": NumberInputBox(732, 246, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Hallway width: ", 3, "1", False),
        "DOORWAYWIDTH": NumberInputBox(732, 293, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Doorway width: ", 3, "1", False),
        "HORIZONTALBIAS": NumberInputBox(732, 340, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Horizontal bias: ", 5, "5", True),
        "CURLINESS": NumberInputBox(732, 387, 536, 35, COLORS["BI"], COLORS["BIH"], COLORS["BA"], "Curliness: ", 5, "5", True),
    },
    text_boxes={
        "HEADER": TextBox(733, 30, 1, 1, COLORS["MENUBG"], "Maze settings"),
    },
)


def main():
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        if canvas.active:
            canvas.process_clicks()

        get_active_menu().update(events)
        display_all()

    pygame.quit()


if __name__ == "__main__":
    main()