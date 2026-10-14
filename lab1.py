import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class LabWorkApp30:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторна робота №1 - Варіант 30 (Computer Vision)")
        self.root.geometry("1050x720")

        self.root.protocol("WM_DELETE_WINDOW", self._quit)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(11, 5.5))
        
        self.ax1.set_title("2D", fontsize=10)
        self.ax1.set_xlim(-12, 12)
        self.ax1.set_ylim(-12, 12)
        self.ax1.grid(True)
        
        self.square_line, = self.ax1.plot([], [], 'b-', lw=2, label="Квадрат")
        self.trajectory_line, = self.ax1.plot([], [], 'r--', lw=1.5, label="Траєкторія руху")
        self.traj_x, self.traj_y = [], []
        self.ax1.legend(loc='upper right', fontsize=8)

        self.ax2.set_title("3D", fontsize=10)
        self.ax2.set_xlim(-8, 8)
        self.ax2.set_ylim(-8, 8)
        self.ax2.grid(True)

        self.cube_3d = np.array([
            [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
            [-1, -1,  1, 1], [1, -1,  1, 1], [1,  1,  1, 1], [-1,  1,  1, 1]
        ]).T

        self.edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        self.cube_lines = [self.ax2.plot([], [], 'g-', lw=2)[0] for _ in self.edges]

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.btn_quit = tk.Button(master=self.root, text="Закрити програму", command=self._quit, bg="#d9534f", fg="white", font=("Arial", 11, "bold"))
        self.btn_quit.pack(side=tk.BOTTOM, pady=10)

        self.anim = FuncAnimation(self.fig, self.update_animation, frames=120, interval=60, blit=False)

    def update_animation(self, frame):
        try:
            angle1 = np.radians(frame * 3)
            angle2 = np.radians(-frame * 4)  
            tx = 4 * np.sin(np.radians(frame * 3))
            ty = 4 * np.cos(np.radians(frame * 4))

            T = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
            R1 = np.array([[np.cos(angle1), -np.sin(angle1), 0], [np.sin(angle1), np.cos(angle1), 0], [0, 0, 1]])
            R2 = np.array([[np.cos(angle2), -np.sin(angle2), 0], [np.sin(angle2), np.cos(angle2), 0], [0, 0, 1]])

            M_comp = T @ R1 @ R2
            
            base_sq = np.array([
                [-1.5, 1.5, 1.5, -1.5],
                [-1.5, -1.5, 1.5, 1.5]
            ])
            transformed_sq = (M_comp @ np.vstack((base_sq, np.ones(4))))[:2, :]
            
            x_pts = np.append(transformed_sq[0, :], transformed_sq[0, 0])
            y_pts = np.append(transformed_sq[1, :], transformed_sq[1, 0])
            self.square_line.set_data(x_pts, y_pts)

            cx, cy = np.mean(transformed_sq[0, :]), np.mean(transformed_sq[1, :])
            self.traj_x.append(cx)
            self.traj_y.append(cy)
            if len(self.traj_x) > 100:  
                self.traj_x.pop(0)
                self.traj_y.pop(0)
            self.trajectory_line.set_data(self.traj_x, self.traj_y)

            theta = np.radians(frame * 4)
            Rx = np.array([[1, 0, 0, 0], [0, np.cos(theta), -np.sin(theta), 0], [0, np.sin(theta), np.cos(theta), 0], [0, 0, 0, 1]])
            Ry = np.array([[np.cos(theta), 0, np.sin(theta), 0], [0, 1, 0, 0], [-np.sin(theta), 0, np.cos(theta), 0], [0, 0, 0, 1]])

            shift_x = 2.5 * np.cos(np.radians(frame * 2))
            shift_y = 2.5 * np.sin(np.radians(frame * 2.5))
            
            rotated_cube = Ry @ Rx @ self.cube_3d
            projected_cube = rotated_cube[:2, :]
            projected_cube[0, :] += shift_x
            projected_cube[1, :] += shift_y

            for idx, (i, j) in enumerate(self.edges):
                self.cube_lines[idx].set_data(
                    [projected_cube[0, i], projected_cube[0, j]],
                    [projected_cube[1, i], projected_cube[1, j]]
                )

            alpha_val = 0.2 + 0.8 * abs(np.sin(np.radians(frame * 5)))
            for line in self.cube_lines:
                line.set_alpha(alpha_val)

        except Exception as e:
            print(f"Помилка при оновленні анімації: {e}")

        return self.square_line, self.trajectory_line

    def _quit(self):
        try:
            self.anim.event_source.stop()
            plt.close(self.fig)
        except Exception:
            pass
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = LabWorkApp30(root)
    root.mainloop()