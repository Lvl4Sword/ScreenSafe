import subprocess
import sys
import time

FREEDESKTOP_SCREENSAVER = ['dbus-send',
                           '--session',
                           '--dest=org.freedesktop.ScreenSaver',
                           '--type=method_call',
                           '--print-reply',
                           '--reply-timeout=1000',
                           '/ScreenSaver',
                           'org.freedesktop.ScreenSaver.GetActive']
GNOME_SCREENSAVER = ['dbus-send',
                     '--session',
                     '--dest=org.gnome.ScreenSaver',
                     '--type=method_call',
                     '--print-reply',
                     '--reply-timeout=1000',
                     '/ScreenSaver',
                     'org.gnome.ScreenSaver.GetActive']
GNOME3_SCREENSAVER = ['dbus-send',
                      '--session',
                      '--dest=org.gnome.ScreenSaver',
                      '--type=method_call',
                      '--print-reply',
                      '--reply-timeout=1000',
                      '/org/gnome/ScreenSaver',
                      'org.gnome.ScreenSaver.GetActive']
KDE_SCREENSAVER = ['dbus-send',
                   '--session',
                   '--dest=org.kde.screensaver',
                   '--type=method_call',
                   '--print-reply',
                   '--reply-timeout=1000',
                   '/ScreenSaver',
                   'org.freedesktop.ScreenSaver.GetActive']
SCREENSAVERS = {'FREEDESKTOP_SCREENSAVER': {'command': FREEDESKTOP_SCREENSAVER},
                'GNOME_SCREENSAVER': {'command': GNOME_SCREENSAVER},
                'GNOME3_SCREENSAVER': {'command': GNOME3_SCREENSAVER},
                'KDE_SCREENSAVER': {'command': KDE_SCREENSAVER}}


class Main:
    def __init__(self):
        self.locked = None
        self.linux_screensaver_command = GNOME3_SCREENSAVER

    def detect_lock_screen(self):
        if sys.platform.startswith('win'):
            self.detect_windows()
        elif sys.platform.startswith('linux'):
            self.detect_linux()
        elif sys.platform.startswith('darwin'):
            self.detect_mac()
        else:
            print("NO CLUE WHAT SYSTEM YOU'RE RUNNING BUT IT'S NOT SUPPORTED.")
            sys.exit()

    def detect_windows(self):
        import ctypes
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        result = user32.GetForegroundWindow()
        if result == 0:
            self.locked = True
        else:
            self.locked = False

    def detect_linux(self):
        try:
            check_screensaver = subprocess.check_output(self.linux_screensaver_command).decode().split()[-1]
        except TypeError:
            self.detect_linux_screensaver_command()
        else:
            if check_screensaver == 'true':
                self.locked = True
            elif check_screensaver == 'false':
                self.locked = False
            else:
                print('---------------------------------------------------')
                print('---------------------------------------------------')
                print('---------------------------------------------------')
                print('The screensaver command is giving unexpected output')
                print('----- If you\'re: having issues with setup or -----')
                print('-------- something isn\'t working properly --------')
                print('------------------ file an issue: -----------------')
                print('- https://github.com/Lvl4Sword/ScreenSafe/issues --')
                print('---------------------------------------------------')
                print('---------------------------------------------------')
                print('---------------------------------------------------')
                print('Killing program..')
                sys.exit()

    def detect_linux_screensaver_command(self):
        self.linux_screensaver_command = None
        for x, y in enumerate(SCREENSAVERS):
            try:
                the_command = SCREENSAVERS[y]['command']
                the_output = subprocess.check_output(the_command).decode().split()[-1]
                if the_output in ['false', 'true']:
                    self.linux_screensaver_command = the_command
                    the_name = f' {y} '
                    print('---------------------------------------------------')
                    print('---------------------------------------------------')
                    print('---------------------------------------------------')
                    print('----- The following has been detected as your -----')
                    print('--------------- screensaver command: --------------')
                    print('{:-^51}'.format(the_name))
                    print('---------------------------------------------------')
                    print('---------------------------------------------------')
                    print('---------------------------------------------------')
            except Exception:
                pass
        if self.linux_screensaver_command is None:
            print('---------------------------------------------------')
            print('---------------------------------------------------')
            print('---------------------------------------------------')
            print('The correct screensaver command could not be found.')
            print('-- Please disable ScreenSafe and file an issue: ---')
            print('- https://github.com/Lvl4Sword/ScreenSafe/issues --')
            print('---------------------------------------------------')
            print('---------------------------------------------------')
            print('---------------------------------------------------')
            print('Killing program..')
            sys.exit()

    def detect_mac(self):
        import Quartz
        session_dict = Quartz.CGSessionCopyCurrentDictionary()
        if 'CGSSessionScreenIsLocked' in session_dict.keys():
            self.locked = True
        else:
            self.locked = False

    def check_lock(self):
        current_time = time.strftime('%Y-%m-%d %I:%M:%S%p', time.localtime())
        if not self.locked:
            self.detect_lock_screen()
            if self.locked:
                print(f'System locked at {current_time}')
        if self.locked:
            self.detect_lock_screen()
            if not self.locked:
                print(f'System unlocked at {current_time}')
        time.sleep(1)


disco = Main()
Main().detect_lock_screen()
the_current_time = time.strftime('%Y-%m-%d %I:%M:%S%p', time.localtime())
if disco.locked:
    print(f'Program started. System locked at {the_current_time}')
else:
    print(f'Program started. System unlocked at {the_current_time}')

while True:
    disco.check_lock()
