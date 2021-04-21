######## HEURISTICS #########

# heuristic 1 
# takes in a state; returns number of cars blocking X
def blocking_heuristic(state):
  # extract row 3
  row3 = state[2]
  # Goal: if there is an x in the last 2 spots
  if (row3[4] == "X") and (row3[5] == "X"):
    return 0
  penalty = 1
  # from back to front, count all non "-" until you reach x
  index = 5
  current_char = row3[index]
  while current_char != "X":
    if current_char != "-":
      penalty = penalty + 1
    index = index - 1
    current_char = row3[index]
  return penalty 

# heuristic 2
# takes in a state; returns the number of cars blocking another car
# if XX in the correct spot, return 0
# if no cars are blocked, return 1
# if cars are being blocked, return 1 + the number of occurances
def total_heuristic(state):
  blocked = 1
  # Goal: if there is an x in the last 2 spots
  if (state[2][4] == "X") and (state[2][5] == "X"):
    return 0
  # generate a dict of cars and their orientations 
  car_dict = car_orientations(state)
  for car in car_dict:
    # if car is horizontal; count cars directly to the cars left and right 
    if car_dict[car] == "h":
      # count cars directly left
      blocked = blocked + num_cars_left(car, state)
      # count cars directly right
      blocked = blocked + num_cars_right(car, state)
    # if car verticle count cars directly above and below 
    if car_dict[car] == "v":
      # count cars directly above
      blocked = blocked + num_cars_above(car, state)
      # count cars directly below
      blocked = blocked + num_cars_below(car, state)
  return blocked 



######## HEURISTIC #2 HELPER FUNCTIONS ###################

# returns the number of cars blocking a car from moving up (0 or 1)
def num_cars_above(letter, state):
  coords = coords_car(letter, state)
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[0])
    # if car is at the top anyway return 0
    if coord_pair[0] == 0:
      return 0
  # if car not at top, and the spot above is not empty, its being blocked
  if state[min(rows) - 1][coords[0][1]] != "-":
    return 1
  # if not being blocked return 0
  else:
    return 0

# returns the number of cars blocking a car from moving down (0 or 1)
def num_cars_below(letter, state):
  coords = coords_car(letter, state)
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[0])
    # if car is at the bottom anyway return 0
    if coord_pair[0] == 5:
      return 0
  # if car not at bottom, and the spot above is not empty, its being blocked
  if state[max(rows) + 1][coords[0][1]] != "-":
    return 1
  # if not being blocked return 0
  else:
    return 0


# returns the number of cars blocking a car from moving left (0 or 1)
def num_cars_left(letter, state):
  coords = coords_car(letter, state)
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[1])
    # if car is at the left anyway return 0
    if coord_pair[1] == 0:
      return 0
  # if car not at bottom, and the spot above is not empty, its being blocked
  if state[coords[0][0]][min(rows) - 1] != "-":
    return 1
  # if not being blocked return 0
  else:
    return 0
  
# returns the number of cars blocking a car from moving right (0 or 1)
def num_cars_right(letter, state):
  coords = coords_car(letter, state)
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[1])
    # if car is at the right anyway return 0
    if coord_pair[1] == 5:
      return 0
  # if car not at bottom, and the spot above is not empty, its being blocked
  if state[coords[0][0]][max(rows) + 1] != "-":
    return 1
  # if not being blocked return 0
  else:
    return 0



############ HELPER FUNCTIONS ##########

# print a state in visual fashion 
def state_printer(state):
  for row in state:
    print(row)
  print("\n")

# count the number of occurances of a letter in a row
def letter_counter(letter, row):
  count = 0
  for char in row:
    if char == letter:
      count = count + 1
  return count

# returns a dictionary of cars and their directions
def car_orientations(state):
  cars = {}
  cars["X"] = "h"
  for row in state:
    for char in row:
      if (char != "-") and (char != "X"):
        # check if letter already in dictionary
        if char not in cars:
          num_occurances = letter_counter(char, row)
          # if more than 1 in a row; its horizontal
          if num_occurances > 1:
            cars[char] = "h"
          else:
            cars[char] = "v"
  return cars

# gets all coordinates of a single car
def coords_car(letter, state):
  list_of_coords = []
  for row in range(len(state)):
    for col in range(len(state[0])):
      if state[row][col] == letter:
        coords = [row, col]
        list_of_coords.append(coords)
  return list_of_coords 

# turn a string into a list
def string_to_list(row):
  list = []
  for letter in row:
    list.append(letter)
  return list

# turns list to string 
def list_to_string(list):
  string = ""
  for item in list:
    string = string + item
  return string 

######### NEXT STATE GENERATORS #########

# moves one car up if possible, or return null
def move_up(letter, stateOG):
  state = stateOG[:]
  coords = coords_car(letter, state)
  # if car at top; return null
  for coord_pair in coords:
    if coord_pair[0] == 0:
      return None
  # otherwise, move car up 1:
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[0])
  start = min(rows)
  stop = max(rows)
  # if one above start not -; return null
  if state[start - 1][coords[0][1]] != "-":
    return None
  else:
    # move top up
    row_as_list = string_to_list(state[start - 1])
    row_as_list[coords[0][1]] = letter
    state[start - 1] = list_to_string(row_as_list)
    # add blank below 
    row_as_list = string_to_list(state[stop])
    row_as_list[coords[0][1]] = "-"
    state[stop] = list_to_string(row_as_list)
    return state

