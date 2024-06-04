#Main application file
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
letters_96size:list[str] = ["A","B","C","D","E","F","G","H"]
grid_size_list:list[str] = ["96"]
global rectx1, recty1, rectyx2, recty2
class App(ctk.CTk):
  def __init__(self):
      super().__init__()
      self.title("Well Template.py")
      self.geometry(f"{1600}x{900}")
      # configure grid layout (2x2)
      self.grid_columnconfigure(1, weight=1)
      self.grid_rowconfigure((0, 1), weight=1)
      
      self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
      self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
      self.sidebar_frame.grid_rowconfigure(4, weight=1)
      
      #Logo for app
      self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Well Template App", font=ctk.CTkFont(size=20, weight="bold"))
      self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
      
      self.generate_well_grid = ctk.CTkOptionMenu(self.sidebar_frame, values=grid_size_list,
                                              command = self.create_well_grid_event)
      self.generate_well_grid.grid(row=1,column=0,padx=20,pady=20)
      self.canvas = ctk.CTkCanvas(master=self, width = 900, height = 800, highlightcolor="blue")
      self.canvas.grid(row=0,column=1, pady=(50))
      
      
      
      self.canvas.bind("<Button-1>", self.callback)
      self.canvas.bind("<B1-Motion>", self.drag)
      self.canvas.bind("<B1-ButtonRelease>", self.release)
        
          
          
        
      
      
  
    
      
      
      self.canvas_under_frame = ctk.CTkFrame(self, width=200,height=200)
      self.canvas_under_frame.grid(row=1,column=1)
      self.rect_id = self.canvas.create_rectangle(0,0,0,0,dash=(2,2),fill='',outline='black')
    
  def create_well_grid_event(self, grid_size:str):
    
    if grid_size == "96":
      self.create_canvas(space=70)
    
  def create_canvas(self, space:int):
    
    i = space
    for letter in letters_96size:
      for j in range(12):
        self.canvas.create_aa_circle(x_pos=space*(j+1),y_pos=i,radius=32,fill="black")
        self.canvas.create_aa_circle(x_pos=space*(j+1),y_pos=i,radius=30,fill="white")
      self.canvas.create_text(15,i,text=letter, fill="black", font=('Helvetica 15'), tags = "letter")
      i+=space
      
    for i in range(12):
      self.canvas.create_text(space*(i+1),15,text=i+1, fill="black", font=('Helvetica 15'), tags = "num")
    
  #Test

  def release(self,event):
    global rectx1, recty1, rectx2, recty2
    print("released at", event.x, event.y)
    self.canvas.coords(self.rect_id,0,0,0,0)
    a= self.canvas.find_overlapping(rectx1,recty1,rectx2,recty2)
    for item in a:
      
      print(item) 
      self.canvas.itemconfig(item,fill="red")
  
    
    
  def drag(self,event):
    global rectx2, recty2
    rectx2, recty2 = event.x,event.y
    self.canvas.coords(self.rect_id,rectx1,recty1,rectx2,recty2)
    
  def callback(self,event):
    global rectx1, recty1
    print("clicked at", event.x,event.y)
    rectx1 = event.x
    recty1= event.y
  
      
    
if __name__ == "__main__":
    app = App()
    app.mainloop()  
