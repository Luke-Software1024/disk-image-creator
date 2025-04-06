from tkinter import ttk, Tk, StringVar, messagebox, filedialog, END, PhotoImage
from os import getcwd

def validate_command(new_value):
    if new_value == "" or new_value.isdigit():
        return True
    return False

main = Tk()
main.title("Create Disk Image")
main.iconphoto(True, PhotoImage(file=f"{getcwd()}\\icon.png"))
vcmd = (main.register(validate_command), '%P')

size_label = ttk.Label(main, text="Disk size:")
size_label.grid(row=0, column=0)

size = ttk.Entry(main, validate="key", validatecommand=vcmd)
size.grid(row=0, column=1)

size_units_value = StringVar()
size_units = ttk.OptionMenu(main, size_units_value, "B (x1)", "B (x1)", "KiB (x1024)", "MiB (x(1024^2))", "GiB (x(1024^3))")
size_units.grid(row=0, column=2)

preset_label = ttk.Label(main, text="Use preset:")
preset_label.grid(row=1, column=0)

preset_value = StringVar()
def set_preset(*args):
    match preset_value.get():
        case "3.5\" floppy disk (1440KiB)":
            size.delete(0, END)
            size.insert(0, "1440")
            size_units_value.set("KiB (x1024)")
        case "5.25\" floppy disk (1200KiB)":
            size.delete(0, END)
            size.insert(0, "1200")
            size_units_value.set("KiB (x1024)")
        case "ZIP disk (100MiB)":
            size.delete(0, END)
            size.insert(0, "100")
            size_units_value.set("MiB (x(1024^2))")
        case "CD (700MiB)":
            size.delete(0, END)
            size.insert(0, "700")
            size_units_value.set("MiB (x(1024^2))")
        case "DVD (4700MiB)":
            size.delete(0, END)
            size.insert(0, "4700")
            size_units_value.set("MiB (x(1024^2))")
preset = ttk.OptionMenu(main, preset_value, "3.5\" floppy disk (1440KiB)", "3.5\" floppy disk (1440KiB)", "5.25\" floppy disk (1200KiB)", "ZIP disk (100MiB)", "CD (700MiB)", "DVD (4700MiB)", command=set_preset)
preset.grid(row=1, column=1)

file_label = ttk.Label(main, text="Into file:")
file_label.grid(row=2, column=0)

file = ttk.Entry(main)
file.grid(row=2, column=1)

def browse():
    user_input = filedialog.asksaveasfilename(filetypes=(("All Files (will use *.IMG if extension ignored)", "*.*"), ("", "")))
    file.delete(0, END)
    if user_input[-4] == "." and not user_input.endswith(".img"):
        modified_user_input = user_input
    else:
        modified_user_input = user_input + ".img"
    file.insert(0, modified_user_input)
browse_button = ttk.Button(main, text="Browse", command=browse)
browse_button.grid(row=2, column=2)

def create():
    messagebox.showinfo("Info", "The disk image will be left unformatted. This may take a while.")
    match size_units_value.get():
        case "B (x1)":
            modified_size = int(size.get())
        case "KiB (x1024)":
            modified_size = int(size.get()) * 1024
        case "MiB (x(1024^2))":
            modified_size = int(size.get()) * 1048576
        case "GiB (x(1024^3))":
            modified_size = int(size.get()) * 1073741824
    image = bytearray([0x00] * modified_size)
    with open(file.get(), "wb") as out_file:
        out_file.write(image)
    messagebox.showinfo("Success", "Creation complete. ")
ok_button = ttk.Button(main, text="OK", command=create)
ok_button.grid(row=3, column=0)
main.mainloop()