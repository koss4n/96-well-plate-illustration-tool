#Main application file
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
  def __init__(self):
      super().__init__()
      self.title("Randomizer App.py")
      self.geometry(f"{1000}x{1000}")
      # configure grid layout (2x2)
      self.grid_columnconfigure(1, weight=1)
      self.grid_rowconfigure((0, 1), weight=1)
      
      self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
      self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
      self.sidebar_frame.grid_rowconfigure(4, weight=1)
      
      #Logo for app
      self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Randomizer App", font=ctk.CTkFont(size=20, weight="bold"))
      self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
      
      self.generate_well_grid = ctk.CTkButton(self.sidebar_frame, text="Gen Grid",
                                              command = self.create_well_grid_event)
      self.generate_well_grid.grid(row=1,column=0,padx=20,pady=20)
      self.canvas = ctk.CTkCanvas(master=self, width = 650, height = 450, highlightcolor="blue")
      self.canvas.grid(row=0,column=1, pady=(50))
      self.canvas.create_aa_circle(x_pos=50,y_pos=50,radius=20,fill="blue")
      self.canvas.create_aa_circle(x_pos=100,y_pos=50,radius=20,fill="blue")
      self.canvas.create_aa_circle(x_pos=600,y_pos=50,radius=20,fill="blue")
      self.canvas.create_aa_circle(x_pos=50,y_pos=400,radius=20,fill="blue")
      
      self.canvas.scan
      
      print(self.canvas.grid_bbox(column=1,row=2))
      
      
      self.canvas_under_frame = ctk.CTkFrame(self, width=200,height=200)
      self.canvas_under_frame.grid(row=1,column=1)
     
    
  def create_well_grid_event(self):
    
    coordinates = ctk.CTkInputDialog(text="only int")
    intg = coordinates.get_input().split(',')
    x = int(intg[0])
    y=int(intg[1]) 
    ar = np.zeros(shape=(x,y))
    
    print(ar)
    
if __name__ == "__main__":
    app = App()
    app.mainloop()  
