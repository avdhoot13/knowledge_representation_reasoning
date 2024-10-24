import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

ALIVE = 1
DEAD = 0
AGAIN_COME_ALIVE = 2
states = [ALIVE, DEAD, AGAIN_COME_ALIVE]



def randomGrid(N):
    print("#################################### Random grid #######################################")
    # return np.random.choice(states, N*N, p=[0.2, 0.7, 0.1]).reshape(N, N)
    grid = np.zeros((N, N), dtype=[('state', np.int8), ('generation', np.int32)])
    states = np.random.choice([ALIVE, DEAD, AGAIN_COME_ALIVE], N*N, p=[0.2, 0.7, 0.1]).reshape(N, N)
    grid['state'] = states
    grid['generation'][grid['state'] == ALIVE] = 1
    return grid



def count_neighbors(grid, i, j, N):
    count = 0
    for x in range(max(0, i-1), min(N, i+2)):
        for y in range(max(0, j-1), min(N, j+2)):
            if (x != i or y != j) and grid[x, y]['state'] == ALIVE:
                count += 1
    return count



def update_grid(grid):
    new_grid = grid.copy()
    N = grid.shape[0]
    total_generation = 0

    for i in range(N):
        for j in range(N):
            alive_neighbors = count_neighbors(grid, i, j, N)
            # Apply rules based on the current state
            if grid[i, j]['state'] == ALIVE:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[i, j]['state'] = DEAD
                    new_grid[i, j]['generation'] = 0
                else:
                    new_grid[i, j]['generation'] += 1
            elif grid[i, j]['state'] == DEAD:
                if alive_neighbors == 3:
                    new_grid[i, j]['state'] = ALIVE
                    new_grid[i, j]['generation'] = 1
                    total_generation += 1
            elif grid[i, j]['state'] == AGAIN_COME_ALIVE:
                if 2 <= alive_neighbors <= 3:
                    new_grid[i, j]['state'] = ALIVE
                    new_grid[i, j]['generation'] = 1
                    total_generation += 1

    return new_grid, total_generation



def count_states(grid):
    alive = np.sum(grid['state'] == ALIVE)
    dead = np.sum(grid['state'] == DEAD)
    again_come_alive = np.sum(grid['state'] == AGAIN_COME_ALIVE)
    
    return alive, again_come_alive, dead



def start(event):
    global anim_running
    anim.event_source.start()
    anim_running = True

def stop(event):
    global anim_running
    anim.event_source.stop()
    anim_running = False

def exit(event):
    plt.close()




def update(frame, img, grid, N, status_text):
    print("--------------------------------- inside update function ------------------------------------------")
    print("--------------------------------- grid ------------------------------------------", grid)
    new_grid, total_generation = update_grid(grid)
    
    print("----------------------------------------- new grid ----------------------------------------------", new_grid)

    img.set_data(new_grid['state'])
    grid[:] = new_grid[:]
    
    alive, again_come_alive, dead = count_states(grid)
    status_text.set_text(f"Alive: {alive}, Dead: {dead}, Again Come Alive: {again_come_alive}, Total Generation: {total_generation}")
    return img,

N = 200
grid = randomGrid(N)

fig, ax = plt.subplots(figsize=(12, 8))
img = ax.imshow(grid['state'], cmap='viridis', interpolation='nearest')
ax.set_xticks([])
ax.set_yticks([])


status_text = ax.text(0.02, 1.02, "", transform=ax.transAxes)

start_button_ax = plt.axes([0.32, 0.02, 0.1, 0.075])
stop_button_ax = plt.axes([0.466, 0.02, 0.1, 0.075])
exit_button_ax = plt.axes([0.61, 0.02, 0.1, 0.075])

start_button = Button(start_button_ax, 'Start')
stop_button = Button(stop_button_ax, 'Pause')
exit_button = Button(exit_button_ax, 'Exit')

start_button.on_clicked(start)
stop_button.on_clicked(stop)
exit_button.on_clicked(exit)

print("################################# 3 ##########################################")

# Create the animation
anim_running = True
anim = animation.FuncAnimation(fig, update, fargs=(img, grid, N, status_text), frames=200, interval=50)

plt.show()
