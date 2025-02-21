# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

game_end = False

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "YaredSnake",  # TODO: Your Battlesnake Username
        "color": "#F6A1F7",  # TODO: Choose color
        "head": "fang",  # TODO: Choose head
        "tail": "nr-booster",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    game_end = False
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    game_end = True
    print("GAME OVER\n")

def game_ended(game_state: typing.Dict):
    return game_end

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["y"] == 0:
        is_move_safe["down"] = False
        print("Not down!")
    elif my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
        print("Not up!")
    
    if my_head["x"] == 0:
        is_move_safe["left"] = False
        print("Not left!")
    elif my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
        print("Not right!")

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    for c in my_body:
        if c["x"] == my_head["x"] + 1 and c["y"] == my_head["y"] and not c == my_body[-1]:
            is_move_safe["right"] = False
        if c["x"] == my_head["x"] - 1 and c["y"] == my_head["y"] and not c == my_body[-1]:
            is_move_safe["left"] = False
        if c["x"] == my_head["x"] and c["y"] == my_head["y"] + 1 and not c == my_body[-1]:
            is_move_safe["up"] = False
        if c["x"] == my_head["x"] and c["y"] == my_head["y"] - 1 and not c == my_body[-1]:
            is_move_safe["down"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for snake in opponents:
        for c in snake['body']:
            if c["x"] == my_head["x"] + 1 and c["y"] == my_head["y"]:
                is_move_safe["right"] = False
            if c["x"] == my_head["x"] - 1 and c["y"] == my_head["y"]:
                is_move_safe["left"] = False
            if c["x"] == my_head["x"] and c["y"] == my_head["y"] + 1:
                is_move_safe["up"] = False
            if c["x"] == my_head["x"] and c["y"] == my_head["y"] - 1:
                is_move_safe["down"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    grid = [[0 for _ in range(board_width)] for _ in range(board_height)]
    my_tail = game_state['you']['body'][-1]
    for snake in opponents:
        for c in snake['body']:
            grid[c["x"]][c["y"]] = 1
    
    spot = {"x" : my_head["x"], "y" : my_head["y"]}
    """
    if len(safe_moves) > 1:
        for i in range(len(safe_moves)):
            if safe_moves[i] == "up":
                spot["y"] += 1
            elif safe_moves[i] == "down":
                spot["y"] -= 1
            elif safe_moves[i] == "left":
                spot["x"] -= 1
            elif safe_moves[i] == "right":
                spot["x"] += 1

            x = spot["x"]
            y = spot["y"]
            if y > 0 and x > 0 and y < board_height - 1 and x < board_width - 1:
                if grid[x][y+1] == 1 and grid[x][y-1] == 1 and grid[x+1][y] == 1 and grid[x-1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif not y > 0 and x > 0 and y < board_height - 1 and x < board_width - 1:
                if grid[x][y+1] == 1 and grid[x+1][y] == 1 and grid[x-1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif not x > 0 and y > 0 and y < board_height - 1 and x < board_width - 1:
                if grid[x][y+1] == 1 and grid[x][y-1] == 1 and grid[x+1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif x > 0 and y > 0 and not y < board_height - 1 and x < board_width - 1:
                if grid[x-1][y] == 1 and grid[x][y-1] == 1 and grid[x+1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif y > 0 and x > 0 and y < board_height - 1 and not x < board_width - 1:
                if grid[x][y+1] == 1 and grid[x][y-1] == 1 and grid[x-1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif not y > 0 and not x > 0 and y < board_height - 1 and x < board_width - 1:
                if grid[x][y+1] == 1 and grid[x+1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif y > 0 and not x > 0 and not y < board_height - 1 and x < board_width - 1:
                if grid[x][x+1] == 1 and grid[x][y-1] == 1:
                    safe_moves.remove(safe_moves[i])
            elif y > 0 and x > 0 and not y < board_height - 1 and not x < board_width - 1:
                if grid[x][y-1] == 1 and grid[x-1][y] == 1:
                    safe_moves.remove(safe_moves[i])
            elif not y > 0 and x > 0 and y < board_height - 1 and not x < board_width - 1:
                if grid[x][y+1] == 1 and grid[x-1][y] == 1:
                    safe_moves.remove(safe_moves[i])
    """
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    if len(safe_moves) == 1:
        print(f"MOVE {game_state['turn']}: {safe_moves[0]}")
        return {"move": safe_moves[0]}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    right = False
    left = False
    up = False
    down = False
    for d in safe_moves:
        if d == "up":
            up = True
        if d == "right":
            right = True
        if d == "left":
            left = True
        if d == "down":
            down = True
    
    closest_food = food[0]
    c = 100
    for i in range(len(food)):
        n = abs(food[i]["x"] - my_head["x"]) + abs(food[i]["y"] - my_head["y"])
        if n < c:
            c = n
            closest_food = food[i]
    food_spot = None
    if closest_food["x"] > my_head["x"] and right:
        food_spot = "right"
    elif closest_food["y"] > my_head["y"] and up:
        food_spot = "up"
    elif closest_food["x"] < my_head["x"] and left:
        food_spot = "left"
    elif closest_food["y"] < my_head["y"] and down:
        food_spot = "down"
    
    # TODO: Step 5 - Try to survive as long as possible

    

    direction = None
    if len(game_state["board"]["snakes"]) == 1 and game_state["you"]["health"] > 6:
        if my_tail["x"] > my_head["x"] and "right" in safe_moves:
            direction = "right"
        elif my_tail["y"] > my_head["y"] and "up" in safe_moves:
            direction = "up"
        elif my_tail["x"] < my_head["x"] and "left" in safe_moves:
            direction = "left"
        elif my_tail["y"] < my_head["y"] and "down" in safe_moves:
            direction = "down"
    if direction != None:
        next_move = direction
    else:
        next_move = food_spot

    


    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
