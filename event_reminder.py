import pyodbc, customtkinter, pytz
from datetime import datetime
from plyer import notification
import socket

RES = [300, 300]

class EventReminder:
    def __init__(self):
        self.event_list = []
        self.current_weekday = -1
        self.current_hour = 0
        self.current_min = 0
        self.current_sec = 0
        self.when_current_event_ends = 0
        self.current_event = ""
        self.next_event = ""
        self.isEventChanged = False
        self.timezone = pytz.timezone('CET')
        self.font = ("Roboto", 16, "bold")
        self.countdown_font = ("Roboto", 36, "bold")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.root = customtkinter.CTk()
        self.root.iconbitmap("_internal/gficon.ico")
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        self.coor_x = (self.ws / 2) - (RES[0] / 2)
        self.coor_y = (self.hs / 2) - (RES[1] / 2)
        self.root.geometry('%dx%d+%d+%d' % (RES[0], RES[1], self.coor_x, self.coor_y))
        self.root.resizable(False, False)
        self.root.title("Metin2 Event Reminder")
        self.setup_ui()

    def setup_ui(self):
        self.build_event_text_frame()
        self.build_event_countdown_frame()
        self.get_event_list()
        self.event_check()
        self.user_log()
        
    def user_log(self):
        now = datetime.now(self.timezone)
        host = socket.gethostname()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO who_used VALUES ('{str(host)}', '{str(now)}')")
        conn.commit()
        conn.close()

    def build_event_text_frame(self):
        self.current_e_frame = customtkinter.CTkFrame(master=self.root, fg_color="#212121")
        self.current_e_frame.pack(side="top", expand=False, fill="x", padx=5, pady=5)
        self.next_e_frame = customtkinter.CTkFrame(master=self.root, fg_color="#212121")
        self.next_e_frame.pack(side="top", expand=False, fill="x", padx=5, pady=5)

        self.current_event_text = customtkinter.CTkLabel(master=self.current_e_frame, font=self.font, text_color="white")
        self.current_event_text.pack(side="top", expand=False, fill='x', padx=5, pady=5)
        
        self.next_event_text = customtkinter.CTkLabel(master=self.next_e_frame, font=self.font, text_color="white")
        self.next_event_text.pack(side="top", expand=False, fill='x', padx=5, pady=5)
        
    def build_event_countdown_frame(self):
        self.countdown_frame = customtkinter.CTkFrame(master=self.root, fg_color="black")
        self.countdown_frame.pack(side="bottom", expand=True, fill="both", padx=5, pady=5)

        self.countdown_text = customtkinter.CTkLabel(master=self.countdown_frame, text="None", font=self.countdown_font, text_color="white")
        self.countdown_text.pack(side="left", expand=True, fill="both")

    def get_event_list(self):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        event_list = cursor.execute("SELECT * FROM weekly_events").fetchall()
        for i in event_list:
            self.event_list.append(i)
        conn.commit()
        conn.close()

    def event_check(self):
        current_date = datetime.now(self.timezone)
        if self.current_weekday != current_date.strftime("%w"):
            self.current_weekday = current_date.strftime("%w")
        if self.current_hour != current_date.strftime("%H"):
            self.current_hour = current_date.strftime("%H")
        if self.current_min != current_date.strftime("%M"):
            self.current_min = current_date.strftime("%M")
        if self.current_sec != current_date.strftime("%S"):
            self.current_sec = current_date.strftime("%S")
        isTimeToPickNextEvent = False
        isEventChanged = False
        for event in self.event_list:
            if isTimeToPickNextEvent:
                self.next_event = event[1]
                isTimeToPickNextEvent = False
            if int(event[2]) == int(self.current_weekday) and int(event[3]) <= int(self.current_hour) < int(event[4]):
                if self.current_event != event[1]:
                    self.current_event = event[1]
                    self.when_current_event_ends = event[4]
                    isTimeToPickNextEvent = True
                    isEventChanged = True
                    if self.current_event == "Liderin Kitabi":
                        self.next_event = self.event_list[0][1]
                        isTimeToPickNextEvent = False
        self.current_event_text.configure(text=f"Current Event: {self.current_event}")
        self.next_event_text.configure(text=f"Next Event: {self.next_event}")
        if (self.when_current_event_ends - int(self.current_hour) - 1) > 0 and 59 - int(self.current_min) > 0:
            self.countdown_text.configure(text=f"Next Event\nIN\n{self.when_current_event_ends - int(self.current_hour) - 1}h {59 - int(self.current_min)}m {59 - int(self.current_sec)}s")
        elif (self.when_current_event_ends - int(self.current_hour) - 1) == 0 and 59 - int(self.current_min) > 0:
            self.countdown_text.configure(text=f"Next Event\nIN\n{59 - int(self.current_min)}m {59 - int(self.current_sec)}s")
        elif (self.when_current_event_ends - int(self.current_hour) - 1) == 0 and 59 - int(self.current_min) == 0:
            self.countdown_text.configure(text=f"Next Event\nIN\n{59 - int(self.current_sec)}s")
        if isEventChanged:
            notification.notify(
            title="Metin2 Event Reminder",
            message=f"{self.current_event} currently active\n{self.next_event} is next event",
            timeout=1,
            )
        self.root.after(100, self.event_check)
        
class DbConnection:
    def __init__(self, db_type="server"):
        if db_type == "local":
            driver = "SQL SERVER"
            server = "SCA\SQLEXPRESS"
            db = "Metin2"
            self.connection_string = f"""
                    DRIVER={{{driver}}};
                    SERVER={server};
                    DATABASE={db};
                    Trust_Connection=yes;
                    """
        elif db_type == "server":
            driver = "SQL Server"
            server = "metin2helper.mssql.somee.com"
            db = "metin2helper"
            user = "sca33_SQLLogin_1"
            pw = "ejc7i6uu64"
            self.connection_string = f"""
                            DRIVER={{{driver}}};
                            SERVER={server};
                            DATABASE={db};
                            UID={user};
                            PWD={pw};
                            Trust_Connection=yes;
                            """

    def get_conn(self):
        conn = pyodbc.connect(self.connection_string)
        return conn
    
if __name__ == "__main__":
    app = EventReminder()
    app.root.mainloop()
