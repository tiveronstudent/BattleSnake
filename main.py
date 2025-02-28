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

    # CHECKS FOR SPOTS THAT WOULD KILL THE SNAKE
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    opponents = game_state['board']['snakes']

    my_head = game_state["you"]["body"][0]

    grid = [[0 for _ in range(board_width)] for _ in range(board_height)]
    my_tail = game_state['you']['body'][-1]
    for snake in opponents:
        for c in snake['body']:
            grid[c["x"]][c["y"]] += 4
    for snake in opponents:
        tail = snake["body"][-1]
        grid[tail["x"]][tail["y"]] -= 3
    
    if my_head["y"] == 0:
        is_move_safe["down"] = False
        print("Not down!")
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
        print("Not up!")
    if my_head["x"] == 0:
        is_move_safe["left"] = False
        print("Not left!")
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
        print("Not right!")
    
    if my_head["x"] != 0 and grid[my_head["x"] - 1][my_head["y"]] >= 1:
        is_move_safe["left"] = False
    if my_head["x"] != board_width - 1 and grid[my_head["x"] + 1][my_head["y"]] >= 1:
        is_move_safe["right"] = False
    if my_head["y"] != 0 and grid[my_head["x"]][my_head["y"] - 1] >= 1:
        is_move_safe["down"] = False
    if my_head["y"] != board_height - 1 and grid[my_head["x"]][my_head["y"] + 1] >= 1:
        is_move_safe["up"] = False
    
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    # checks if next move for opponent is a move for it's own head
    if len(safe_moves) > 1:
        for snake in opponents:
            other_head = snake["body"][0]
            if other_head != my_head and snake["length"] >= game_state["you"]["length"]:
                if other_head["x"] != board_width - 1:
                    grid[other_head["x"] + 1][other_head["y"]] += 1
                if other_head["x"] != 0:
                    grid[other_head["x"] - 1][other_head["y"]] += 1
                if other_head["y"] != board_height - 1:
                    grid[other_head["x"]][other_head["y"] + 1] += 1
                if other_head["y"] != 0:
                    grid[other_head["x"]][other_head["y"] - 1] += 1
    if my_head["x"] != 0 and grid[my_head["x"] - 1][my_head["y"]] >= 1:
        is_move_safe["left"] = False
        print("no more left!")
    if my_head["x"] != board_width - 1 and grid[my_head["x"] + 1][my_head["y"]] >= 1:
        is_move_safe["right"] = False
        print("no more right!")
    if my_head["y"] != 0 and grid[my_head["x"]][my_head["y"] - 1] >= 1:
        is_move_safe["down"] = False
        print("no more down!")
    if my_head["y"] != board_height - 1 and grid[my_head["x"]][my_head["y"] + 1] >= 1:
        is_move_safe["up"] = False
        print("no more up!")
    
    safe_moves2 = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves2.append(move)
    
    least_risky = ""
    if len(safe_moves2) == 0:
        print("choosing least risky move")
        spot = {"x" : my_head["x"], "y" : my_head["y"]}
        min = 5
        for move in safe_moves:
            if move == "right":
                spot["x"] += 1
            elif move == "left":
                spot["x"] -= 1
            elif move == "up":
                spot["y"] += 1
            elif move == "down":
                spot["y"] -= 1
            if grid[spot["x"]][spot["y"]] < min:
                min = grid[spot["x"]][spot["y"]]
                least_risky = move
            else:
                pass #check if it is equal risk, then pick spot with food because it is more worth it
        safe_moves2.append(least_risky)
    if len(safe_moves2) > 0:
        print("switched safe_moves!")
        safe_moves = safe_moves2  

    # RETURNS A MOVE IF ONLY ONE MOVE OR NO MOVES ARE AVAILABLE
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    if len(safe_moves) == 1:
        print(f"MOVE {game_state['turn']}: {safe_moves[0]}")
        return {"move": safe_moves[0]}




    # CHOOSES RANDOM SAFE MOVE
    next_move = random.choice(safe_moves)

    # FINDS THE NEAREST FOOD
    food = game_state['board']['food']
    
    closest_food = food[0]
    c = 100
    for i in range(len(food)):
        n = abs(food[i]["x"] - my_head["x"]) + abs(food[i]["y"] - my_head["y"])
        if n < c:
            c = n
            closest_food = food[i]

    # PICKS THE MOVE THAT WOULD TAKE SNAKE TO THE NEAREST FOOD
    food_spot = None
    if closest_food["x"] > my_head["x"] and "right" in safe_moves:
        food_spot = "right"
    elif closest_food["y"] > my_head["y"] and "up" in safe_moves:
        food_spot = "up"
    elif closest_food["x"] < my_head["x"] and "left" in safe_moves:
        food_spot = "left"
    elif closest_food["y"] < my_head["y"] and "down" in safe_moves:
        food_spot = "down"
    
    # CHASES TAIL IF ONLY SNAKE ON BOARD AND HAS ENOUGH HEALTH, OTHERWISE FINDS FOOD
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
        else:
            if (my_tail["x"] > my_head["x"] or my_tail["x"] < my_head["x"]) and "up" in safe_moves:
                direction = "up"
            elif (my_tail["x"] > my_head["x"] or my_tail["x"] < my_head["x"]) and "down" in safe_moves:
                direction = "down"
            if (my_tail["y"] > my_head["y"] or my_tail["y"] < my_head["y"]) and "right" in safe_moves:
                direction = "right"
            elif (my_tail["y"] > my_head["y"] or my_tail["y"] < my_head["y"]) and "right" in safe_moves:
                direction = "down"
    if direction != None:
        next_move = direction
    else:
        next_move = food_spot

    if next_move == None:
        next_move = random.choice(safe_moves)

    # RETURNS THE MOVE CHOSEN
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}



# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
