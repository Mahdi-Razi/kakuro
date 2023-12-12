import pygame
import time

pygame.init()
start_time = time.time()
WIDTH = 560
HEIGHT = 560
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Kakuro board with tuples representing the clue values and whether the cell is filled or not
board = [
    [(-1,-1),  (23, -1), (30, -1), (-1, -1), (-1, -1), (27,-1), (12, -1), (16, -1)],
    [(-1, 16), (0, 0),   (0, 0),   (-1, -1), (17, 24), (0, 0),  (0, 0),   (0, 0)],
    [(-1, 17), (0, 0),   (0, 0),   (15, 29), (0, 0),   (0, 0),  (0, 0),   (0, 0)],
    [(-1, 35), (0, 0),   (0, 0),   (0, 0),   (0, 0),   (0, 0),  (12, -1), (-1, -1)],
    [(-1, -1), (-1, 7),  (0, 0),   (0, 0),   (7, 8),   (0, 0),  (0, 0),   (7, -1)],
    [(-1, -1), (11, -1), (10, 16), (0, 0),   (0, 0),   (0, 0),  (0, 0),   (0, 0)],
    [(-1, 21), (0, 0),   (0, 0),   (0, 0),   (0, 0),   (-1, 5), (0, 0),   (0, 0)],
    [(-1, 6),  (0, 0),   (0, 0),   (0, 0),   (-1, -1), (-1, 3), (0, 0),   (0, 0)],
]

h = HEIGHT // (len(board))
w = WIDTH // (len(board[0]))

# Draw the Kakuro board on the screen with graphical representation.
def draw_board():
    for i in range(len(board)):
        for j in range(len(board[0])):
            f, s = board[i][j]
            # empty cell
            if s == 0:
                pygame.draw.rect(screen, "black", [j * w, i * h, (j + 1) * w, (i + 1) * h], 5)
                # filled cell with answer
                if f != 0:
                    font = pygame.font.Font('freesansbold.ttf', 40)
                    score_text = font.render(f'{f}', True, 'red')
                    screen.blit(score_text, (j * w + w // 3, i  * h + h // 3))
            else:
                l = 5
                r = 5
                # vertical clue is blank
                if f == -1:
                    l = 0
                # horizontal clue is blank
                if s == -1:
                    r = 0
                
                # draw clues or blanks
                font = pygame.font.Font('freesansbold.ttf', 20)
                score_text = font.render(f'{f}', True, 'black')
                screen.blit(score_text, (j * w + w // 4, (i + 1) * h - h // 2))
                score_text = font.render(f'{s}', True, 'black')
                screen.blit(score_text, ((j + 1) * w - w // 2, i * h + h // 4))
                pygame.draw.polygon(screen, "black", ((j * w, i * h), ((j + 1) * w, (i + 1) * h), (j * w, (i + 1) * h)), l)
                pygame.draw.polygon(screen, "black", ((j * w, i * h), ((j + 1) * w, (i + 1) * h), ((j + 1) * w, i * h)), r)


# finds clues assigned to (row, col)
def find_boundary_position(board, row, col):
    r = row
    c = col
    while board[r][col][1] == 0:
        r -= 1
    while board[row][c][1] == 0:
        c -= 1
    
    return r, c



# check if placing 'num' at position (row, col) is a valid move in the Kakuro board.
def is_valid(board, row, col, num):

    r, c = find_boundary_position(board, row, col)
    
    row_sum = board[row][c][1]
    col_sum = board[r][col][0]
    
    sum = 0
    remaining_empty_cells = 0
    while  c + 1 < len(board[0]) and board[row][c + 1][1] == 0:
        # no repitition is allowed
        if board[row][c + 1][0] == num:
            return False
        # counts number of remaining empty cells 
        if board[row][c + 1][0] == 0:
            remaining_empty_cells += 1
        # sum so far
        sum += board[row][c + 1][0]
        c += 1

    if num + sum > row_sum:
        return False
    
    if remaining_empty_cells == 1:
        if num + sum != row_sum:
            return False
    
    # calculates the max amount we can put in remaining empty cells
    v = remaining_empty_cells - 1
    z = 45 - ((9 - v) * (10 - v) / 2)
    if row_sum - num - sum > z:
        return False
    
    sum = 0
    remaining_empty_cells = 0
    while r + 1 < len(board) and board[r + 1][col][1] == 0:
        # no repitition is allowed        
        if board[r + 1][col][0] == num:
            return False
        # counts number of remaining empty cells 
        if board[r + 1][col][0] == 0:
            remaining_empty_cells += 1
        # sum so far
        sum += board[r + 1][col][0]
        r += 1

    if num + sum > col_sum:
        return False
    
    if remaining_empty_cells == 1:
        if num + sum != col_sum:
            return False
    
    # calculates the max amount we can put in remaining empty cells
    v = remaining_empty_cells - 1
    z = 45 - ((9 - v) * (10 - v) / 2)
    if col_sum - num - sum > z:
        return False
    
    return True

def backtracking(board):
    # Find most constrained position in the board
    empty, values = most_constrained_variable(board)
    
    # if no such location exits terminate
    if(empty == (-1, -1)):
        return True
    
    row, col = empty

    # Try placing digits from domain of that value in the empty position
    for num in values:
        if is_valid(board, row, col, num):
            # If placing 'num' is valid, update the board and recursively solve the remaining puzzle
            board[row][col] = (num, 0)

            if backtracking(board):
                return True

            # If the recursive call does not lead to a solution, backtrack
            board[row][col] = (0, 0)

    # If no digit can be placed, backtrack to the previous empty position
    return False


def legal_values(board, pos):
    row, col = pos
    # initially values are in range 1 - 9
    values = set(range(1, 10))
    r, c = find_boundary_position(board, row, col)
    
    while  c + 1 < len(board[0]) and board[row][c + 1][1] == 0:
        # discard values from domain if they are already used in row
        if board[row][c + 1][0] != 0:
            values.discard(board[row][c + 1][0])
        c += 1

    while r + 1 < len(board) and board[r + 1][col][1] == 0:
        # discard values from domain if they are already used in col
        if board[r + 1][col][0] != 0:
            values.discard(board[r + 1][col][0])
        r += 1

    # return domain
    return values


def most_constrained_variable(board):
    # find all empty positions
    empty_positions = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == (0, 0)]
    
    # if none exists return a flag
    if(len(empty_positions) == 0):
        return (-1, -1), {}
    
    # finds the variable with most constrains, its domain has fewest possible options
    mcv = empty_positions[0]
    min = legal_values(board, mcv)
    for position in empty_positions:
        curr = legal_values(board, position)
        if len(curr) < len(min):
            mcv = position
            min = curr
    
    # return mcv and its domain
    return mcv, min

if __name__ == '__main__': 
    # solve kakuro using backtracking and mcv filtering 
    backtracking(board)
    end_time = time.time()
    # print the elapsed time
    print(f'elapsed time: {end_time - start_time}')
    run = True
    while run:
        screen.fill('white')
        draw_board()
        # for quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        pygame.display.flip()

    pygame.quit()
