# Main application file
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkColorPicker import *
from PIL import Image, ImageTk, ImageDraw

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
LETTER_LIST: list[str] = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
]
GRID_SIZE_LIST: list[str] = ["96"]
global rectx1, recty1, rectyx2, recty2, non_circle_items
non_circle_items: int
rectx1, recty1, rectyx2, recty2, non_circle_items = 0, 0, 0, 0, 0
FONT_LIST = ["Helvetica", "Sans", "System", "Terminal", "Ms", "Times"]
FONT_SIZE_LIST = [str(i) for i in range(1, 21)]
IMAGES = []


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.radius = 0
        self.color = "white"
        self.font = "Helvetica 15"
        self.circle_radio_list = {}
        # Color str: list[ids], smallest, largest
        self.circle_color_map = {}
        self.canvas_items_map = {}
        self.canvas_id_text_map = {}
        self.actions_stack = []
        self.item_changes_map = {}
        self.tab_map = {}
        self.tab_name_map = {}
        self.title("Well Template.py")
        self.geometry(f"{1600}x{900}")
        # configure grid layout (2x2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.radio_var = ctk.StringVar(value="other")

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Logo for app
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Well Template App",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.choose_grid_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=GRID_SIZE_LIST,
            command=self.create_well_grid_event,
        )
        self.choose_grid_optionmenu.set("")
        self.choose_grid_optionmenu.grid(row=1, column=0, padx=20, pady=20)

        # Button to create circle type
        self.create_circle_type = ctk.CTkButton(
            self.sidebar_frame, text="Create Circle Type", command=self.ask_color
        )
        self.create_circle_type.grid(row=2, column=0, padx=20, pady=(40, 0))

        # Button for adding name to circle type
        self.change_name_circle = ctk.CTkButton(
            self.sidebar_frame,
            text="Change Name Circle",
            state="disabled",
            command=self.add_name_radiobutton,
        )
        self.change_name_circle.grid(row=3, column=0, padx=20, pady=(40, 0))

        self.gradient_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Values Gradient",
            command=self.concentration_gradient,
        )
        self.gradient_button.grid(row=4, column=0, padx=20, pady=(40, 0))

        # Optionmenus for choosing text style
        self.font_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=FONT_LIST, command=self.change_font
        )
        self.font_optionmenu.set("Helvetica")
        self.font_optionmenu.grid(row=5, column=0, padx=(0, 55), pady=20)

        # Optionmenus for choosing text style
        self.font_size_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=FONT_SIZE_LIST,
            width=20,
            command=self.change_font,
        )
        self.font_size_optionmenu.set("15")
        self.font_size_optionmenu.grid(row=5, column=0, padx=(145, 0), pady=20)

        self.remove_text_button = ctk.CTkButton(
            self.sidebar_frame, text="Remove Text", command=self.lift
        )
        self.remove_text_button.grid(row=6, column=0, padx=20, pady=(200, 0))

        # Scroll frame with circle types

        self.scroll_frame_circles = ctk.CTkScrollableFrame(self, width=200)
        self.scroll_frame_circles.grid(
            row=0, column=1, sticky="ns", padx=(20, 0), pady=(40, 0)
        )

        def color_white():
            self.color = "white"

        circle_button = ctk.CTkRadioButton(
            self.scroll_frame_circles,
            border_color="white",
            border_width_checked=11,
            fg_color="white",
            variable=self.radio_var,
            text="Default",
            command=color_white,
        )
        circle_button.grid(
            row=len(self.circle_radio_list), column=0, padx=20, pady=20, sticky="w"
        )
        self.circle_radio_list["white"] = circle_button
        # Canvas GUI
        self.canvas = ctk.CTkCanvas(
            master=self, width=900, height=700, highlightcolor="blue"
        )
        self.canvas.grid(row=0, column=2, pady=(50))
        self.tab_name_map["Tab 1"] = self.canvas

        self.tab_button = ctk.CTkSegmentedButton(
            self,
            width=100,
            height=30,
            corner_radius=30,
            values=["Tab 1", "+"],
            command=self.new_tab,
        )
        self.tab_button.set("Tab 1")
        self.tab_button.grid(row=0, column=2, padx=(120, 0), pady=(20, 0), sticky="nw")

        self.canvas.bind_all("<Control-Button-1>", self.callback)
        self.canvas.bind_all("<Control-B1-Motion>", self.drag)
        self.canvas.bind_all("<Control-B1-ButtonRelease>", self.release)
        self.canvas.bind_all("<Shift-B1-ButtonRelease>", self.add_text_selected_items)
        self.canvas.bind_all("<Shift-B1-Motion>", self.drag)
        self.canvas.bind_all("<Shift-Button-1>", self.callback)
        self.canvas.bind_all("<Alt-B1-ButtonRelease>", self.add_rect_selected_area)
        self.canvas.bind_all("<Alt-B1-Motion>", self.drag)
        self.canvas.bind_all("<Alt-Button-1>", self.callback)
        self.bind("<Control-z>", self.undo_action)

        self.canvas_under_frame = ctk.CTkFrame(self, width=900, height=200)
        self.canvas_under_frame.grid(row=1, column=2)

    def create_well_grid_event(self, grid_size: str):
        self.canvas.addtag_all("del")
        self.canvas.delete("del")
        self.rect_id = self.canvas.create_rectangle(
            0, 0, 0, 0, dash=(2, 2), fill="", outline="black"
        )

        if grid_size == "96":
            self.create_canvas(space=70, radius=30, rows=8, cols=12)
            self.radius = 30

    # Creates a canvas from the specified values
    def create_canvas(self, space: int, radius: int, rows: int, cols: int):
        # Updates the values of non circle items
        global non_circle_items
        non_circle_items = rows + cols + 1
        # Algorithm creates letters/num seperately from circles to be easier identify which itemIDs belong to circles
        i = space
        for i in range(rows):
            self.canvas.create_text(
                15,
                space * (i + 1),
                text=LETTER_LIST[i],
                fill="black",
                font=self.font,
                tags="letter",
            )

        for i in range(cols):
            self.canvas.create_text(
                space * (i + 1),
                15,
                text=i + 1,
                fill="black",
                font=self.font,
                tags="num",
            )

        for i in range(cols):
            for j in range(rows):
                x = space * (i + 1)
                y = space * (j + 1)
                self.canvas.create_aa_circle(x, y, radius=radius + 2, fill="black")
                # +1 r, +1 y ?
                id = self.canvas.create_aa_circle(x, y, radius=radius, fill="white")
                coords_circle = x, y
                self.canvas_items_map[id] = coords_circle
                self.item_changes_map[id] = ["white"]

    # Manipulates all circles overlapping with click-drag rectangle
    def release(self, event):
        global rectx1, recty1, rectx2, recty2

        self.canvas.coords(self.rect_id, 0, 0, 0, 0)
        items_overlapping = self.canvas.find_overlapping(rectx1, recty1, rectx2, recty2)
        # Ignores items that aren't inner circle
        list_of_items = []
        for item in items_overlapping:
            if item in self.canvas_items_map:
                list_of_items.append(item)
                self.canvas.itemconfig(item, fill=self.color, tags=self.color)
                self.item_changes_map[item].append(self.color)

                # self.canvas.create_text(self.canvas_items_map[item],text="Test", tags = "text-item")
        tuple = (list_of_items, "color_change")
        self.actions_stack.append(tuple)

    def drag(self, event):
        global rectx2, recty2
        rectx2, recty2 = event.x, event.y
        self.canvas.coords(self.rect_id, rectx1, recty1, rectx2, recty2)

    def callback(self, event):
        global rectx1, recty1, rectx2, recty2
        rectx1, rectx2 = event.x, event.x
        recty1, recty2 = event.y, event.y

    def ask_color(self):
        pick_color = AskColor()  # open the color picker
        color = pick_color.get()  # get the color string

        def change_color():
            self.color = color
            self.change_name_circle.configure(state="normal")

        circle_button = ctk.CTkRadioButton(
            self.scroll_frame_circles,
            border_color=color,
            border_width_checked=11,
            variable=self.radio_var,
            text="",
            fg_color=color,
            command=change_color,
        )
        circle_button.grid(
            row=len(self.circle_radio_list), column=0, padx=20, pady=20, sticky="w"
        )
        self.circle_radio_list[color] = circle_button

    def add_name_radiobutton(self):
        if self.color != "white":
            input_name = ctk.CTkInputDialog(
                text="Write Circle Name", title="Circle Name"
            )
            name = input_name.get_input()
            self.circle_radio_list[self.color].configure(text=name)

    def add_text_to_circletype(self):
        input_text = ctk.CTkInputDialog(text="Write Text", title="Add Text")
        text = input_text.get_input()
        colored_items = self.circle_color_map[self.color]
        for item in colored_items:
            coords_ = self.canvas_items_map[item]
            self.canvas.create_text(coords_, text=text, tags=text, font=self.font)

    def remove_text_for_circles(self):
        self.canvas.itemconfigure(self.color, fill=self.color)

    def add_text_selected_items(self, event):
        global rectx1, recty1, rectx2, recty2
        self.canvas.coords(self.rect_id, 0, 0, 0, 0)
        input_text = ctk.CTkInputDialog(text="Write Text", title="Add Text")
        text = input_text.get_input()
        items_overlapping = self.canvas.find_overlapping(rectx1, recty1, rectx2, recty2)
        # Ignores items that aren't inner circle
        list_of_items = []
        #   #checks if item id is inner circle, and if it already exists as a text-item or not.
        for item in items_overlapping:

            # If exists configure existing text-item
            if item in self.canvas_items_map and item in self.canvas_id_text_map:

                text_item = self.canvas_id_text_map[item]
                self.canvas.itemconfigure(text_item, text=text)
                self.item_changes_map[text_item].append(text)
                list_of_items.append(text_item)
            # If not exists create text-item and add to map
            elif item in self.canvas_items_map and item not in self.canvas_id_text_map:
                coords_ = self.canvas_items_map[item]
                text_item = self.canvas.create_text(
                    coords_, text=text, tags="text", font=self.font
                )
                self.canvas_id_text_map[item] = text_item
                self.item_changes_map[text_item] = [""]
                self.item_changes_map[text_item].append(text)
                list_of_items.append(text_item)

        tuple = (list_of_items, "text_change")
        self.actions_stack.append(tuple)

    def change_font(self, var):
        var
        font = self.font_optionmenu.get()
        size = self.font_size_optionmenu.get()
        style = font + " " + size
        self.font = style

        # Get 2 option menu valeus, concat them to 1 string with a empty space divider, change self.font to the new string

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if "alpha" in kwargs:
            alpha = int(kwargs.pop("alpha") * 255)
            fill = kwargs.pop("fill")
            fill = app.winfo_rgb(fill)
            fill = fill[0] % 256, fill[1] % 256, fill[2] % 256
            fill += (alpha,)
            image = Image.new("RGBA", (x2 - x1, y2 - y1), color=fill)
            IMAGES.append(ImageTk.PhotoImage(image))
            b = self.canvas.create_image(x1, y1, image=IMAGES[-1], anchor="nw")
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        ids = [b, rect]
        tuple = (ids, "item_created")
        self.actions_stack.append(tuple)

    def add_rect_selected_area(self, event):
        global rectx1, recty1, rectx2, recty2

        self.canvas.coords(self.rect_id, 0, 0, 0, 0)
        a = self.canvas.find_overlapping(rectx1, recty1, rectx2, recty2)
        # Ignores items that aren't inner circle

        b, c = 0, 0
        i, j = 0, 1
        while b == 0:
            if a[i] in self.canvas_items_map:
                b = a[i]
            i += 1
        while c == 0:
            if a[len(a) - j] in self.canvas_items_map:
                c = a[len(a) - j]
            j += 1

        coords1 = self.canvas_items_map[b]
        coords2 = self.canvas_items_map[c]

        l = self.radius + 4

        x1, y1 = coords1
        x2, y2 = coords2

        self.create_rectangle(
            x1 - l, y1 - l, x2 + l, y2 + l, fill=self.color, alpha=0.2
        )

    def undo_action(self, event):

        if len(self.actions_stack) < 1:
            return

        prev_action = self.actions_stack.pop()
        items = prev_action[0]

        if prev_action[1] == "color_change":

            for item in items:
                current_color = self.item_changes_map[item].pop()
                prev_color = self.item_changes_map[item][
                    len(self.item_changes_map[item]) - 1
                ]
                self.canvas.itemconfigure(item, fill=prev_color)

        elif prev_action[1] == "text_change":
            for item in items:
                current_text = self.item_changes_map[item].pop()
                prev_text = self.item_changes_map[item][
                    len(self.item_changes_map[item]) - 1
                ]
                self.canvas.itemconfigure(item, text=prev_text)

        elif prev_action[1] == "item_created":
            for item in items:
                self.canvas.delete(item)

    def new_tab(self, tab_name):
        self.stash_data()

        if tab_name != "+":
            self.canvas = self.tab_name_map[tab_name]
            self.update_app_vars()
            ctk.CTk.lift(self.canvas)

        else:
            input_name = ctk.CTkInputDialog(text="Write Tab Name", title="New Tab Name")
            input_name.lift()
            name = input_name.get_input()
            if name == "":
                CTkMessagebox(
                    master=self,
                    title="Error",
                    message="Input tab name is required",
                    icon="cancel",
                    option_1="OK",
                    justify="center",
                ).tkraise()
                self.tab_button.set("")
                return
            elif name == None:
                self.tab_button.set("")
                return

            value_list = self.tab_button._value_list.copy()
            if name in value_list:
                CTkMessagebox(
                    master=self,
                    title="Error",
                    message="Tab name already exists",
                    icon="cancel",
                    option_1="OK",
                    justify="center",
                ).tkraise()
                self.tab_button.set("")
                return

            value_list = self.tab_button._value_list.copy()
            self.canvas = ctk.CTkCanvas(
                master=self, width=900, height=800, highlightcolor="blue"
            )
            self.canvas.grid(row=0, column=2, pady=(50))
            self.stash_data()
            self.tab_name_map[name] = self.canvas

            index = len(value_list) - 1
            value_list.insert(index, name)
            self.tab_button.configure(values=value_list)
            self.tab_button.set(value_list[index])
            ctk.CTk.lift(self.canvas)

    def stash_data(self):
        tuple = (
            self.circle_color_map.copy(),
            self.canvas_items_map.copy(),
            self.canvas_id_text_map.copy(),
            self.actions_stack.copy(),
            self.item_changes_map.copy(),
        )
        self.tab_map[self.canvas] = tuple

    def update_app_vars(self):
        tuple = self.tab_map[self.canvas]
        self.circle_color_map = tuple[0]
        self.canvas_items_map = tuple[1]
        self.canvas_id_text_map = tuple[2]
        self.actions_stack = tuple[3]
        self.item_changes_map = tuple[4]

    def grab_current_state(self):
        self.circle_color_map
        for id in self.canvas_items_map:
            a = self.item_changes_map[id][-1]

            if a not in self.circle_color_map:
                self.circle_color_map[a] = [id]
            else:
                self.circle_color_map[a].append(id)
        keys = self.circle_color_map.keys()
        for key in keys:
            list_id = self.circle_color_map[key]
            smallest_val = 1000000
            largest_val = 0
            for id in list_id:
                if id in self.canvas_id_text_map:
                    b = self.canvas_id_text_map[id]
                    c = self.item_changes_map[b][-1]
                    try:
                        value = int(c)

                        if value > largest_val:
                            largest_val = value
                        elif value < smallest_val:
                            smallest_val = value
                    except ValueError:
                        value = 1
            tuple = (list_id, smallest_val, largest_val)
            self.circle_color_map[key] = tuple

    def create_conc_circle(self, x, y, diameter, **kwargs):

        if "alpha" in kwargs:
            alpha = int(kwargs.pop("alpha") * 255)
            fill = kwargs.pop("fill")
            fill = app.winfo_rgb(fill)
            fill = fill[0] % 256, fill[1] % 256, fill[2] % 256
            fill += (alpha,)
            image = Image.new("RGBA", (diameter, diameter), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.ellipse((0, 0, diameter, diameter), fill=fill)
            IMAGES.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x, y, image=IMAGES[-1])

    def concentration_gradient(self):

        self.stash_data()
        self.grab_current_state()
        value_list = self.tab_button._value_list.copy()
        self.canvas = ctk.CTkCanvas(
            master=self, width=900, height=800, highlightcolor="blue"
        )
        self.canvas.grid(row=0, column=2, pady=(50))
        self.stash_data()
        tab_name = self.tab_button.get() + " %"
        self.tab_name_map[tab_name] = self.canvas
        if tab_name in value_list:
            value_list.remove(tab_name)
        value_list.insert(1, tab_name)
        self.tab_button.configure(values=value_list)
        self.tab_button.set(value_list[1])
        ctk.CTk.lift(self.canvas)
        self.create_well_grid_event("96")
        for color in self.circle_color_map:

            items, _, largest = self.circle_color_map[color]

            for item in items:
                if item in self.canvas_id_text_map:
                    coords = self.canvas_items_map[item]
                    x, y = coords
                    b = self.canvas_id_text_map[item]
                    c = self.item_changes_map[b][-1]
                    try:
                        g = int(c)
                        self.create_conc_circle(
                            x,
                            y,
                            self.radius * 2,
                            fill=color,
                            alpha=(g / largest) * 0.5,
                        )
                    except ValueError:
                        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
