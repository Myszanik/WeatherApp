import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")
        master.configure(bg='green')
        master.geometry("800x620")

        for i in range(5):
            master.grid_columnconfigure(i, weight=1)

            # Description label
        self.entry_description = tk.Label(master, text='Please enter city/town below', font=('Trebuchet MS', 35), bg='green')
        self.entry_description.grid(row=0, column=0, columnspan=5, padx=20, pady=(5, 0), sticky='n')

        # Entry widget
        self.entry = tk.Entry(master, width=50, font=('Verdana', 25), bg='white', fg='black', insertbackground='black')
        self.entry.grid(row=1, column=0, columnspan=4, padx=(20, 10), pady=10, sticky='w')

        # Search button
        self.search_button = tk.Button(master, text='Search', font=('Arial', 26), bg='white', fg='black')
        self.search_button.grid(row=1, column=4, padx=(10, 20), pady=10, sticky='e')
        self.search_button.config(command=self.on_search_click)
        master.bind('<Return>', self.on_enter_press)

        # City label
        self.city = tk.Label(master, text='', font=('Roboto Condensed', 25), background='green', fg='orange')
        self.city.grid(row=3, column=0, columnspan=5, pady=5, sticky='n')

        # Error message
        self.error_message = tk.Label(master, text='', font=('Roboto Condensed', 25), background='green', fg='dark red')
        self.error_message.grid(row=3, column=0, columnspan=5, pady=5, sticky='n')
        self.error_message.grid_forget()

        # Temperature label
        self.temperature = tk.Label(master, text='Temperature:', font=('Roboto Condensed', 25), background='green', fg='black')
        self.temperature.grid(row=4, column=0, columnspan=5, pady=5, sticky='n')

        # Condition label
        self.condition = tk.Label(master, text='Condition:', font=('Roboto Condensed', 25), background='green', fg='black')
        self.condition.grid(row=5, column=0, columnspan=5, pady=5, sticky='n')

        # Condition icon (placeholder for now)
        self.condition_icon = tk.Label(master, height=30, background='green')
        self.condition_icon.grid(row=5, column=4, padx=5, pady=5, sticky='w')
        self.condition_icon.grid_forget()

        # Humidity label
        self.humidity = tk.Label(master, text='Humidity:', font=('Roboto Condensed', 25), background='green', fg='black')
        self.humidity.grid(row=6, column=0, columnspan=5, pady=5, sticky='n')

        # Wind Speed label
        self.wind_speed = tk.Label(master, text='Wind Speed:', font=('Roboto Condensed', 25), background='green',  fg='black')
        self.wind_speed.grid(row=7, column=0, columnspan=5, pady=5, sticky='n')

        # Additional data label
        self.additional_data = tk.Label(master, text='Weather forecast for next 5 days', font=('Trebuchet MS', 30), bg='green')
        self.additional_data.grid(row=8, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='n')

        # Additional data label
        self.additional_data = tk.Label(master, text='Weather forecast for next 5 days', font=('Trebuchet MS', 30), bg='green')
        self.additional_data.grid(row=8, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='n')

        # Forecast day labels
        self.day_labels = []
        for i in range(5):
            day_label = tk.Label(master, width=15, height=5, font=('Roboto Condensed', 20), background='light blue', fg='black', justify='center')
            day_label.grid(row=9, column=i, padx=10, pady=10, sticky='nsew')
            self.day_labels.append(day_label)

    def fetch_weather_data(self):
        city = self.entry.get()
        api_key = 'REMOVED_KEY'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()


            temp = round(data['main']['temp'] * 2) / 2
            condition = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = round(data['wind']['speed'] * 3.6)
            icon_code = data['weather'][0]['icon']
            icon_url = f'http://openweathermap.org/img/wn/{icon_code}@2x.png'

            icon_request = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_request.content))
            icon_image = icon_image.resize((90, 70), Image.Resampling.LANCZOS)
            self.weather_icon = ImageTk.PhotoImage(icon_image)

            temp_display = f"{temp:.1f}".rstrip('0').rstrip('.')

            self.temperature.config(text=f'Temperature: {temp_display}°C')
            self.condition.config(text=f'Condition: {condition.capitalize()}')
            self.humidity.config(text=f'Humidity: {humidity}%')
            self.wind_speed.config(text=f'Wind Speed: {wind_speed}km/h')
            self.city.config(text=f'Weather in {city.capitalize()}')
            self.condition_icon.config(image=self.weather_icon)

        except requests.RequestException as e:
            self.temperature.config(text='Error fetching data')
            self.condition.config(text='Error fetching data')
            self.humidity.config(text='Error fetching data')
            self.wind_speed.config(text='Error fetching data')

    def on_search_click(self):
        city = self.entry.get().strip()  # Get the text from the entry and remove any leading/trailing whitespace
        if not city:  # Check if the text is empty
            self.error_message.config(text="Please enter a city/town")
            self.error_message.grid(row=3, column=0, columnspan=5, pady=5, sticky='n')  # Show the error message
        else:
            self.error_message.grid_forget()  # Hide the error message
            self.fetch_weather_data()
            self.entry.delete(0, tk.END)
            self.condition_icon.grid(row=5, column=4, padx=5, pady=5, sticky='w')
            self.city.grid(row=3, column=0, columnspan=5, pady=5, sticky='n')

    def on_enter_press(self, event):
        city = self.entry.get().strip()  # Get the text from the entry and remove any leading/trailing whitespace
        if not city:  # Check if the text is empty
            self.error_message.config(text="Please enter a city/town")
            self.error_message.grid(row=3, column=0, columnspan=5, pady=5, sticky='n')  # Show the error message
        else:
            self.error_message.grid_forget()  # Hide the error message
            self.fetch_weather_data()
            self.entry.delete(0, tk.END)
            self.condition_icon.grid(row=5, column=4, padx=5, pady=5, sticky='w')
            self.city.grid(row=3, column=0, columnspan=5, pady=5, sticky='n')

root = tk.Tk()
ToDoApp = WeatherApp(root)
root.mainloop()