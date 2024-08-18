import tkinter as tk
class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")
        master.configure(bg='light slate gray')

        self.entry = tk.Entry(master, width=50, font=('Arial', 40), justify='center', bg='black')
        self.entry.grid(row=1, column=0, columnspan=8)
        self.entry_description = tk.Label(master, text='Please enter city below', width=50, font=('Arial', 40))
        self.entry_description.grid(row=0, column=0)
        self.search_button = tk.Button(master, width=11, height=2, text='Search', font=('Arial', 20), bg='black')
        self.search_button.place(x=1000, y=53)

root = tk.Tk()
ToDoApp = WeatherApp(root)
root.mainloop()