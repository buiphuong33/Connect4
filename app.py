from fastapi import FastAPI, HTTPException
import random
import uvicorn
import math
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState(BaseModel):
    board: List[List[int]]
    current_player: int
    valid_moves: List[int]

class AIResponse(BaseModel):
    move: int

def get_best_move(state: GameState) -> int:
    import math, random

    ROW_COUNT = 6
    COLUMN_COUNT = 7
    WINDOW_LENGTH = 4
    AI_PLAYER = state.current_player
    OPPONENT = 2 if AI_PLAYER == 1 else 1
    board = state.board
    last_depth = 6

    def make_move(board, col, player):
        new_board = [row[:] for row in board]
        for row in reversed(range(ROW_COUNT)):
            if new_board[row][col] == 0:
                new_board[row][col] = player
                return new_board
        return new_board

    def get_valid_moves(board):
        return [c for c in range(COLUMN_COUNT) if board[0][c] == 0]

    def winning_move(board, player):
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if all(board[r][c + i] == player for i in range(4)):
                    return True
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT):
                if all(board[r + i][c] == player for i in range(4)):
                    return True
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                if all(board[r + i][c + i] == player for i in range(4)):
                    return True
        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if all(board[r - i][c + i] == player for i in range(4)):
                    return True
        return False

    def evaluate_window(window, player):
        score = 0
        opp = OPPONENT if player == AI_PLAYER else AI_PLAYER

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2
        if window.count(opp) == 3 and window.count(0) == 1:
            score -= 4
        return score

    def score_position(board, player):
        score = 0
        center_array = [board[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
        score += center_array.count(player) * 3

        for r in range(ROW_COUNT):
            row_array = board[r]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, player)

        for c in range(COLUMN_COUNT):
            col_array = [board[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, player)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, player)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, player)

        return score

    def is_terminal(board):
        return winning_move(board, AI_PLAYER) or winning_move(board, OPPONENT) or len(get_valid_moves(board)) == 0

    def opponent_can_win_next(board, col):
        new_board = make_move(board, col, AI_PLAYER)
        opp_moves = get_valid_moves(new_board)
        for opp_col in opp_moves:
            if winning_move(make_move(new_board, opp_col, OPPONENT), OPPONENT):
                return True
        return False

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = get_valid_moves(board)

        # === Move ordering: prioritize by score ===
        move_scores = []
        for col in valid_locations:
            new_board = make_move(board, col, AI_PLAYER if maximizingPlayer else OPPONENT)
            move_scores.append((col, score_position(new_board, AI_PLAYER)))
        ordered_moves = [col for col, _ in sorted(move_scores, key=lambda x: x[1], reverse=maximizingPlayer)]

        is_terminal_node = is_terminal(board)

        if depth == 0 or is_terminal_node:
            if is_terminal_node:
                if winning_move(board, AI_PLAYER):
                    return (None, 1e10)
                elif winning_move(board, OPPONENT):
                    return (None, -1e10)
                else:
                    return (None, 0)
            else:
                return (None, score_position(board, AI_PLAYER))

        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in ordered_moves:
                # Skip moves that allow opponent to win immediately
                if opponent_can_win_next(board, col):
                    continue
                new_board = make_move(board, col, AI_PLAYER)
                new_score = minimax(new_board, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in ordered_moves:
                new_board = make_move(board, col, OPPONENT)
                new_score = minimax(new_board, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value
        
    for col in state.valid_moves:
     temp_board = make_move(board, col, AI_PLAYER)
     if winning_move(temp_board, AI_PLAYER):
        return col

    best_move, _ = minimax(board, last_depth, -math.inf, math.inf, True)

    # Fall-back in case all good moves are filtered
    if best_move is None or best_move not in state.valid_moves:
        for col in state.valid_moves:
            if not opponent_can_win_next(board, col):
                return col
        return random.choice(state.valid_moves)

    return best_move;

@app.post("/api/connect4-move")
async def make_move(game_state: GameState) -> AIResponse:
    try:
        if not game_state.valid_moves:
            raise ValueError("Không có nước đi hợp lệ")
            
        selected_move = get_best_move(game_state) # change logic thuật toán AI của bạn ở đây
        
        return AIResponse(move=selected_move)
    except Exception as e:
        if game_state.valid_moves:
            return AIResponse(move=game_state.valid_moves[0])
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/api/test")
async def health_check():
    return {"status": "ok", "message": "Server is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)