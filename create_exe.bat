pyinstaller --noconfirm --onedir --windowed --icon "D:/EVERYTHING/My_Future/Python/gficon.ico" --add-data "D:/EVERYTHING/My_Future/Python/_internal/event_notification.wav;." --add-data "D:/EVERYTHING/My_Future/Python/_internal/exit_notification.wav;." --add-data "D:/EVERYTHING/My_Future/Python/_internal/gficon.ico;." --add-data "D:/EVERYTHING/My_Future/Python/_internal/razador_notification.wav;." --hidden-import "plyer.platforms.win.notification"  "D:/EVERYTHING/My_Future/Python/Metin2Helper.py"