# moves car one down if possible; else return null
def move_down(letter, stateOG):
  state = stateOG[:]
  coords = coords_car(letter, state)
  # if car at bottom; return null
  for coord_pair in coords:
    if coord_pair[0] == 5:
      return None
  # otherwise, move car down 1:
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[0])
  start = min(rows)
  stop = max(rows)
  # if one below start not -; return null
  if state[stop + 1][coords[0][1]] != "-":
    return None
  else:
    # move bottom down
    row_as_list = string_to_list(state[stop + 1])
    row_as_list[coords[0][1]] = letter
    state[stop + 1] = list_to_string(row_as_list)
    # add blank above 
    row_as_list = string_to_list(state[start])
    row_as_list[coords[0][1]] = "-"
    state[start] = list_to_string(row_as_list)
    return state

# moves car one to the left if possible, or return null
def move_left(letter, stateOG):
  #copy list as to not alter the original 
  state = stateOG[:]
  coords = coords_car(letter, state)
  # if car at left; return null
  for coord_pair in coords:
    if coord_pair[1] == 0:
      return None
  # otherwise, move car left 1:
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[1])
  start = min(rows)
  stop = max(rows)
  # if one ableft of start not -; return null
  correct_row = coords[0][0]
  if state[correct_row][start - 1] != "-":
    return None
  else:
    # move leftmost left
    row_as_list = string_to_list(state[correct_row])
    row_as_list[start - 1] = letter
    state[correct_row] = list_to_string(row_as_list)
    # add blank to the right 
    row_as_list = string_to_list(state[correct_row])
    row_as_list[stop] = "-"
    state[correct_row] = list_to_string(row_as_list)
    return state

# moves car one to the right if possible, or return null
def move_right(letter, stateOG):
  state = stateOG[:]
  coords = coords_car(letter, state)
  # if car at right; return null
  for coord_pair in coords:
    if coord_pair[1] == 5:
      return None
  # otherwise, move car right 1:
  rows = []
  for coord_pair in coords:
    rows.append(coord_pair[1])
  start = min(rows)
  stop = max(rows)
  # if one right of start not -; return null
  correct_row = coords[0][0]
  if state[correct_row][stop + 1] != "-":
    return None
  else:
    # move right most right
    row_as_list = string_to_list(state[correct_row])
    row_as_list[stop + 1] = letter
    state[correct_row] = list_to_string(row_as_list)
    # add blank to the left
    row_as_list = string_to_list(state[correct_row])
    row_as_list[start] = "-"
    state[correct_row] = list_to_string(row_as_list)
    return state

############# ALL NEXT STATE GENERATER ##########

# generates all possible next states given a current state
def generate_next_state(state):
  # move to main later:
  car_dict = car_orientations(state)

  next_states = []
  for car in car_dict:
    # if car is horizontal move left and right
    if car_dict[car] == "h":
      right = move_right(car, state)
      if right != None:
        next_states.append(right)
      left = move_left(car, state)
      if left != None:
        next_states.append(left)
    # if car verticle move up and down
    if car_dict[car] == "v":
      down = move_down(car, state)
      if down != None:
        next_states.append(down)
      up = move_up(car, state)
      if up != None:
        next_states.append(up)
  return next_states

############### BEST FIRST SEARCH ALGO #############

# strategy: 0 or 1 to indicate h(n) strategy
# unexplored is the list of next states
# path is a list of how we got where we are 
def best_first_search(strategy, unexplored, path, states_explored):
  # if nothing left to explore, return null
  if unexplored == []:
    return []
  else:
    # make a dictionary which will pair h value with state
    state_ranks = {}
    for state in unexplored:
      # find the heuristic penalty for a given state
      h = 0
      if strategy == 0:
        h = blocking_heuristic(state)
      else:
        h = total_heuristic(state)
      # add to the length of the path so far
      f = h + len(path)
      state_ranks[f] = state
      # if any of the options generated the goal, return that
      if len(path) in state_ranks:
        # add the final state to the path
        path.append(state_ranks[len(path)])
        return path, states_explored
      else:
        # find the board which generated the best f value
        best_next = min(state_ranks)
        # add best state to the path 
        path.append(state_ranks[best_next])
        # find the next set of nodes given the best set
        next_states = generate_next_state(state_ranks[best_next])

        states_explored = states_explored + len(next_states)

        # deal with circuits here???

        result = best_first_search(strategy, next_states, path, states_explored)
        if result != []:
          return result
        else:
          return best_first_search(strategy, generate_next_state(unexplored[1:]), path, states_expored)

def rushhour(heuristic, start_state):
  # pass all information to the best first search
  best_path = best_first_search(0, [start_state], [], 0)
  # extract results from the answer 
  path = best_path[0]
  total_moves = len(path) - 1
  states_explored = best_path[1]
  print("Solution:")
  for state in path:
    state_printer(state)
  print("Total Moves: ", total_moves)
  print("Total States Explored: ", states_explored)