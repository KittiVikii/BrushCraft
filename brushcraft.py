from tkinter import *
from tkinter import colorchooser, filedialog
from PIL import ImageGrab


class BrushCraft:
    def __init__(self, master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 1
        self.drawWidgets()

        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        self.undo_list = []

    # painting method
    def paint(self, e):
        if self.old_x and self.old_y:
            line = self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth, fill=self.color_fg,
                                      capstyle='round', smooth=True)
            self.undo_list.append(line)

        self.old_x = e.x
        self.old_y = e.y

    def use_brush(self):
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    # eraser method
    def erase(self, e):
        if self.old_x and self.old_y:
            line = self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth, fill=self.color_bg,
                                        capstyle=ROUND, smooth=True)
            self.undo_list.append(line)

        self.old_x = e.x
        self.old_y = e.y

    def use_eraser(self):
        self.c.bind('<B1-Motion>', self.erase)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.color_fg = self.color_bg  # Assign the current background color to `self.color_fg`

    # resetting or cleaning the canvas
    def reset(self, e):
        self.old_x = None
        self.old_y = None

    # changing the pen width
    def changeW(self, e):
        self.penwidth = e

    # clearing canvas
    def clear(self):
        self.c.delete(ALL)

    # changing pen color
    def change_fg(self):
        self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]

    # background changing
    def change_bg(self):
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

    # undo method
    def undo(self):
        if self.undo_list:
            line_id = self.undo_list.pop()
            self.c.delete(line_id)

    # cube brush method
    def use_cube(self):
        self.c.bind('<B1-Motion>', self.draw_cube)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def draw_cube(self, e):
        if self.old_x and self.old_y:
            cube = self.c.create_rectangle(self.old_x, self.old_y, e.x, e.y, outline=self.color_fg,
                                           width=self.penwidth)
            self.undo_list.append(cube)

        self.old_x = e.x
        self.old_y = e.y

    # circle brush method
    def use_circle(self):
        self.c.bind('<B1-Motion>', self.draw_circle)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def draw_circle(self, e):
        if self.old_x and self.old_y:
            radius = max(abs(e.x - self.old_x), abs(e.y - self.old_y))
            circle = self.c.create_oval(self.old_x - radius, self.old_y - radius, self.old_x + radius,
                                        self.old_y + radius,
                                        outline=self.color_fg, width=self.penwidth)
            self.undo_list.append(circle)

        self.old_x = e.x
        self.old_y = e.y

    # saving as file
    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png')])
        if file_path:
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()
            image = ImageGrab.grab((x, y, x1, y1))
            image.save(file_path)
            print("Image saved as PNG:", file_path)

    def save_canvas_jpg(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[('JPEG Files', '*.jpg')])
        if file_path:
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()
            image = ImageGrab.grab((x, y, x1, y1))
            image.save(file_path, 'JPEG')
            print("Image saved as JPEG:", file_path)

    def drawWidgets(self):
        self.controls = Frame(self.master, padx=5, pady=5, bg="#ffffff")
        self.controls.pack(side=LEFT, padx=10, pady=10)

        # adding pen width slider
        Label(self.controls, text='Pen Width:', font=('Verdana', 18)).grid(row=0, column=0, sticky=W)
        self.slider = Scale(self.controls, from_=1, to=100, command=self.changeW, orient=VERTICAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0, column=1, ipadx=30)

        #adding brush button
        self.brush_button = Button(self.controls, text="Brush", command=self.use_brush, relief=RAISED, bg="#e0e0e0",
                                   activebackground="#d6d6d6", font=('Arial', 12))
        self.brush_button.grid(row=1, column=0, pady=5)

        #adding eraser button
        self.eraser_button = Button(self.controls, text="Eraser", command=self.use_eraser, relief=RAISED, bg="#e0e0e0",
                                    activebackground="#d6d6d6", font=('Arial', 12))
        self.eraser_button.grid(row=1, column=1, pady=5)

        #adding undo button
        self.undo_button = Button(self.controls, text="Undo", command=self.undo, relief=RAISED, bg="#e0e0e0",
                                  activebackground="#d6d6d6", font=('Arial', 12))
        self.undo_button.grid(row=2, column=0, pady=5)

        # adding cube brush button
        self.cube_button = Button(self.controls, text="Cube", command=self.use_cube, relief=RAISED, bg="#e0e0e0",
                                  activebackground="#d6d6d6", font=('Arial', 12))
        self.cube_button.grid(row=3, column=0, pady=5)

        # adding circle brush button
        self.circle_button = Button(self.controls, text="Circle", command=self.use_circle, relief=RAISED, bg="#e0e0e0",
                                    activebackground="#d6d6d6", font=('Arial', 12))
        self.circle_button.grid(row=3, column=1, pady=5)

        self.c = Canvas(self.master, width=500, height=400, bg=self.color_bg)
        self.c.pack(fill=BOTH, expand=True)

        # adding menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        self.master.configure(bg="#f2f2f2")
        menu.configure(bg="#ffffff", fg="#333333")
        menu.configure(font=('Verdana', 12, 'bold'))

        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Save as PNG', command=self.save_canvas, compound=LEFT)
        filemenu.add_command(label='Save as JPG', command=self.save_canvas_jpg,
                             compound=LEFT)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.master.destroy, compound=LEFT)
        filemenu.configure(bg="#ffffff", fg="#333333")
        filemenu.configure(font=('Verdana', 10))

        colormenu = Menu(menu)
        menu.add_cascade(label='Colors', menu=colormenu)
        colormenu.add_command(label='Brush Color', command=self.change_fg)
        colormenu.add_command(label='Background Color', command=self.change_bg)
        colormenu.configure(bg="#ffffff", fg="#333333")
        colormenu.configure(font=('Verdana', 10))

        optionmenu = Menu(menu)
        menu.add_cascade(label='Options', menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas', command=self.clear)
        optionmenu.configure(bg="#ffffff", fg="#333333")
        optionmenu.configure(font=('Verdana', 10))


if __name__ == '__main__':
    root = Tk()
    BrushCraft(root)
    root.title('BrushCraft')
    root.option_add('*Font', 'Verdana 14 bold')
    root.mainloop()
