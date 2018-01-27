from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk

def P_select():
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)

    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)

    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)

    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    
    P_list = []
    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        print (event.x,event.y)
        coord = event.x,event.y
        P_list.append(coord)
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()
    return P_list



def get_line(start, end):
    global nodes
    global true_points
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    start 
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    px_sum = 0
    n_px = 0
    im = Image.open('road_0.jpg')
    px = im.load()

    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)

        px_sum = px[coord][0] + px_sum
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

        n_px = n_px + 1
    
    px_avg = px_sum / n_px
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    if px_avg > 200:
        nodes.append((start, end))
        for n in range(len(points)):
            true_points.append(points[n])
    # return points

if __name__ == "__main__":
    nodes = []
    true_points = []
    P_list = P_select()
    LEN = len(P_list)
    for j in range(LEN):
        for k in range(LEN):
            if k != j:
                get_line(P_list[j], P_list[k])
    # LEN = len(points)
    # print(true_points)
    print(nodes)
    im = Image.open('road_0.jpg')
    px = im.load()
    for i in range(len(true_points)):
        px[true_points[i]] = (255,0,0)
    im.show()