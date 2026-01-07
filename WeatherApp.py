import tkinter as tk
from geopy.geocoders import Nominatim
import geocoder
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from io import BytesIO
from dotenv import load_dotenv
import os
load_dotenv()
class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather App")
        master.configure(bg='green')
        master.geometry("1200x910")
        master.resizable(False, False)
        self.current_date = datetime.now().date()  # Set default date or initialize as needed

        # Store the city name
        self.city_name = ""

        # Create frames
        self.main_frame = tk.Frame(master, bg='green')
        self.details_frame = tk.Frame(master, bg='green')

        # Initialize main frame
        self.setup_main_frame()
        self.setup_details_frame()

        # Start with main frame
        self.main_frame.pack(fill='both', expand=True)

    def create_label(self, parent, text, row, column, columnspan=5, font_size=30, pady=5):
        label = tk.Label(parent, text=text, font=('Roboto Condensed', font_size), background='green', fg='black')
        label.grid(row=row, column=column, columnspan=columnspan, pady=pady, sticky='n')
        return label

    def setup_main_frame(self):
        for i in range(5):
            self.main_frame.grid_columnconfigure(i, weight=1)

            # Description label
        self.entry_description = tk.Label(self.main_frame, text='Please enter location below', font=('Trebuchet MS', 55), bg='green')
        self.entry_description.place(x=240, y=10)  # Adjust x and y based on your window layout
        # Entry widget
        self.entry = tk.Entry(self.main_frame, width=39, font=('Verdana', 35), bg='white', fg='black', insertbackground='black')
        self.entry.place(x=20, y=85)  # Adjust x and y based on your window layout
        self.entry.focus_set()  # Set focus to the entry widget
        self.entry.bind('<KeyRelease>', self.capitalize_first_letter)

        # Search button
        self.search_button = tk.Button(self.main_frame, text='Search', width=10, font=('Arial', 36), bg='white', fg='black')
        self.search_button.place(x=929, y=85)  # Adjust x and y based on your window layout
        self.search_button.config(command=self.on_search_click)
        self.entry.bind('<Return>', self.on_enter_press)
        self.master.update_idletasks()

        # City label
        self.city = tk.Label(self.main_frame, text='', font=('Roboto Condensed', 40), background='green', fg='orange')
        self.city.grid(row=3, column=0, columnspan=5, pady=(145, 0), sticky='n')  # Add padding only above the label

        # Error message
        self.error_message = tk.Label(self.main_frame, text='', font=('Roboto Condensed', 45), background='green', fg='dark red')
        self.error_message.grid(row=3, column=0, columnspan=5, pady=(145, 0), sticky='n')
        self.error_message.grid_forget()

        # Condition icon (placeholder for now)
        self.condition_icon = tk.Label(self.main_frame, height=35, background='green')
        self.condition_icon.place(x=800, y=260)  # Adjust x and y based on your window layout
        self.condition_icon.place_forget()

        # Additional data label
        self.additional_data = tk.Label(self.main_frame, text='Weather forecast for next 5 days', font=('Trebuchet MS', 30), bg='green')
        self.additional_data.grid(row=13, column=0, columnspan=5, padx=20, pady=(5, 5), sticky='n')
        self.additional_data.grid_forget()

        # Forecast day labels
        self.day_labels = []
        for i in range(5):
            day_label = tk.Label(self.main_frame, width=15, font=('Roboto Condensed', 30), background='dark green', fg='black', justify='center')
            day_label.grid(row=14, column=i, padx=10, pady=(10, 0), sticky='nsew')
            day_label.bind('<Button-1>', self.on_day_label_click)  # Bind click event
            self.day_labels.append(day_label)
            self.master.update_idletasks()

        # Hide labels initially
        self.hide_day_labels()

        # Use the new method to create labels
        self.temperature = self.create_label(self.main_frame, 'Temperature:', 4, 0)
        self.condition = self.create_label(self.main_frame, 'Condition:', 5, 0)
        self.humidity = self.create_label(self.main_frame, 'Humidity:', 6, 0)
        self.wind_speed = self.create_label(self.main_frame, 'Wind Speed:', 7, 0)
        self.chance_of_rain = self.create_label(self.main_frame, 'Chance of Rain:', 8, 0)
        self.visibility = self.create_label(self.main_frame, 'Visibility:', 9, 0)
        self.min_and_max_temp = self.create_label(self.main_frame, 'Minimum and Maximum Temperature:', 10, 0)
        self.sunrise = self.create_label(self.main_frame, 'Sunrise:', 11, 0)
        self.sunset = self.create_label(self.main_frame, 'Sunset:', 12, 0)

    def hide_day_labels(self):
        for label in self.day_labels:
            label.grid_forget()  # Use grid_forget to hide labels added with grid

    def setup_details_frame(self):
        # Details screen setup
        self.details_label = tk.Label(self.details_frame, text='', font=('Roboto Condensed', 40), background='green', fg='orange')
        self.details_label.grid(row=0, column=1, padx=0, pady=(100, 0), sticky='n')

        self.hourly_data_frame = tk.Frame(self.details_frame, bg='green')
        self.hourly_data_frame.grid(row=1, column=1, padx=0, pady=(60, 0), sticky='nsew')

        self.main_menu_button = tk.Button(self.details_frame, text='Main Screen', width=8, font=('Arial', 20), bg='white', fg='black', command=self.show_main_frame)
        self.main_menu_button.place(x=530, y=0)

        self.previous_day_button = tk.Button(self.details_frame, text='Previous Day', width=8, font=('Arial', 20), bg='white', fg='black', command=self.show_previous_day)
        self.previous_day_button.place(x=0, y=0)

        self.previous_day_error_message = tk.Label(self.details_frame, text='', width=17, font=('Arial', 30), bg='green', fg='dark red')
        self.previous_day_error_message.place(x=0, y=50)
        self.previous_day_error_message.place_forget()

        self.next_day_button = tk.Button(self.details_frame, text='Next Day', width=8, font=('Arial', 20), bg='white', fg='black', command=self.show_next_day)
        self.next_day_button.place(x=1068, y=0)

        self.next_day_error_message = tk.Label(self.details_frame, text='', width=14, font=('Arial', 30), bg='green', fg='dark red')
        self.next_day_error_message.place(x=960, y=50)
        self.next_day_error_message.place_forget()

        self.hour_labels = []

        for i in range(8):
            text_widget = tk.Text(self.hourly_data_frame, width=18, height=9, bg='dark green', fg='black', font=('Roboto Condensed', 25), wrap='word', borderwidth=0, highlightthickness=0)
            text_widget.insert(tk.END, " " * 15)  # Insert space to ensure proper formatting
            text_widget.grid(row=i // 4, column=i % 4, padx=5, pady=10, sticky='nsew')
            self.hour_labels.append(text_widget)

        # Optionally, you can update the layout for the entire master window
        self.master.update_idletasks()

    def show_previous_day(self):
        if self.current_date:
            # Calculate the previous date
            previous_date = self.current_date - timedelta(days=1)

            # Check if the previous_date is within the 5-day range
            if previous_date in self.forecast_dates:
                self.current_date = previous_date
                self.fetch_3hourly_data(previous_date.strftime("%A"))
                self.show_details_frame(previous_date.strftime("%A"))
            else:
                self.previous_day_error_message.place(x=0, y=50)
                self.previous_day_error_message.config(text='No previous day data')  # Display error message
                self.previous_day_error_message.after(1500, self.clear_message)

    def show_next_day(self):
        if self.current_date:
            # Calculate the next date
            next_date = self.current_date + timedelta(days=1)

            # Check if the next_date is within the 5-day range
            if next_date in self.forecast_dates:
                self.current_date = next_date
                self.fetch_3hourly_data(next_date.strftime("%A"))
                self.show_details_frame(next_date.strftime("%A"))
            else:
                self.next_day_error_message.place(x=960, y=50)
                self.next_day_error_message.config(text='No next day data')  # Display error message
                self.next_day_error_message.after(1500, self.clear_message)

    def show_details_frame(self, date):
        self.details_label.config(text=f"The forecast for {date} is displayed in 3-hour intervals")
        self.main_frame.pack_forget()
        self.details_frame.pack(fill='both', expand=True)
        self.fetch_3hourly_data(date)  # Fetch and display hourly data
        self.master.update_idletasks()

    def show_main_frame(self):
        self.details_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)
        self.master.update_idletasks()

    def on_day_label_click(self, event):
        day = event.widget.cget('text').split('\n')[0]  # Get the day from the label text
        selected_date = self.get_date_from_day(day)
        if selected_date:
            self.current_date = selected_date
            self.show_details_frame(day)
            self.master.update_idletasks()

    def get_date_from_day(self, day_name):
        for i, label in enumerate(self.day_labels):
            if label.cget('text').startswith(day_name):
                return self.forecast_dates[i]  # Assuming forecast_dates is a list of datetime objects
        return None

    def capitalize_first_letter(self, event):
        # Get the current content of the entry
        content = self.entry.get()

        # If the content is not empty, capitalize the first letter
        if content:
            # Capitalize the first letter and combine it with the rest of the text
            content = content[0].upper() + content[1:]

            # Set the modified content back to the entry widget
            self.entry.delete(0, tk.END)  # Delete the existing content
            self.entry.insert(0, content)  # Insert the modified content

    # Fetching hourly data method
    def fetch_3hourly_data(self, date):
        city = self.city_name
        api_key = os.getenv("api_key")
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Convert day name to date format
            selected_date = None
            for forecast in data['list']:
                forecast_date = forecast['dt_txt'].split()[0]
                date_obj = datetime.strptime(forecast_date, "%Y-%m-%d")
                forecast_day = date_obj.strftime("%A")
                if forecast_day == date:
                    selected_date = forecast_date
                    break

            if not selected_date:
                print("No data available for the selected date.")
                return

            # Filter 3-hourly data by selected date
            three_hourly_data = [forecast for forecast in data['list'] if forecast['dt_txt'].startswith(selected_date)]

            # Clear existing data
            for text_widget in self.hour_labels:
                text_widget.config(state=tk.NORMAL)  # Temporarily make the Text widget editable
                text_widget.delete('1.0', tk.END)
                text_widget.config(state=tk.DISABLED)  # Reapply non-editable state

            # Update text widgets with 3-hourly data
            for i, forecast in enumerate(three_hourly_data[:8]):  # Adjusted to 8 labels
                forecast_time = forecast['dt_txt'][11:16]  # Extract time (HH:MM)
                temp = forecast['main']['temp']
                description = forecast['weather'][0]['description'].capitalize()
                humidity = forecast['main']['humidity']
                wind_speed = forecast['wind']['speed'] * 3.6
                visibility = forecast.get('visibility', 1000) / 1000  # Convert from meters to kilometers (default to 1 km if not available)

                # Chance of rain (default to 0 if 'rain' key doesn't exist)
                chance_of_rain = forecast.get('rain', {}).get('3h', 0)  # Use '3h' for 3-hour rain data

                # Use tk.Text widget to display formatted text
                text_widget = self.hour_labels[i]
                text_widget.config(state=tk.NORMAL)  # Temporarily make the Text widget editable
                text_widget.delete('1.0', tk.END)
                text_widget.insert(tk.END, f"{forecast_time}\n", ('bold_underline'))
                text_widget.insert(tk.END, f"Temp: {temp:.1f}°C\nCondition: {description}\nHumidity: {humidity}%\nWind: {wind_speed:.1f} km/h\nVisibility: {visibility}km\nChance of Rain: {chance_of_rain}mm")
                text_widget.config(state=tk.DISABLED)  # Reapply non-editable state

                # Define tags for formatting
                text_widget.tag_configure('bold_underline', font=('Roboto Condensed', 35, 'bold', 'underline'))

            self.master.update_idletasks()

        except requests.RequestException as e:
            print(f"RequestException: {e}")
            for text_widget in self.hour_labels:
                text_widget.config(state=tk.NORMAL)  # Temporarily make the Text widget editable
                text_widget.delete('1.0', tk.END)
                text_widget.insert(tk.END, '')
                text_widget.config(state=tk.DISABLED)  # Reapply non-editable state

    def fetch_weather_data(self):
        city = self.entry.get()
        api_key = os.getenv("api_key")
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Fetch basic weather data
            temp = round(data['main']['temp'] * 2) / 2
            condition = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = round(data['wind']['speed'] * 3.6)
            visibility = data['visibility'] / 1000  # Convert from meters to kilometers
            min_temp = round(data['main']['temp_min'] * 2) / 2
            max_temp = round(data['main']['temp_max'] * 2) / 2

            # Calculate sunrise and sunset times
            sunrise_timestamp = data['sys']['sunrise']
            sunset_timestamp = data['sys']['sunset']
            sunrise = datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
            sunset = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')

            # Chance of rain (default to 0 if 'rain' key doesn't exist)
            chance_of_rain = data.get('rain', {}).get('1h', 0)

            # Weather icon
            icon_code = data['weather'][0]['icon']
            icon_url = f'http://openweathermap.org/img/wn/{icon_code}@2x.png'

            icon_request = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_request.content))
            icon_image = icon_image.resize((90, 70), Image.Resampling.LANCZOS)
            self.weather_icon = ImageTk.PhotoImage(icon_image)

            # Format temperature display
            temp_display = f"{temp:.1f}".rstrip('0').rstrip('.')
            min_temp_display = f"{min_temp:.1f}".rstrip('0').rstrip('.')
            max_temp_display = f"{max_temp:.1f}".rstrip('0').rstrip('.')

            # Update the labels with the fetched data
            self.temperature.config(text=f'Temperature: {temp_display}°C')
            self.condition.config(text=f'Condition: {condition.capitalize()}')
            self.humidity.config(text=f'Humidity: {humidity}%')
            self.wind_speed.config(text=f'Wind Speed: {wind_speed} km/h')
            self.visibility.config(text=f'Visibility: {visibility:.1f} km')
            self.min_and_max_temp.config(text=f'Minimum and Maximum Temperature: {min_temp_display}°C / {max_temp_display}°C')
            self.sunrise.config(text=f'Sunrise: {sunrise}')
            self.sunset.config(text=f'Sunset: {sunset}')
            self.chance_of_rain.config(text=f'Chance of Rain: {chance_of_rain:.1f} mm')
            self.city.config(text=f'Weather in {city.capitalize()}')
            self.condition_icon.config(image=self.weather_icon)

            self.master.update_idletasks()


        except requests.RequestException as e:
            error_message = "Please enter a valid location"
            # Display the error message in the designated label
            self.error_message.config(text=error_message)
            self.error_message.grid(row=3, column=0, columnspan=5, pady=(145, 0), sticky='n')  # Show the error message
            self.additional_data.grid_forget()

            self.master.update_idletasks()

    def fetch_5day_forecast(self):
        city = self.entry.get()
        api_key = os.getenv("api_key")
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Extract the daily forecasts at 12:00 PM for each day (forecast is every 3 hours)
            daily_forecasts = {}
            forecast_dates = []
            for forecast in data['list']:
                dt_txt = forecast['dt_txt']
                if "12:00:00" in dt_txt:
                    date = dt_txt.split()[0]
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    date = date_obj.strftime("%A")
                    if len(daily_forecasts) < 5:  # Limit to the first 5 days
                        daily_forecasts[date] = forecast
                        forecast_dates.append(date_obj.date())

            # Update day labels with forecast data
            for i, (date, forecast) in enumerate(daily_forecasts.items()):
                if i < 5:  # Limit to the first 5 days
                    temp = round(forecast['main']['temp'] * 2) / 2
                    condition = forecast['weather'][0]['description'].capitalize()
                    icon_code = forecast['weather'][0]['icon']
                    icon_url = f'http://openweathermap.org/img/wn/{icon_code}@2x.png'

                    icon_request = requests.get(icon_url)
                    icon_image = Image.open(BytesIO(icon_request.content))
                    icon_image = icon_image.resize((100, 100), Image.Resampling.LANCZOS)
                    weather_icon = ImageTk.PhotoImage(icon_image)

                    display_text = f"{date}\n{temp:.1f}°C"
                    self.day_labels[i].config(text=display_text, image=weather_icon, compound='top')
                    self.day_labels[i].image = weather_icon  # Keep a reference to avoid garbage collection

            self.forecast_dates = forecast_dates
            self.master.update_idletasks()
            return True

        except requests.RequestException as e:
            return False

    def clear_forecast_labels(self):
        for label in self.day_labels:
            label.grid_forget()  # Hide the labels if they are visible

    def on_search_click(self):
        city = self.entry.get().strip()

        # Display an error message if no city is entered
        if not city:
            self.error_message.config(text="Please enter a location")
            self.error_message.grid(row=3, column=0, columnspan=5, pady=(145, 0), sticky='n')
            self.clear_forecast_labels()
            return

        self.error_message.grid_forget()  # Hide the error message if there's any
        self.city_name = city  # Store the city name

        # Hide forecast labels initially
        self.clear_forecast_labels()

        # Fetch weather data
        self.fetch_weather_data()

        # Fetch 5-day forecast data and only display if successful
        if self.fetch_5day_forecast():
            self.condition_icon.place(x=800, y=260)
            self.city.grid(row=3, column=0, columnspan=5, pady=(145, 0), sticky='n')
            self.additional_data.grid(row=13, column=0, columnspan=5, padx=20, pady=(5, 5), sticky='n')
            for i, label in enumerate(self.day_labels):
                label.grid(row=14, column=i, padx=10, pady=(10, 0), sticky='nsew')
        else:
            self.error_message.config(text="Please enter a valid location")
            self.error_message.grid(row=3, column=0, columnspan=5, pady=(145, 0), sticky='n')

        self.entry.delete(0, tk.END)
        self.master.update_idletasks()

    def on_enter_press(self, event):
        self.on_search_click()
        self.master.update_idletasks()

    def clear_message(self):
        self.next_day_error_message.config(text="")
        self.previous_day_error_message.config(text='')

root = tk.Tk()
ToDoApp = WeatherApp(root)
root.mainloop()
