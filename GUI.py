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
      self.circle_radio_list ={}
      self.circle_color_map ={}
      self.canvas_items_map = {}
      self.title("Well Template.py")
      self.geometry(f"{1600}x{900}")
      # configure grid layout (2x2)
      self.grid_columnconfigure(2, weight=1)
      self.grid_rowconfigure((0, 1), weight=1)
      
      self.radio_var = ctk.StringVar(value="other") 
      
      self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
      self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
      self.sidebar_frame.grid_rowconfigure(6, weight=1)
      
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
      
      #Button for adding name to circle type
      self.change_name_circle = ctk.CTkButton(self.sidebar_frame, text = "Change Name Circle", state='disabled',
                                              command = self.add_name_radiobutton)
      self.change_name_circle.grid(row=3, column = 0, padx = 20, pady=(40,0))
      
      self.add_text_button = ctk.CTkButton(self.sidebar_frame, text = "Add Text",
                                              command = self.add_text_to_circletype)
      self.add_text_button.grid(row=4, column = 0, padx = 20, pady=(40,0))
      
      self.remove_text_button = ctk.CTkButton(self.sidebar_frame, text = "Remove Text",
                                              command = self.remove_text_for_circles)
      self.remove_text_button.grid(row=5, column = 0, padx = 20, pady=(200,0))
      
      #Scroll frame with circle types
      
      self.scroll_frame_circles = ctk.CTkScrollableFrame(self, width = 200)
      self.scroll_frame_circles.grid(row=0,column=1, sticky="ns", padx=(20,0),pady=(40,0)) 
      def color_white():
        self.color = "white"
      circle_button = ctk.CTkRadioButton(self.scroll_frame_circles, border_color ="white", border_width_checked=11, fg_color="white",
                                       variable=self.radio_var, text="Default",
                                       command = color_white)
      circle_button.grid(row=len(self.circle_radio_list),column=0,padx=20,pady=20, sticky="w")
      self.circle_radio_list["white"] = circle_button
      #Canvas GUI
      self.canvas = ctk.CTkCanvas(master=self, width = 900, height = 800, highlightcolor="blue")
      self.canvas.grid(row=0,column=2, pady=(50))
      
      
      
      self.canvas.bind("<Control-Button-1>", self.callback)
      self.canvas.bind("<Control-B1-Motion>", self.drag)
      self.canvas.bind("<Control-B1-ButtonRelease>", self.release)
      self.canvas.bind("<Shift-B1-ButtonRelease>", self.add_text_selected_items)
      self.canvas.bind("<Shift-B1-Motion>", self.drag)
      self.canvas.bind("<Shift-Button-1>", self.callback)
          
          
      
      
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
        x = space*(i+1), 
        y = space*(j+1)
        self.canvas.create_aa_circle(x,y,radius=radius+2,fill="black")
        id = self.canvas.create_aa_circle(x,y,radius=radius,fill="white")
        coords_circle = x,y
        self.canvas_items_map[id] = coords_circle
        
    print(self.canvas_items_map[27])    
    
    
  
  #Manipulates all circles overlapping with click-drag rectangle
  def release(self,event):
    global rectx1, recty1, rectx2, recty2
    print("released at", event.x, event.y)
    
    self.canvas.coords(self.rect_id,0,0,0,0)
    a= self.canvas.find_overlapping(rectx1,recty1,rectx2,recty2)
    #Ignores items that aren't inner circle
    item_list = []
    for item in a:
      if item > non_circle_items and item%2==1:
        item_list.append(item)
        self.canvas.itemconfig(item,fill=self.color, tags=self.color)
        
        #self.canvas.create_text(self.canvas_items_map[item],text="Test", tags = "text-item")
    self.circle_color_map[self.color] = item_list
        
  
    
    
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
    
    def change_color():
      self.color = color
      self.change_name_circle.configure(state='normal')
     
    circle_button = ctk.CTkRadioButton(self.scroll_frame_circles, border_color =color,border_width_checked=11,
                                       variable=self.radio_var, text="", fg_color= color,
                                       command = change_color)
    circle_button.grid(row=len(self.circle_radio_list),column=0,padx=20,pady=20, sticky="w")
    self.circle_radio_list[color] = circle_button
    
  def add_name_radiobutton(self):
    if self.color != "white":
      input_name = ctk.CTkInputDialog(text="Write Circle Name",title="Circle Name")
      name = input_name.get_input()
      self.circle_radio_list[self.color].configure(text=name)
    
  def add_text_to_circletype(self):
    input_text = ctk.CTkInputDialog(text="Write Text",title="Add Text")
    text = input_text.get_input()
    colored_items = self.circle_color_map[self.color]    
    for item in colored_items:
      coords_ = self.canvas_items_map[item]
      self.canvas.create_text(coords_, text=text, tags=text)
    
  def remove_text_for_circles(self):
    self.canvas.itemconfigure(self.color,fill=self.color)
  
  def add_text_selected_items(self,event):
    global rectx1, recty1, rectx2, recty2
    print("released at", event.x, event.y)
    
    self.canvas.coords(self.rect_id,0,0,0,0)
    input_text = ctk.CTkInputDialog(text="Write Text",title="Add Text")
    text = input_text.get_input()
    a= self.canvas.find_overlapping(rectx1,recty1,rectx2,recty2)
    #Ignores items that aren't inner circle
    for item in a:
      if item > non_circle_items and item%2==1: 
        coords_ = self.canvas_items_map[item]
        self.canvas.create_text(coords_, text=text, tags=text)
        #self.canvas.create_text(self.canvas_items_map[item],text="Test", tags = "text-item")
    
    
    
if __name__ == "__main__":
    app = App()
    app.mainloop()  
