import controller
import math
import tkinter as tk
from tkinter import ttk

PI = 3.1415

# arm calc

window = tk.Tk()
window.geometry("400x400")

canvas = tk.Canvas(window, background="white", width=400, height=400)
canvas.place(x=0, y=0)


ctlr = controller.Arm3Joints(
    [100, 100, 50],
    [PI * 3 / 4, PI * 2 / 3, PI * 5 / 4],
)


def update(e):
    x = e.x - 100
    y = 400 - e.y - 100

    ctlr.set_tip_position((x, y))
    ctlr.set_tip_angle(0)
    print("status : ", ctlr.calculate())

    print(ctlr.joints_angle)

    arm_agl = [PI / 2]

    for d in ctlr.joints_angle:
        nxt_agl = arm_agl[-1] - PI + d
        arm_agl.append(nxt_agl)

    print(arm_agl)

    arm_vec = [(0, -30), (0, 0)]

    for a in range(1, len(arm_agl)):
        angle = arm_agl[a]
        length = ctlr.arms_length[a - 1]
        x = arm_vec[-1][0] + math.cos(angle) * length
        y = arm_vec[-1][1] + math.sin(angle) * length
        arm_vec.append((x, y))

    canvas.delete("all")

    for v in range(1, len(arm_vec)):
        base = arm_vec[v - 1]
        head = arm_vec[v]
        canvas.create_line(
            (base[0] + 100),
            400 - (base[1] + 100),
            (head[0] + 100),
            400 - (head[1] + 100),
        )


canvas.bind("<Motion>", update)
window.mainloop()
