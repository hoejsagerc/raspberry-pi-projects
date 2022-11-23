import curses
import requests
import time
import socket


class DisplayTopBox():
    """
        Class for controlling and defining the top display
        the top display will show general information on the cluster
        such as if it has internet access and if it is degraded or working on full
    """
    def __init__(self, width, height, top):
        self.width = width # width of the window
        self.height = height # height of the window
        self.top = top # how far from the top should the window be displayed
        #self.top = (curses.LINES - height) // 2  <-- if you want to display in the middle of screen
        left = (curses.COLS - self.width) // 2  # this will display the window in the middle of the terminal screen
        self.win = curses.newwin(self.height, self.width, self.top, left) # creating the window
        self.win.refresh() # refresh the window to display the window


    def display_box(self):
        """
            Method for defining the top window of the application
            This window will display if the cluster has internet connection, what the WAN ip address is and what the Local ip address is
            It will also display the state of the cluster wether it is up, degraded or down
        """
        self.win.border()
        self.win.addstr(1, 2, 'UPTIME', curses.A_STANDOUT)
        self.win.addstr(1, 11, 'INTERNET:', curses.A_STANDOUT)
        self.win.addstr(1, 44, 'SYSTEM:', curses.A_STANDOUT)
        self.win.addstr(2, 2, 'WAN_IP', curses.A_BOLD)
        self.win.addstr(2, 14, 'LOCAL_IP', curses.A_BOLD)
        self.win.refresh()


    def find_internet_state(self):
        url="https://google.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            return "online"
        except (requests.ConnectionError, requests.Timeout) as exception:
            return "offline"


    def set_internet_state(self):
        """
            method for adding the INTERNET online or offline state in the top box
        """
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        GREEN_AND_BLACK = curses.color_pair(1)
        RED_AND_BLACK = curses.color_pair(2)

        while True:
            internet_state = self.find_internet_state()

            if internet_state == 'online':
                self.win.addstr(1, 26, f'connected   ', GREEN_AND_BLACK)
            elif internet_state == 'offline':
                self.win.addstr(1, 26, f'disconnected', RED_AND_BLACK)
            
            self.win.refresh()
            time.sleep(1.5)


    def find_ip_address(self,):
        """
            method for finding the wan and lan ip address of the infrastructure node
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr=socket.gethostbyname(socket.gethostname())
        s.close()

        return ip_addr


    def set_ip_address(self, local_ip):
        """
            method for displaying the wan ip address and local ip address in the top window
        """
        wan_ip = self.find_ip_address()
        self.win.addstr(2, 10, f'{wan_ip}')
        self.win.addstr(2, 24, f'{local_ip}')
        self.win.refresh()



class DisplayMainBox():
    """
        class for controlling and defining the main display
        the main display will show an info screen with stats on all the different
        raspberry pi's
    """
    def __init__(self, width, height, top):
        self.width = width 
        self.height = height 
        self.top = top 
        left = (curses.COLS - self.width) // 2
        self.win = curses.newwin(self.height, self.width, self.top, left) 
        self.win.refresh() 


    def display_box(self):
        """
            method for displaying the main box. The main box will display up to 6 raspberry pi nodes
        """
        self.win.border()
        self.win.addst