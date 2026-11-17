import asyncio
import random
import pygame

pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 400, 440
BOARD_SIZE = 400
BOARD_TOP = 40
BLOCK = 100
ROWS = COLS = 4
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (231, 76, 60)
VIOLET = (136, 78, 160)
DARK_GREY = (35, 35, 35)
BORDER = (255, 255, 255)


PLAYER_COLORS = [RED, VIOLET]
PLAYER_NAMES = ["Player 1", "Player 2"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chain Reaction")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("Arial", 34, bold=True)
button_font = pygame.font.SysFont("Arial", 19, bold=True)
status_font = pygame.font.SysFont("Arial", 18)
small_font = pygame.font.SysFont("Arial", 15)


def make_empty_board():
    return [[[None, 0] for _ in range(COLS)] for _ in range(ROWS)]


def get_neighbors(row, col):
    result = []
    if row > 0:
        result.append((row - 1, col))
    if row < ROWS - 1:
        result.append((row + 1, col))
    if col > 0:
        result.append((row, col - 1))
    if col < COLS - 1:
        result.append((row, col + 1))
    return result


def critical_mass(row, col):
    return len(get_neighbors(row, col))


def copy_board(board):
    return [[cell.copy() for cell in row] for row in board]


def legal_moves(board, player):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            owner, _ = board[row][col]
            if owner is None or owner == player:
                moves.append((row, col))
    return moves


def resolve_chain(board, start_row, start_col, player):
    """Resolve all explosions without recursive function calls."""
    pending = [(start_row, start_col)]
    explosions = 0
    max_explosions = 10000

    while pending:
        row, col = pending.pop(0)
        owner, atoms = board[row][col]
        limit = critical_mass(row, col)

        if atoms < limit:
            continue

        board[row][col][1] -= limit
        if board[row][col][1] == 0:
            board[row][col][0] = None

        explosions += 1
        if explosions > max_explosions:
            # Safety guard against a pathological infinite chain.
            break

        for nr, nc in get_neighbors(row, col):
            board[nr][nc][0] = player
            board[nr][nc][1] += 1
            if board[nr][nc][1] >= critical_mass(nr, nc):
                pending.append((nr, nc))


def apply_move(board, row, col, player):
    owner, atoms = board[row][col]
    if owner is not None and owner != player:
        return False

    board[row][col][0] = player
    board[row][col][1] += 1
    resolve_chain(board, row, col, player)
    return True


def count_atoms(board):
    totals = [0, 0]
    for row in board:
        for owner, atoms in row:
            if owner in (0, 1):
                totals[owner] += atoms
    return totals


def get_winner(board, turns_played):
    # Avoid declaring a winner before both sides have had a first move.
    if turns_played < 2:
        return None

    totals = count_atoms(board)
    if totals[0] == 0 and totals[1] > 0:
        return 1
    if totals[1] == 0 and totals[0] > 0:
        return 0
    return None


# ---------------------------------------------------------------------
# COMPUTER PLAYER
# Two-ply search: consider each computer move, then the strongest
# response the human could make. Evaluation rewards material, territory,
# and useful cells that are close to exploding.
# ---------------------------------------------------------------------
def evaluate_board(board):
    score = 0.0

    for row in range(ROWS):
        for col in range(COLS):
            owner, atoms = board[row][col]
            if owner is None or atoms == 0:
                continue

            sign = 1 if owner == 1 else -1
            score += sign * (atoms * 1.0 + 1.5)

            limit = critical_mass(row, col)
            if atoms == limit - 1:
                vulnerable_neighbors = 0
                for nr, nc in get_neighbors(row, col):
                    neighbor_owner, neighbor_atoms = board[nr][nc]
                    if neighbor_owner is not None and neighbor_owner != owner:
                        vulnerable_neighbors += 1
                threat_value = 1.5 + vulnerable_neighbors * 1.25
                score += sign * threat_value

    return score


def choose_computer_move(board):
    options = legal_moves(board, 1)
    if not options:
        return None

    best_score = float("-inf")
    best_moves = []

    for row, col in options:
        after_computer = copy_board(board)
        apply_move(after_computer, row, col, 1)

        if get_winner(after_computer, 2) == 1:
            return (row, col)

        human_options = legal_moves(after_computer, 0)
        if not human_options:
            move_score = evaluate_board(after_computer)
        else:
            # Human chooses the reply that is worst for the computer.
            worst_reply_score = float("inf")
            for human_row, human_col in human_options:
                after_human = copy_board(after_computer)
                apply_move(after_human, human_row, human_col, 0)

                if get_winner(after_human, 3) == 0:
                    reply_score = -100000
                elif get_winner(after_human, 3) == 1:
                    reply_score = 100000
                else:
                    reply_score = evaluate_board(after_human)

                worst_reply_score = min(worst_reply_score, reply_score)

            move_score = worst_reply_score

        if move_score > best_score:
            best_score = move_score
            best_moves = [(row, col)]
        elif move_score == best_score:
            best_moves.append((row, col))

    return random.choice(best_moves)


# ---------------------------------------------------------------------
# DRAWING
# -------------------------------------------------------------------
def draw_button(rect, text, color=RED):
    pygame.draw.rect(screen, color, rect, border_radius=14)
    label = button_font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_menu():
    screen.fill(BLACK)

    title = title_font.render("Chain Reaction", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 105)))

    computer_button = pygame.Rect(90, 190, 220, 52)
    friend_button = pygame.Rect(90, 270, 220, 52)

    draw_button(computer_button, "Play with Computer")
    draw_button(friend_button, "Play with Friend")

    hint = small_font.render("Choose a game mode", True, WHITE)
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 365)))

    return computer_button, friend_button


