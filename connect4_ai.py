import math
import random
from connect4_utils import *  

# Khởi tạo bảng băm để lưu trạng thái bảng và kết quả Minimax, giúp tối ưu hóa tìm kiếm
transposition_table = {}

# Hàm đánh giá một cửa sổ 4 ô, tính điểm dựa trên số đĩa của người chơi và đối thủ
def evaluate_window(window, piece):
    opponent_piece = 2 if piece == 1 else 1  # Xác định đối thủ (1 hoặc 2)
    score = 0
    if window.count(piece) == 4:  # 4 đĩa: thắng ngay
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:  # 3 đĩa + 1 trống: tiềm năng cao
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:  # 2 đĩa + 2 trống: tiềm năng thấp
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1:  # Đối thủ 3 đĩa + 1 trống: nguy hiểm
        score -= 10
    elif window.count(opponent_piece) == 4:  # Đối thủ thắng: phạt điểm rất nặng
        score -= 10000000000
    return score

# Hàm đánh giá toàn bộ bảng, tính điểm dựa trên tất cả cửa sổ 4 ô và ưu tiên cột giữa
def score_position(board, piece):
    score = 0
    # Đếm số đĩa ở cột giữa thưởng điểm
    center_array = [int(i) for i in list(board[:, board.shape[1]//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # Kiểm tra ngang
    for r in range(board.shape[0]):  # Duyệt từng hàng
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(board.shape[1] - 3):  # Lấy từng cửa sổ 4 ô
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)
    # Kiểm tra dọc
    for c in range(board.shape[1]):  # Duyệt từng cột
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(board.shape[0] - 3):  # Lấy từng cửa sổ 4 ô
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)
    # Kiểm tra chéo chính (trên trái → dưới phải)
    for r in range(3, board.shape[0]):  # Chỉ xét các hàng đủ dài cho chéo
        for c in range(board.shape[1] - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    # Kiểm tra chéo phụ (dưới trái → trên phải)
    for r in range(3, board.shape[0]):
        for c in range(3, board.shape[1]):
            window = [board[r - i][c - i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

# Kiểm tra trạng thái kết thúc (thắng hoặc hòa)
def is_terminal_node(board, winning_move):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

# Lấy danh sách các cột hợp lệ (chưa đầy)
def get_valid_locations(board):
    return [col for col in range(board.shape[1]) if board[0][col] == 0]

# Tìm hàng trống thấp nhất trong cột col
def get_next_open_row(board, col):
    for r in range(board.shape[0] - 1, -1, -1):  # Duyệt từ dưới lên
        if board[r][col] == 0:
            return r
    return None  # Trả về None nếu cột đầy 

# Sắp xếp nước đi nâng cao: ưu tiên thắng, chặn đối thủ, hoặc dựa trên điểm heuristic
def advanced_move_order(valid_locations, board, piece, winning_move):
    opponent_piece = 2 if piece == 1 else 1
    move_scores = []
    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        b_copy[row][col] = piece
        if winning_move(b_copy, piece):  # Nếu nước đi dẫn đến thắng ngay
            return [col]  # Trả về ngay để ưu tiên
        b_copy[row][col] = opponent_piece
        if winning_move(b_copy, opponent_piece):  # Nếu nước đi chặn đối thủ thắng
            return [col]  # Trả về ngay để ưu tiên
        score = score_position(b_copy, piece)  # Đánh giá heuristic
        move_scores.append((col, score))
    # Sắp xếp các nước đi theo điểm từ cao đến thấp
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return [col for col, _ in move_scores]

# Sắp xếp nước đi đơn giản: ưu tiên cột gần trung tâm
def simple_move_order(valid_locations, board_width):
    center = board_width // 2
    return sorted(valid_locations, key=lambda x: abs(x - center))

# Thuật toán Minimax với cắt tỉa Alpha-Beta và bảng băm
def minimax(board, depth, alpha, beta, maximizing_player, piece, winning_move):
    # Tạo hash cho trạng thái bảng để tra cứu trong bảng băm
    board_hash = hash(str(board.tobytes()))
    # Nếu trạng thái đã được lưu với độ sâu đủ lớn, trả về kết quả
    if board_hash in transposition_table and transposition_table[board_hash][0] >= depth:
        return transposition_table[board_hash][1]

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board, winning_move)
    # Kiểm tra trạng thái kết thúc hoặc hết độ sâu
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, piece):  # AI thắng
                return (None, 10000000)
            elif winning_move(board, 2 if piece == 1 else 1):  # Đối thủ thắng
                return (None, -10000000)
            else:  # Hòa
                return (None, 0)
        else:  # Hết độ sâu, đánh giá bảng
            return (None, score_position(board, piece))

    # Sắp xếp nước đi để tối ưu cắt tỉa
    ordered_moves = advanced_move_order(valid_locations, board, piece, winning_move)

    if maximizing_player:  # Lượt của AI
        value = -math.inf
        column = ordered_moves[0]  # Mặc định chọn nước đi đầu tiên
        for col in ordered_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = piece
            # Gọi đệ quy cho lượt đối thủ
            new_score = minimax(b_copy, depth - 1, alpha, beta, False, piece, winning_move)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:  # Cắt tỉa
                break
        result = (column, value)
        # Lưu kết quả vào bảng băm
        transposition_table[board_hash] = (depth, result)
        return result
    else:  # Lượt của đối thủ
        value = math.inf
        column = ordered_moves[0]
        opponent_piece = 2 if piece == 1 else 1
        for col in ordered_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = opponent_piece
            # Gọi đệ quy cho lượt AI
            new_score = minimax(b_copy, depth - 1, alpha, beta, True, piece, winning_move)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:  # Cắt tỉa
                break
        result = (column, value)
        # Lưu kết quả vào bảng băm
        transposition_table[board_hash] = (depth, result)
        return result

# Hàm điều khiển trò chơi giữa người chơi và AI
def play_ai_game(screen, event, board, turn, not_over, my_font):
    winner = None
    if turn == PLAYER_TURN:  # Lượt của người chơi
        if event.type == pygame.MOUSEBUTTONDOWN and not_over:  # Khi người chơi nhấp chuột
            xpos = event.pos[0]
            col = int(math.floor((xpos - BOARD_X_OFFSET) / SQUARESIZE))  # Tính cột dựa trên vị trí chuột
            if 0 <= col < COLS and is_valid_location(board, col):  # Kiểm tra nước đi hợp lệ
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)  # Thả đĩa của người chơi
                if winning_move(board, PLAYER_PIECE):  # Kiểm tra thắng
                    winner = "Player WIN!"
                    not_over = False
                elif len(get_valid_locations(board)) == 0:  # Kiểm tra hòa
                    winner = "It's a tie!"
                    not_over = False
                turn = (turn + 1) % 2  # Chuyển lượt
    elif turn == AI_TURN and not_over:  # Lượt của AI
        # Gọi Minimax để tìm nước đi tốt nhất với độ sâu 5
        col, _ = minimax(board, 5, -math.inf, math.inf, True, AI_PIECE, winning_move)
        if 0 <= col < COLS and is_valid_location(board, col):  # Kiểm tra nước đi hợp lệ
            pygame.time.wait(500)  # Đợi 0.5 giây
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)  # Thả đĩa của AI
            if winning_move(board, AI_PIECE):  # Kiểm tra thắng
                winner = "FFF_AI WIN!"
                not_over = False
            elif len(get_valid_locations(board)) == 0:  # Kiểm tra hòa
                winner = "It's a tie!"
                not_over = False
            turn = (turn + 1) % 2  # Chuyển lượt
    return turn, not_over, winner  # Trả về lượt, trạng thái trò chơi, và người thắng