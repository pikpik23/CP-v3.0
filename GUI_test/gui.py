from tkinter import *
from PIL import ImageTk, Image
from time import sleep
from threading import Thread

class gui():

    def __init__(self):
        self.root = Tk()
        self.root.title("Command Post V3.0")
        self.root.geometry("249x324+300+150")
        self.root.resizable(width=False, height=False)

        #Generate Frame
        self.gen_frame()


    def button_press(self):
        print("closing")
        self.root.destroy()

    def ready(self):
        # rezie to fix button glitch
        self.root.geometry("250x325+300+150")

    def gen_frame(self):
        #IMAGE FRAME
        img = Image.open("CPL.gif")
        img = img.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.root, image=img)
        panel.image = img
        panel.pack(pady=20)

        #Status label
        status_text = Label(self.root)
        status_text['text'] = "Starting Up"

        #Exit Button
        button = Button(self.root, text=" STOP SERVER ", command=self.button_press)

        status_text.pack(pady=10)
        button.pack(pady=0)

        self.root.wait_visibility()

        self.root.after_idle(self.ready)

        # start the event loop
        self.root.mainloop()

def start_server():
    while True:
        sleep(1)
        print("Hi")

if __name__ == "__main__":
    thr = Thread(target=start_server)
    thr.setDaemon(True)
    thr.start()

    print("threaded")
    x = gui()