def draw_board(board, current_player, mode):
    screen.fill(BLACK)

    if mode == "computer":
        turn_text = "Your turn" if current_player == 0 else "Computer thinking..."
    else:
        turn_text = f"{PLAYER_NAMES[current_player]}'s turn"

    turn_color = PLAYER_COLORS[current_player]
    status = status_font.render(turn_text, True, turn_color)
    screen.blit(status, status.get_rect(center=(WIDTH // 2, 20)))

    # Grid lines, matching the original game's player-colored lines.
    for index in range(ROWS + 1):
        position = index * BLOCK
        pygame.draw.line(
            screen, turn_color,
            (0, BOARD_TOP + position),
            (BOARD_SIZE, BOARD_TOP + position), 2
        )
        pygame.draw.line(
            screen, turn_color,
            (position, BOARD_TOP),
            (position, BOARD_TOP + BOARD_SIZE), 2
        )

    # Draw one, two, or three atoms in each cell.
    for row in range(ROWS):
        for col in range(COLS):
            owner, atoms = board[row][col]
            if owner is None or atoms == 0:
                continue

            color = PLAYER_COLORS[owner]
            center_x = col * BLOCK + BLOCK // 2
            center_y = BOARD_TOP + row * BLOCK + BLOCK // 2
            radius = 11

            if atoms == 1:
                positions = [(center_x, center_y)]
            elif atoms == 2:
                positions = [
                    (center_x - 16, center_y),
                    (center_x + 16, center_y)
                ]
            else:
                positions = [
                    (center_x, center_y - 17),
                    (center_x - 17, center_y + 13),
                    (center_x + 17, center_y + 13)
                ]

            for x, y in positions:
                pygame.draw.circle(screen, color, (x, y), radius)

    footer = small_font.render("ESC: Menu   |   R: Restart   |   Q: Quit", True, WHITE)
    screen.blit(footer, footer.get_rect(center=(WIDTH // 2, HEIGHT - 10)))


def draw_game_over(board, current_player, winner, mode):
    draw_board(board, current_player, mode)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 175))
    screen.blit(overlay, (0, 0))

    if mode == "computer":
        winner_text = "You won!" if winner == 0 else "Computer won!"
    else:
        winner_text = f"{PLAYER_NAMES[winner]} won!"

    title = title_font.render(winner_text, True, WHITE)
    restart = status_font.render("Press R to play again", True, WHITE)
    menu = status_font.render("Press M for menu", True, WHITE)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 185)))
    screen.blit(restart, restart.get_rect(center=(WIDTH // 2, 235)))
    screen.blit(menu, menu.get_rect(center=(WIDTH // 2, 270)))


# ---------------------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------------------
async def main():
    state = "menu"
    mode = None
    board = make_empty_board()
    current_player = 0
    turns_played = 0
    winner = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

                elif event.key == pygame.K_ESCAPE and state == "game":
                    state = "menu"

                elif event.key == pygame.K_r and state in ("game", "over"):
                    board = make_empty_board()
                    current_player = 0
                    turns_played = 0
                    winner = None
                    state = "game"

                elif event.key == pygame.K_m and state == "over":
                    state = "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos

                if state == "menu":
                    computer_button = pygame.Rect(90, 190, 220, 52)
                    friend_button = pygame.Rect(90, 270, 220, 52)

                    if computer_button.collidepoint(mouse_x, mouse_y):
                        mode = "computer"
                        board = make_empty_board()
                        current_player = 0
                        turns_played = 0
                        winner = None
                        state = "game"

                    elif friend_button.collidepoint(mouse_x, mouse_y):
                        mode = "friend"
                        board = make_empty_board()
                        current_player = 0
                        turns_played = 0
                        winner = None
                        state = "game"

                elif state == "game" and not (
                    mode == "computer" and current_player == 1
                ):
                    if BOARD_TOP <= mouse_y < BOARD_TOP + BOARD_SIZE:
                        col = mouse_x // BLOCK
                        row = (mouse_y - BOARD_TOP) // BLOCK

                        if 0 <= row < ROWS and 0 <= col < COLS:
                            if apply_move(board, row, col, current_player):
                                turns_played += 1
                                winner = get_winner(board, turns_played)

                                if winner is not None:
                                    state = "over"
                                else:
                                    current_player = 1 - current_player

        # Let the computer make its move after the human's move.
        if (
            state == "game"
            and mode == "computer"
            and current_player == 1
            and winner is None
        ):
            await asyncio.sleep(0.12)
            computer_move = choose_computer_move(board)

            if computer_move is not None:
                apply_move(board, computer_move[0], computer_move[1], 1)
                turns_played += 1
                winner = get_winner(board, turns_played)

                if winner is not None:
                    state = "over"
                else:
                    current_player = 0

        if state == "menu":
            draw_menu()
        elif state == "game":
            draw_board(board, current_player, mode)
        elif state == "over":
            draw_game_over(board, current_player, winner, mode)

        pygame.display.flip()
        clock.tick(FPS)

        # Required by Pygbag: yield control so the browser can update.
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
