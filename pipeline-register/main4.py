import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import time
import random

# Define pipeline stages
pipeline_stages = ["Fetch", "Decode", "Execute", "Memory", "Write-back"]

# Number of instructions to simulate
# num_instructions = 6
num_instructions = random.randint(1, 10)

# Create a 2D array to simulate the pipeline process
num_cycles = len(pipeline_stages) + num_instructions - 1
pipeline = [["" for _ in range(num_cycles)] for _ in range(num_instructions)]

# Populate the pipeline simulation
for i in range(num_instructions):
    for j in range(len(pipeline_stages)):
        if i + j < len(pipeline[0]):
            pipeline[i][i + j] = pipeline_stages[j]

# Colors for active and inactive cells
active_color = "lightblue"
inactive_color = "white"

# Initialize figure and axes
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title("Pipeline Simulation (Animated)", fontsize=14)
ax.set_xlabel("Cycles", fontsize=12)
ax.set_ylabel("Instructions", fontsize=12)

# Draw grid and initialize text elements
rectangles = []
text_elements = []
# for i in range(num_instructions):
#     row_rects = []
#     row_texts = []
#     for j in range(num_cycles):
#         # Draw grid cell
#         rect = plt.Rectangle((j - 0.5, num_instructions - i - 1.5), 1, 1, edgecolor="black", facecolor=inactive_color)
#         ax.add_patch(rect)
#         row_rects.append(rect)

#         # Add text
#         text = ax.text(j, num_instructions - i - 1, "", ha="center", va="center", fontsize=8)
#         row_texts.append(text)
#     rectangles.append(row_rects)
#     text_elements.append(row_texts)
for i in range(num_instructions):
    row_rects = []
    row_texts = []
    for j in range(num_cycles):
        # Adjust vertical placement to match "top-to-bottom" instruction order
        rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor="black", facecolor=inactive_color)
        ax.add_patch(rect)
        row_rects.append(rect)

        # Add text
        text = ax.text(j, i, "", ha="center", va="center", fontsize=8)
        row_texts.append(text)
    rectangles.append(row_rects)
    text_elements.append(row_texts)

# Set axis limits and labels
ax.set_xlim(-0.5, num_cycles - 0.5)
ax.set_ylim(-0.5, num_instructions - 0.5)
ax.set_xticks(range(num_cycles))
ax.set_xticklabels([f"Cycle {i + 1}" for i in range(num_cycles)])
ax.set_yticks(range(num_instructions))
ax.set_yticklabels([f"Instr {i + 1}" for i in range(num_instructions)])
plt.gca().invert_yaxis()

# Terminal display function
def display_terminal(frame):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
    print(f"Cycle {frame + 1}/{num_cycles}")
    print("-" * (num_cycles * 10))
    for i in range(num_instructions):
        row = [" " * 10 for _ in range(num_cycles)]
        for j in range(num_cycles):
            if pipeline[i][j] != "" and j <= frame:
                row[j] = pipeline[i][j].center(10)
        print(" | ".join(row))
    print("-" * (num_cycles * 10))

# Update function for animation
def update(frame):
    display_terminal(frame)  # Update terminal display
    for i in range(num_instructions):
        for j in range(num_cycles):
            # Update cell color and text
            if j == frame and pipeline[i][j] != "":
                rectangles[i][j].set_facecolor(active_color)
                text_elements[i][j].set_text(pipeline[i][j])
            elif pipeline[i][j] != "":
                rectangles[i][j].set_facecolor(inactive_color)
            else:
                text_elements[i][j].set_text("")
                rectangles[i][j].set_facecolor(inactive_color)
    return [item for sublist in rectangles for item in sublist] + [item for sublist in text_elements for item in sublist]

# Create animation
anim = FuncAnimation(fig, update, frames=num_cycles, interval=1000, blit=False)

plt.tight_layout()
plt.show()
