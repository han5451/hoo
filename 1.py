import streamlit as st
import random
import time

st.title("Streamlit 테트리스 - 가로 15, 세로 10")

WIDTH, HEIGHT = 15, 10

TETRIS_SHAPES = {
    "I": [[1,1,1,1]],
    "O": [[1,1],
          [1,1]],
    "T": [[0,1,0],
          [1,1,1]],
    "S": [[0,1,1],
          [1,1,0]],
    "Z": [[1,1,0],
          [0,1,1]],
    "J": [[1,0,0],
          [1,1,1]],
    "L": [[0,0,1],
          [1,1,1]],
}

if "grid" not in st.session_state:
    st.session_state.grid = [[0]*WIDTH for _ in range(HEIGHT)]

if "current_shape" not in st.session_state:
    st.session_state.current_shape = None
if "current_pos" not in st.session_state:
    st.session_state.current_pos = [WIDTH//2 - 1, 0]
if "score" not in st.session_state:
    st.session_state.score = 0
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()

def new_block():
    shape_key = random.choice(list(TETRIS_SHAPES.keys()))
    st.session_state.current_shape = TETRIS_SHAPES[shape_key]
    st.session_state.current_pos = [WIDTH // 2 - len(st.session_state.current_shape[0]) // 2, 0]

def can_move(dx, dy):
    shape = st.session_state.current_shape
    pos_x, pos_y = st.session_state.current_pos
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = pos_x + x + dx, pos_y + y + dy
                if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                    return False
                if ny >= 0 and st.session_state.grid[ny][nx]:
                    return False
    return True

def fix_block():
    shape = st.session_state.current_shape
    pos_x, pos_y = st.session_state.current_pos
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = pos_x + x, pos_y + y
                if ny >= 0:
                    st.session_state.grid[ny][nx] = 1
    clear_lines()
    new_block()
    if not can_move(0, 0):
        st.warning(f"게임 종료! 점수: {st.session_state.score}")
        st.stop()

def clear_lines():
    new_grid = [row for row in st.session_state.grid if any(cell == 0 for cell in row)]
    cleared = HEIGHT - len(new_grid)
    if cleared > 0:
        for _ in range(cleared):
            new_grid.insert(0, [0]*WIDTH)
        st.session_state.grid = new_grid
        st.session_state.score += cleared

def draw_grid():
    shape = st.session_state.current_shape
    pos_x, pos_y = st.session_state.current_pos
    for y in range(HEIGHT):
        row_str = ""
        for x in range(WIDTH):
            draw_cell = False
            if shape:
                rel_x = x - pos_x
                rel_y = y - pos_y
                if 0 <= rel_y < len(shape) and 0 <= rel_x < len(shape[0]):
                    if shape[rel_y][rel_x]:
                        draw_cell = True
            if draw_cell:
                row_str += "🟦"
            elif st.session_state.grid[y][x]:
                row_str += "🟥"
            else:
                row_str += "⬜"
        st.write(row_str)

if st.session_state.current_shape is None:
    new_block()

col1, col2 = st.columns(2)
left_btn = col1.button("⬅️ 왼쪽")
right_btn = col2.button("➡️ 오른쪽")

if left_btn and can_move(-1, 0):
    st.session_state.current_pos[0] -= 1
elif right_btn and can_move(1, 0):
    st.session_state.current_pos[0] += 1

# 1초마다 자동으로 블록이 아래로 떨어지게 하기
current_time = time.time()
if current_time - st.session_state.last_time > 1:
    st.session_state.last_time = current_time
    if can_move(0, 1):
        st.session_state.current_pos[1] += 1
    else:
        fix_block()
    st.experimental_rerun()  # 페이지 다시 실행 (자동 새로고침)

draw_grid()
st.write(f"점수: {st.session_state.score}")


streamlit-autorefresh


