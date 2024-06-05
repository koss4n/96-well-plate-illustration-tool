#Main application file
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkColorPicker import *

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
letters_list:list[str] = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P"]
grid_size_list:list[str] = ["96"]
global rectx1, recty1, rectyx2, recty2, non_circle_items
non_circle_items:int
rectx1, recty1, rectyx2, recty2, non_circle_items = 0,0,0,0,0
class App(ctk.CTk):
  def __init__(self):
      super().__init__()
      self.color = "white"
      self.circle_type_list =[]
      self.title("Well Template.py")
      self.geometry(f"{1600}x{900}")
      # configure grid layout (2x2)
      self.grid_columnconfigure(2, weight=1)
      self.grid_rowconfigure((0, 1), weight=1)
      
      self.radio_var = ctk.StringVar(value="other") 
      
      self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
      self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
      self.sidebar_frame.grid_rowconfigure(4, weight=1)
      
      #Logo for app
      self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Well Template App", font=ctk.CTkFont(size=20, weight="bold"))
      self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
      
      self.choose_grid_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=grid_size_list,
                                              command = self.create_well_grid_event)
      self.choose_grid_optionmenu.set("")
      self.choose_grid_optionmenu.grid(row=1,column=0,padx=20,pady=20)
      
      #Button to create circle type
      self.create_circle_type = ctk.CTkButton(self.sidebar_frame, text = "Create Circle Type",
                                              command = self.ask_color)
      self.create_circle_type.grid(row=2, column = 0, padx = 20, pady=(40,0))
    
      #Scroll frame with circle types
      
      self.scroll_frame_circles = ctk.CTkScrollableFrame(self, width = 200)
      self.scroll_frame_circles.grid(row=0,column=1, sticky="ns", padx=(20,0),pady=(40,0)) 
      #Canvas GUI
      self.canvas = ctk.CTkCanvas(master=self, width = 900, height = 800, highlightcolor="blue")
      self.canvas.grid(row=0,column=2, pady=(50))
      
      
      
      self.canvas.bind("<Button-1>", self.callback)
      self.canvas.bind("<B1-Motion>", self.drag)
      self.canvas.bind("<B1-ButtonRelease>", self.release)
        
          
          
      
      
      self.canvas_under_frame = ctk.CTkFrame(self, width=900,height=200)
      self.canvas_under_frame.grid(row=1,column=2)
      self.rect_id = self.canvas.create_rectangle(0,0,0,0,dash=(2,2),fill='',outline='black')
    
  def create_well_grid_event(self, grid_size:str):
    
    if grid_size == "96":
      self.create_canvas(space=70, radius=30,rows=8,cols=12)
    
  #Creates a canvas from the specified values
  def create_canvas(self, space:int, radius:int, rows:int, cols:int):
    #Updates the values of non circle items
    global non_circle_items
    non_circle_items = rows + cols + 1
    #Algorithm creates letters/num seperately from circles to be easier identify which itemIDs belong to circles
    i = space
    for i in range(rows):
      self.canvas.create_text(15,space*(i+1),text=letters_list[i], fill="black", font=('Helvetica 15'), tags = "letter")
      
    for i in range(cols):
      self.canvas.create_text(space*(i+1),15,text=i+1, fill="black", font=('Helvetica 15'), tags = "num")
    
    for i in range (cols):
      for j in range(rows):
        self.canvas.create_aa_circle(x_pos=space*(i+1),y_pos=space*(j+1),radius=radius+2,fill="black")
        self.canvas.create_aa_circle(x_pos=space*(i+1),y_pos=space*(j+1),radius=radius,fill="white")
        
    
    
  #Test

  def release(self,event):
    global rectx1, recty1, rectx2, recty2
    print("released at", event.x, event.y)
    
    self.canvas.coords(self.rect_id,0,0,0,0)
    a= self.canvas.find_overlapping(rectx1,recty1,rectx2,recty2)
    #Ignores items that aren't inner circle
    for item in a:
      if item > non_circle_items and item%2==1:
        print(item) 
        self.canvas.itemconfig(item,fill=self.color)
  
    
    
  def drag(self,event):
    global rectx2, recty2
    rectx2, recty2 = event.x,event.y
    self.canvas.coords(self.rect_id,rectx1,recty1,rectx2,recty2)
    
  def callback(self,event):
    global rectx1, recty1,rectx2,recty2
    print("clicked at", event.x,event.y)
    rectx1, rectx2 = event.x, event.x
    recty1,recty2= event.y,event.y
  
  def ask_color(self):
    pick_color = AskColor() # open the color picker
    color = pick_color.get() # get the color string
    self.circle_type_list.append(color)
    
    def change_color():
      self.color = color
      
     
    circle_button = ctk.CTkRadioButton(self.scroll_frame_circles, border_color =color, text=color, variable=self.radio_var, 
                                       command = change_color)
    circle_button.grid(row=len(self.circle_type_list),column=0,padx=20,pady=20, sticky="w")
if __name__ == "__main__":
    app = App()
    app.mainloop()  
