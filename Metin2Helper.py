import customtkinter
from pygame import mixer
import pyodbc
from CTkListbox import CTkListbox
from CTkMessagebox import CTkMessagebox
from datetime import datetime, timedelta, date
import pytz, time
from plyer import notification

WIDTH = 400
HEIGHT = 200
LOGIN_RES = [1100, 400]

class Metin2Helper:
    def __init__(self):
        mixer.init()
        self.razador_sound = mixer.Sound("_internal/razador_notification.wav")
        self.event_sound = mixer.Sound("_internal/event_notification.wav")
        self.exit_sound = mixer.Sound("_internal/exit_notification.wav")
        self.timezone = pytz.timezone('CET')
        self.current_hour = 0
        self.event_list = []
        self.current_weekday = -1
        self.current_event = ""
        self.next_event = ""
        self.isEventChanged = False
        self.isCollapsed = False
        self.default_text_of_timer_frame = "You Can Start A Session \n by Clicking \n 'Start Razador Session' \n Button"
        self.how_many_chest_dropped = 0
        self.where_u_left = 0
        self.minute = 30
        self.stopwatch_duration = -1
        self.minute_will_be_shown = ""
        self.second_will_be_shown = ""
        self.isAlarmRunning1  = False
        self.isCountdownRunning = False
        self.isStopwatchRunning = False
        self.sayac_suresi = (60 * self.minute) + 1
        self.kac_kez_caldi = 0
        self.last_stopwatch_duration = 0
        self.kill_list = []
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.root = customtkinter.CTk()
        self.root.iconbitmap("_internal/gficon.ico")
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        self.coor_x = (self.ws / 2) - (LOGIN_RES[0] / 5.2)
        self.coor_y = (self.hs / 2) - (LOGIN_RES[1] / 2)
        self.current_x = self.root.winfo_rootx()
        self.current_y = self.root.winfo_rooty()
        self.root.title("Metin2 Helper")
        self.root.geometry('%dx%d+%d+%d' % (LOGIN_RES[0], LOGIN_RES[1], self.coor_x, self.coor_y))
        self.root.minsize(width=int(LOGIN_RES[0] / 4), height=LOGIN_RES[1])
        self.root.maxsize(width=LOGIN_RES[0], height=LOGIN_RES[1])
        self.root.resizable(False, True)
        self.setupUI()

    def setupUI(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_left_frame()
        self.build_right_frame()
        self.build_sales_frame()
        self.get_event_list()
        self.event_control()
        self.event_changer()
        self.collapse()

    def build_left_frame(self):
        self.left_frame = customtkinter.CTkFrame(master=self.root, width=500)
        self.left_frame.pack(fill="both", expand=False, side="left", padx=5, pady=5)

        self.frame_in_left_frame = customtkinter.CTkFrame(master=self.left_frame, fg_color="#212121")
        self.frame_in_left_frame.pack(side='top', fill='x', padx=3, pady=3)

        self.event_text = customtkinter.CTkLabel(master=self.frame_in_left_frame, text="None", font=("Roboto", 12, "bold"), text_color="yellow")
        self.event_text.pack(side="top", expand=False)

        self.last_stopwatch_duration_text = customtkinter.CTkLabel(master=self.frame_in_left_frame,
            text=str(f"Last Razador Duration: {self.last_stopwatch_duration // 60} min"
            f" and {self.last_stopwatch_duration % 60} sec"),
            text_color='#00F3FF', font=('Roboto', 17, 'bold'))
        self.last_stopwatch_duration_text.pack(side='left', fill='both', pady=7, padx=5)

        self.start_stop_button = customtkinter.CTkButton(master=self.left_frame, text="End Razador Session",
                                                         text_color="white", font=("Roboto", 16, "bold"),
                                                         command=self.start_stop_timer, fg_color="#232323",
                                                         border_width=1, hover_color="#474747")
        self.start_stop_button.pack(fill='both', expand=False, side="bottom", padx=5, pady=5)

        self.start_and_stop_stopwatch_button = customtkinter.CTkButton(master=self.left_frame,
                                                                       text="Start Razador Session", text_color="white",
                                                                       font=("Roboto", 16, "bold"),
                                                                       command=self.start_and_stop_stopwatch,
                                                                       fg_color="#232323", border_width=1,
                                                                       hover_color="#474747")
        self.start_and_stop_stopwatch_button.pack(fill='both', expand=False, side="bottom", padx=5, pady=5)

        self.timer_text = customtkinter.CTkLabel(master=self.left_frame, text=self.default_text_of_timer_frame,
                                                 font=('Roboto', 18, 'bold'), text_color="white")
        self.timer_text.pack(side='left', expand=True, padx=2, pady=2)

        self.build_collapse_frame()

    def build_collapse_frame(self):
        self.collapse_button_frame = customtkinter.CTkFrame(master=self.root, width=20)
        self.collapse_button_frame.pack(side="left", fill='y', expand=False, pady=5)

        self.collapse_button = customtkinter.CTkButton(master=self.collapse_button_frame,
                                                       text="<<", width=1, text_color="white", hover_color="#313131",
                                                       font=("Roboto", 14, "bold"),
                                                       fg_color="#212121", command=self.collapse)
        self.collapse_button.pack(side='right', expand=False, fill='y')

    def build_right_frame(self):
        self.right_frame = customtkinter.CTkFrame(master=self.root)
        self.right_frame.pack(fill="both", expand=False, side="left", padx=5, pady=5)

        self.information_text = customtkinter.CTkLabel(master=self.right_frame, text="",
                                                       font=('Roboto', 16, 'bold'), text_color="#00F3FF")
        self.information_text.pack(fill="both", expand=False, side='top', pady=5)

        self.killed_razador_list = CTkListbox(master=self.right_frame, text_color="#FFBD00",
                                              font=("Roboto", 14, "normal"), justify='center',
                                              command=self.list_box_clicked, border_width=0)
        self.killed_razador_list.pack(fill="both", expand=True, padx=5, pady=5)

        self.avarage_of_dropped_chest_label = customtkinter.CTkLabel(master=self.right_frame, text="",
                                                                     text_color="#FFFB00")
        self.avarage_of_dropped_chest_label.pack(side='top', fill='both')

        self.weekly_event = customtkinter.CTkButton(master=self.right_frame, text="Today's Events",
                                                    font=("Roboto", 20, "bold"), fg_color="#232323", border_width=1,
                                                    hover_color="#474747", text_color="white")
        self.weekly_event.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        self.truncate_list = customtkinter.CTkButton(master=self.right_frame, text="Clear List",
                                                     command=self.clear_list, text_color='white',
                                                     font=('Roboto', 20, "bold"), fg_color="#232323", border_width=1,
                                                     hover_color="#474747")
        self.truncate_list.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        self.fill_razador_killed_listBox()

    def build_sales_frame(self):
        self.sales_frame = customtkinter.CTkFrame(master=self.root)
        self.sales_frame.pack(side='right', fill='both', expand=False, padx=5, pady=5)

        self.won_amount_frame = customtkinter.CTkFrame(master=self.sales_frame)
        self.won_amount_frame.pack(side='top', fill='both', padx=5, pady=5)
        self.won_amount_text = customtkinter.CTkLabel(master=self.won_amount_frame, text="Won Amount: ",
                                                      text_color="white", font=("Roboto", 16, "bold"))
        self.won_amount_text.pack(side='left', padx=5, pady=5)
        self.won_amount_entry = customtkinter.CTkEntry(master=self.won_amount_frame, font=("Roboto", 16, "bold"),
                                                     text_color="white")
        self.won_amount_entry.pack(side='right', padx=5, pady=5)

        self.won_price_frame = customtkinter.CTkFrame(master=self.sales_frame)
        self.won_price_frame.pack(side='top', fill='both', padx=5, pady=5)
        self.won_price_text = customtkinter.CTkLabel(master=self.won_price_frame, text="Sale Price: ",
                                                     text_color="white", font=("Roboto", 16, "bold"))
        self.won_price_text.pack(side='left', padx=5, pady=5)
        self.won_price_entry = customtkinter.CTkEntry(master=self.won_price_frame, font=("Roboto", 16, "bold"),
                                                     text_color="white")
        self.won_price_entry.pack(side='right', padx=5, pady=5)

        self.submit_sale_button = customtkinter.CTkButton(master=self.sales_frame, text="Save Sale", text_color="white",
                                                          font=("Roboto", 20, "bold"), fg_color="#232323",
                                                          border_width=1, hover_color="#474747",
                                                          command=self.submit_sale)
        self.submit_sale_button.pack(side='top', fill='both', padx=5, pady=5)

        self.last_sales_list = CTkListbox(master=self.sales_frame, text_color="#FFBD00", font=("Roboto", 14, "normal"),
                                          justify='center', command=self.sales_list_box_clicked, border_width=0)
        self.last_sales_list.pack(side='top', fill='both', expand=True)

        self.sales_info_frame = customtkinter.CTkFrame(master=self.sales_frame, fg_color="green")
        self.sales_info_frame.pack(side='bottom', fill='both', padx=5, pady=5)
        self.total_record_count = customtkinter.CTkLabel(master=self.sales_info_frame, text_color="white",
                                                         font=("Roboto", 16, "bold"), justify='center')
        self.total_record_count.pack(side='left', fill='both', padx=5, pady=3, expand=True)
        self.sales_analysis_button = customtkinter.CTkButton(master=self.sales_info_frame, text="?", width=10, fg_color="#123212", text_color="white", command=self.open_sales_analyse)
        self.sales_analysis_button.pack(side='right', fill='both', padx=5, pady=3, expand=False)
        self.sales_list_refresh()

    def open_sales_analyse(self):
        m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12 = [], [], [], [], [], [], [], [], [], [], [], []
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sales ORDER BY Sales_date")
        self.first_sale = datetime
        x = 0
        y = 0
        total_price = 0
        total_won = 0
        for _ in cursor.fetchall():
            date = _[3]
            if date.month == 1:
                m1.append(_[2])
            elif date.month == 2:
                m2.append(_[2])
            elif date.month == 3:
                m3.append(_[2])
            elif date.month == 4:
                m4.append(_[2])
            elif date.month == 5:
                m5.append(_[2])
            elif date.month == 6:
                m6.append(_[2])
            elif date.month == 7:
                m7.append(_[2])
            elif date.month == 8:
                m8.append(_[2])
            elif date.month == 9:
                m9.append(_[2])
            elif date.month == 10:
                m10.append(_[2])
            elif date.month == 11:
                m11.append(_[2])
            elif date.month == 12:
                m12.append(_[2])
            if y == 0:
                self.first_sale = date
            total_price += _[2]
            total_won += _[1]
            x += 1
            if y != 1:
                y += 1

        # Initialize month variables
        January = February = March = April = May = June = July = August = September = October = November = December = 0

        # Sum the values for each month
        for j in m1:
            January += j * 0.92
        for f in m2:
            February += f * 0.92
        for mr in m3:
            March += mr * 0.92
        for ap in m4:
            April += ap * 0.92
        for ma in m5:
            May += ma * 0.92
        for jn in m6:
            June += jn * 0.92
        for jl in m7:
            July += jl * 0.92
        for ag in m8:
            August += ag * 0.92
        for sp in m9:
            September += sp * 0.92
        for oc in m10:
            October += oc * 0.92
        for nv in m11:
            November += nv * 0.92
        for dc in m12:
            December += dc * 0.92

        # Calculate income per day
        now = datetime.now()
        diff = abs(now - self.first_sale).days
        income_per_day = (total_price / diff) * 0.92
        str_pdi = str(income_per_day)[:6]

        # Create the message
        msg = f"Work Time : {diff} Days ({diff // 30}M - {diff % 30}D)\nTotal Won Sold : {total_won} Won\nTotal Income : {round(total_price * 0.92,2)} TL\nPer Day Income : {str_pdi}\nPer Month Income : {str(round(income_per_day * 30, 2))}"
        current_date = datetime.now()
        current_month = current_date.month
        if current_month == 1:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)"
        elif current_month == 2:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)"
        elif current_month == 3:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\n March: {March} TL ({len(m3)} Sales)"
        elif current_month == 4:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\n March: {March} TL ({len(m3)} Sales)\n April: {April} TL ({len(m4)} Sales)"
        elif current_month == 5:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)"
        elif current_month == 6:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {round(May,2)} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)"
        elif current_month == 7:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)\nJuly: {July} TL ({len(m7)} Sales)"
        elif current_month == 8:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)\nJuly: {July} TL ({len(m7)} Sales)\nAugust: {August} TL ({len(m8)} Sales)"
        elif current_month == 9:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)\nJuly: {July} TL ({len(m7)} Sales)\nAugust: {August} TL ({len(m8)} Sales)\nSeptember: {September} TL ({len(m9)} Sales)"
        elif current_month == 10:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)\nJuly: {July} TL ({len(m7)} Sales)\nAugust: {August} TL ({len(m8)} Sales)\nSeptember: {September} TL ({len(m9)} Sales)\nOctober: {October} TL ({len(m10)} Sales)"
        elif current_month == 11:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)\nJuly: {July} TL ({len(m7)} Sales)\nAugust: {August} TL ({len(m8)} Sales)\nSeptember: {September} TL ({len(m9)} Sales)\nOctober: {October} TL ({len(m10)} Sales)\nNovember: {November} TL ({len(m11)} Sales)"
        elif current_month == 12:
            msg += f"\nJanuary: {January} TL ({len(m1)} Sales)\nFebruay: {February} TL ({len(m2)} Sales)\nMarch: {March} TL ({len(m3)} Sales)\nApril: {April} TL ({len(m4)} Sales)\nMay: {May} TL ({len(m5)} Sales)\nJune: {June} TL ({len(m6)} Sales)\nJuly: {July} TL ({len(m7)} Sales)\nAugust: {August} TL ({len(m8)} Sales)\nSeptember: {September} TL ({len(m9)} Sales)\nOctober: {October} TL ({len(m10)} Sales)\nNovember: {November} TL ({len(m11)} Sales)\nDecember: {December} TL ({len(m12)} Sales)"
         
        # Show the information message
        InfoMessage(title="Analyse", msg=msg).show_info()
        conn.close()

    def get_event_list(self):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        event_list = cursor.execute("SELECT * FROM weekly_events").fetchall()
        for i in event_list:
            self.event_list.append(i)

    def event_control(self):
        current_date = datetime.now(self.timezone)
        if self.current_weekday != current_date.strftime("%w"):
            self.current_weekday = current_date.strftime("%w")
        if self.current_hour != current_date.strftime("%H"):
            self.current_hour = current_date.strftime("%H")
        isTimeToPickNextEvent = False
        isEventChanged = False
        for event in self.event_list:
            if isTimeToPickNextEvent:
                self.next_event = event[1]
                isTimeToPickNextEvent = False
            if int(event[2]) == int(self.current_weekday) and int(event[3]) <= int(self.current_hour) < int(event[4]):
                if self.current_event != event[1]:
                    self.current_event = event[1]
                    isTimeToPickNextEvent = True
                    isEventChanged = True
                    if self.current_event == "Liderin Kitabi":
                        self.next_event = self.event_list[0][1]
                        isTimeToPickNextEvent = False
        if isEventChanged:
            notification.notify(
            title="Metin2 Helper",
            message=f"{self.current_event} currently active\n{self.next_event} is next event",
            timeout=1,
            )
            self.event_sound.play()
        self.root.after(100, self.event_control)

    def collapse(self):
        if not self.isCollapsed:
            self.collapse_button.configure(text="|\n~\n \ne\nx\np\na\nn\nd\n \n~\n|")
            if self.last_stopwatch_duration // 60 < 10 and self.last_stopwatch_duration % 60 < 10 and self.current_event != "Münzevi Tavsiyesi":
                self.root.geometry('%dx%d' % ((LOGIN_RES[0] / 2.85), LOGIN_RES[1]))
            elif self.last_stopwatch_duration // 60 < 10 and self.last_stopwatch_duration % 60 >= 10:
                self.root.geometry('%dx%d' % ((LOGIN_RES[0] / 2.78), LOGIN_RES[1]))
            elif self.last_stopwatch_duration // 60 >= 10 and self.last_stopwatch_duration % 60 < 10:
                self.root.geometry('%dx%d' % ((LOGIN_RES[0] / 2.78), LOGIN_RES[1]))
            elif self.last_stopwatch_duration // 60 >= 10 and self.last_stopwatch_duration % 60 >= 10:
                self.root.geometry('%dx%d' % ((LOGIN_RES[0] / 2.70), LOGIN_RES[1]))
            if self.last_stopwatch_duration // 60 < 10 and self.last_stopwatch_duration % 60 < 10 and self.current_event == "Münzevi Tavsiyesi":
                self.root.geometry('%dx%d' % ((LOGIN_RES[0] / 2.61), LOGIN_RES[1]))
            if self.last_stopwatch_duration // 60 < 10 and self.last_stopwatch_duration % 60 < 10 and self.current_event == "Yesil Ejderha Fasülyesi":
                self.root.geometry('%dx%d' % ((LOGIN_RES[0] / 2.70), LOGIN_RES[1]))
            self.right_frame.pack_forget()
            self.sales_frame.pack_forget()
            self.isCollapsed = True
        else:
            self.collapse_button.configure(text="|\n~\n \nc\no\nl\nl\na\np\ns\ne\n \n~\n|")
            self.root.after(100, self.list_box_refresh)
            self.root.geometry('%dx%d' % (LOGIN_RES[0], LOGIN_RES[1]))
            self.right_frame.pack(fill="both", expand=True, side="left", padx=5, pady=5)
            self.sales_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
            self.isCollapsed = False

    def sales_info_frame_refresh(self):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sales")
        records = cursor.fetchall()
        conn.commit()
        conn.close()
        total_income = 0
        for record in records:
            total_income += record[2] * 0.92
        self.total_record_count.configure(text=f"Total: {len(records)} Sales ~ Income: {total_income}₺")

    def sales_list_refresh(self):
        self.last_sales_list.delete("all")
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sales ORDER BY Sales_date DESC")
        sales = cursor.fetchall()
        conn.commit()
        conn.close()
        x = 0
        for sale in sales:
            self.last_sales_list.insert(x,
                                        f"{sale[0]}: {sale[1]} Won {str(sale[2] * 0.92)[0:6]} TL ~ "
                                        f"{str(sale[3])[:16]}")
            x += 1
        self.sales_info_frame_refresh()

    def sales_list_box_clicked(self, selected_option):
        id = ""
        for i in selected_option:
            if i != ":":
                id += str(i)
            else:
                break
        answer = InfoMessage("Would you like to delete this record ?", "Confirm").ask_question("Yes - NO")
        if answer:
            conn = DbConnection().get_conn()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_delete_sale_record_by_id " + id)
            conn.commit()
            conn.close()
            self.sales_list_refresh()

    def submit_sale(self):
        won_amount = self.won_amount_entry.get()
        won_price = self.won_price_entry.get()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"EXEC sp_add_sale {won_amount}, {won_price}")
        conn.commit()
        conn.close()
        self.sales_list_refresh()

    def list_box_clicked(self, selected_option):
        id = ""
        for i in selected_option:
            if i != ":":
                id += str(i)
            else:
                break
        answer = InfoMessage("Would you like to delete this record ?", "Confirm").ask_question()
        if answer:
            conn = DbConnection().get_conn()
            cursor = conn.cursor()
            cursor.execute("EXEC sp_delete_record_by_id " + id)
            conn.commit()
            conn.close()
            self.root.after(10, self.list_box_refresh)

    def event_changer(self):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # self.root.title("Current Event: " + self.current_event + " -- Next Event: " + self.next_event)
        self.event_text.configure(text=self.current_event + " is active / " + self.next_event + " is next")
        self.root.after(100, self.event_changer)

    def clear_list(self):
        answer = InfoMessage("Are you sure you want to clear the list ?",
                             "Confirm").ask_question("Verify your choice")
        if answer:
            conn = DbConnection().get_conn()
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE Killed_Razador_List")
            conn.commit()
            conn.close()
            self.root.after(10, self.list_box_refresh)
            InfoMessage("List has been wiped!", "Info").show_info()
        else:
            pass

    def fill_razador_killed_listBox(self):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Killed_Razador_List ORDER BY When_killed DESC")
        records = cursor.fetchall()
        self.kill_list = records
        now = datetime.today()
        now_day = str(now)[8:10]
        yesterday_day = str(int(now_day) - 1)
        actual_yesterday = str(now)
        x = 0
        yesterday = ""
        for i in actual_yesterday:
            if x == 8:
                yesterday += str(yesterday_day)[0]
            else:
                yesterday += i
            x += 1
        y = 0
        new_yesterday = ""
        if yesterday[8] == "0" and yesterday[9] == "0":
            if yesterday[5] == "0" and yesterday[6] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                for i in yesterday:
                    if y == 6:
                        new_yesterday += "1"
                    elif y == 8:
                        new_yesterday += "3"
                    elif y == 9:
                        new_yesterday += "1"
                    else:
                        new_yesterday += i
                    y += 1
            yesterday = new_yesterday
        cursor.execute(
            f"SELECT * FROM Killed_Razador_List WHERE "
            f"When_killed BETWEEN '{str(now)[:19]}' AND '{str(now)[:19]}'")
        last_24_hours = cursor.fetchall()
        conn.commit()
        conn.close()
        last_24_sum_of_chests = 0
        for i in last_24_hours:
            last_24_sum_of_chests += i[3]
        self.information_text.configure(
            text=f"{str(len(records))} ITEM ~ LAST 24 hr ({len(last_24_hours)})-({last_24_sum_of_chests})")
        place = 0
        sum_of_amount_of_chest = 0
        for record in records:
            min = record[1] // 60
            sec = record[1] % 60
            min_text = ""
            sec_text = ""
            if len(str(min)) == 1:
                min_text = "0" + str(min)
            elif len(str(min)) == 2:
                min_text = str(min)
            if len(str(sec)) == 1:
                sec_text = "0" + str(sec)
            elif len(str(sec)) == 2:
                sec_text = str(sec)
            time_text = str(record[0]) + ": " + "Time : " + str(min_text) + ":" + str(sec_text)
            full_text = time_text + " - Date : " + str(record[2])[5:16] + "~" + str(record[3]) + " Chest"
            self.killed_razador_list.insert(place, full_text)
            place += 1
            # calculating avarage chest drop
            sum_of_amount_of_chest += record[3]
        avarage = str(sum_of_amount_of_chest / len(records))
        self.avarage_of_dropped_chest_label.configure(text=f"Avarage Chest Drop: {avarage[:4]}")

    def list_box_refresh(self):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Killed_Razador_List ORDER BY When_killed DESC")
        records = cursor.fetchall()
        if records != self.kill_list:
            print("Records didn't match. List box have been updated.")
            self.killed_razador_list.delete("all")
            self.kill_list = records
            now = datetime.today()
            now_day = str(now)[8:10]
            yesterday_day = str(int(now_day) - 1)
            actual_yesterday = str(now)
            x = 0
            yesterday = ""
            for i in actual_yesterday:
                if x == 8:
                    yesterday += str(yesterday_day)[0]
                elif x == 9:
                    yesterday += str(yesterday_day)[1]
                else:
                    yesterday += i
                x += 1
            y = 0
            new_yesterday = ""
            if yesterday[8] == "0" and yesterday[9] == "0":
                if yesterday[5] == "0" and yesterday[6] == "2":
                    for i in yesterday:
                        if y == 6:
                            new_yesterday += "1"
                        elif y == 8:
                            new_yesterday += "3"
                        elif y == 9:
                            new_yesterday += "1"
                        else:
                            new_yesterday += i
                        y += 1
                yesterday = new_yesterday
            cursor.execute(
                f"SELECT * FROM Killed_Razador_List"
                f" WHERE When_killed BETWEEN '{str(yesterday)[:19]}' AND '{str(now)[:19]}'")
            last_24_hours = cursor.fetchall()
            conn.commit()
            conn.close()
            last_24_sum_of_chests = 0
            for i in last_24_hours:
                last_24_sum_of_chests += i[3]
            self.information_text.configure(
                text=f"{str(len(records))} ITEM ~ LAST 24 hr ({len(last_24_hours)})-({last_24_sum_of_chests})")
            place = 0
            sum_of_amount_of_chest = 0
            for record in records:
                min = record[1] // 60
                sec = record[1] % 60
                min_text = ""
                sec_text = ""
                if len(str(min)) == 1:
                    min_text = "0" + str(min)
                elif len(str(min)) == 2:
                    min_text = str(min)
                if len(str(sec)) == 1:
                    sec_text = "0" + str(sec)
                elif len(str(sec)) == 2:
                    sec_text = str(sec)
                time_text = str(record[0]) + ": " + "Time : " + str(min_text) + ":" + str(sec_text)
                full_text = time_text + " - Date : " + str(record[2])[5:16] + "~" + str(record[3]) + " Chest"
                self.killed_razador_list.insert(place, full_text)
                place += 1
                # calculating avarage chest drop
                sum_of_amount_of_chest += record[3]
            avarage = str(sum_of_amount_of_chest / len(records))
            self.avarage_of_dropped_chest_label.configure(text=f"Avarage Chest Drop: {avarage[:4]}")
        else:
            print("Records are matched. No need to refresh the listbox")

    def add_record_to_razador_killed(self, chest_count):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_add_record_to_razador_killed " + str(self.last_stopwatch_duration) + ", " + chest_count)
        cursor.execute("SELECT GETDATE()")
        date = cursor.fetchone()
        conn.commit()
        conn.close()
        if not self.isCollapsed:
            self.root.after(100, self.list_box_refresh)
        else:
            print("Due to collapsed state, list box haven't refreshed")
        self.collapse()
        self.collapse()

    def start_and_stop_stopwatch(self):
        if self.isCountdownRunning == True:
            answer = InfoMessage(
                "You can't start a session..\n while razador CoolDown ON \n"
                " Would you like to terminate CoolDown-CountDown ?",
                "Confirm").ask_question("Razador Countdown ON!")
            if answer:
                self.isCountdownRunning = False
                self.start_stop_button.configure(text="End Razador Session")
                self.timer_text.configure(text="Next Razador Session \n Countdown\n Terminated", text_color="red",
                                          font=("Roboto", 20, "bold"))
                self.sayac_suresi = (60 * self.minute) + 1
                self.kac_kez_caldi = 0
        else:
            if not self.isStopwatchRunning:
                self.stopwatch_duration = -1
                self.isStopwatchRunning = True
                self.start_and_stop_stopwatch_button.configure(text="Stop Razador Session Duration")
                self.update_stopwatch()
            else:
                self.isStopwatchRunning = False
                self.start_and_stop_stopwatch_button.configure(text="Start Razador Session")
                self.last_stopwatch_duration = self.stopwatch_duration
                self.last_stopwatch_duration_text.configure(
                    text=f"Last Razador Duration: {self.last_stopwatch_duration // 60} min and"
                         f" {self.last_stopwatch_duration % 60} sec")

    def update_stopwatch(self):
        if self.isStopwatchRunning:
            self.stopwatch_duration = self.stopwatch_duration + 1
            dakika = self.stopwatch_duration // 60
            saniye = self.stopwatch_duration % 60
            for x in str(dakika):
                if x != ".":
                    self.minute_will_be_shown += x
                else:
                    break
            for y in str(saniye):
                if y != ".":
                    self.second_will_be_shown += y
                else:
                    break
            if self.stopwatch_duration >= 60:
                self.timer_text.configure(text=f"{self.minute_will_be_shown}' {self.second_will_be_shown}''",
                                          text_color="white", font=("Roboto", 80, "bold"))
            else:
                self.timer_text.configure(text=f"{self.second_will_be_shown}''", text_color="white",
                                          font=("Roboto", 80, "bold"))
            self.minute_will_be_shown = ""
            self.second_will_be_shown = ""
            self.root.after(1000, self.update_stopwatch)

    def start_stop_timer(self):
        if self.isStopwatchRunning:
            self.isStopwatchRunning = False
            self.start_and_stop_stopwatch_button.configure(text="Start Razador Session")
            self.last_stopwatch_duration = self.stopwatch_duration
            self.last_stopwatch_duration_text.configure(
                text=f"Last Razador Duration: {self.last_stopwatch_duration // 60} min"
                     f" and {self.last_stopwatch_duration % 60} sec")
        if self.isCountdownRunning == False:
            if self.last_stopwatch_duration > 0:
                self.isCountdownRunning = True
                self.start_stop_button.configure(text="Stop Razador CoolDown CountDown")
                self.last_stopwatch_duration_text.configure(
                    text=f"Last Razador Duration: {self.last_stopwatch_duration // 60} min"
                         f" and {self.last_stopwatch_duration % 60} sec")
                self.update_timer()
                coor_x = (self.ws / 2) - (350 / 2)
                coor_y = (self.hs / 2) - (200 / 2)
                chest = customtkinter.CTkInputDialog(title="How many chest dropped ?",
                                                     text="Please chose the number of chests you have just dropped.",
                                                     isCombo=True,
                                                     comboValues=["8", "9", "10"])
                chest.geometry('%dx%d+%d+%d' % (350, 200, coor_x, coor_y))
                chest_count = chest.get_input()
                if chest_count in (["8", "9", "10"]):
                    self.add_record_to_razador_killed(chest_count)
                else:
                    InfoMessage("You have not chose any ! \n You've lost your record !", "Info").show_error(
                        "Blank Error!!")
            else:
                InfoMessage("You didn't count the Razador session duration!", "Info").show_error("Error")
        else:
            self.isCountdownRunning = False
            self.start_stop_button.configure(text="End Razador Session")
            self.timer_text.configure(text="Countdown\n Terminated", text_color="yellow")
            self.sayac_suresi = (60 * self.minute) + 1

    def update_timer(self):
        if self.isCountdownRunning:
            if self.sayac_suresi > 0:
                self.sayac_suresi = self.sayac_suresi - 1
                dakika = self.sayac_suresi // 60
                saniye = self.sayac_suresi % 60
                if (20 <= dakika < 30):
                    self.timer_text.configure(text=f" Next Razador \n in \n {int(dakika)}' {int(saniye)}''",
                                              text_color="#59FF00", font=("Roboto", 40, "bold"))
                elif (10 <= dakika < 20):
                    self.timer_text.configure(text=f"Next Razador \n in \n {int(dakika)}' {int(saniye)}''",
                                              text_color="#FFB600", font=("Roboto", 40, "bold"))
                elif (0 < dakika < 10):
                    self.timer_text.configure(text=f"Next Razador \n in \n {int(dakika)}' {int(saniye)}''",
                                              text_color="#FF0000", font=("Roboto", 40, "bold"))
                elif (dakika == 0 and 0 < saniye < 60):
                    self.timer_text.configure(text=f"Next Razador \n in \n {int(saniye)}''", text_color="red",
                                              font=("Roboto", 40, "bold"))
                self.root.after(1000, self.update_timer)
            elif self.sayac_suresi == 0:
                self.timer_text.configure(text="Razador Time !", text_color="white", font=("Roboto", 40, "bold"))
                self.isAlarmRunning = True
                self.isCountdownRunning = False
                self.start_stop_button.configure(text="End Razador Session")
                notification.notify(
                    title="Metin2 Helper",
                    message="Razador Cooldown Time Finished",
                    timeout=3,
                )
                self.razador_sound.play()
                self.sayac_suresi = (60 * self.minute) + 1

    def onclosing(self):
        self.exit_sound.play()
        self.destroy()
    
    def destroy(self):
        time.sleep(1)
        self.root.destroy()

    # def sound_player(self):
    #     if self.isAlarmRunning:
    #         self.isAlarmRunning = True
    #         if self.kac_kez_caldi < 3:
    #             self.sound.play()
    #             self.kac_kez_caldi += 1
    #             self.root.after(3333, self.sound_player)
    #         else:
    #             self.isAlarmRunning = False
    #             self.start_stop_button.configure(text="End Razador Session")
    #             self.isAlarmRunning = False
    #             self.sound.stop()
    #             self.sayac_suresi = (60 * self.minute) + 1
    #             self.kac_kez_caldi = 0


class DbConnection:
    def __init__(self, db_type="local"):
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


class InfoMessage:
    def __init__(self, msg, title):
        self.msg = msg
        self.title = title

    def show_info(self):
        CTkMessagebox(title=self.title, message=self.msg, width=WIDTH, height=HEIGHT, title_color="green", icon=None,font=("Roboto",14),text_color="white")

    def show_checkmark(self):
        CTkMessagebox(message=self.msg,
                      icon="check", option_1="Thanks", width=WIDTH, height=HEIGHT)

    def show_error(self, title):
        CTkMessagebox(title=title, message=self.msg, icon="cancel", width=WIDTH, height=HEIGHT)

    def ask_question(self):
        shown_message = CTkMessagebox(title=self.title, message=self.msg,
                                      icon="question", option_1="Forget it", option_2="No", option_3="Yes")
        response = shown_message.get()

        if response == "Yes":
            return True
        else:
            return False



if __name__ == "__main__":
    app = Metin2Helper()
    app.root.protocol("WM_DELETE_WINDOW", app.onclosing)
    app.root.mainloop()
