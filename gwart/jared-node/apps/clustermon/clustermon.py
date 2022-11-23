import threading
import time
import json
from clustermon.DisplayWindows import *
import curses
from curses import wrapper

node_one_ip = '10.13.37.10'
node_one_name = 'jared00'
node_two_ip = '10.13.37.20'
node_two_name = 'jared01'
node_three_ip = '10.13.37.30'
node_three_name = 'jared02'
node_four_ip = '10.13.37.40'
node_four_name = 'jared03'
node_five_ip = '10.13.37.50'
node_five_name = 'jared04'
node_six_ip = '10.13.37.60'
node_six_name = 'jared05'

def main(stdscr):
    #* INITIALIZE SCREEN
    stdscr.clear()
    stdscr.refresh()

    #* COlORS
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)
    RED_AND_BLACK = curses.color_pair(2)
    YELLOW_AND_BLACK = curses.color_pair(3)


    #* DEFINING TOP WINDOW
    window_width = 60
    window_height = 4
    window_top = 1
    
    # initiating the top window
    tb = DisplayTopBox(window_width, window_height, window_top)
    tb.display_box()

    # creating thread for checking if the cluster has access to the internet
    thread = threading.Thread(target=tb.set_internet_state()) 
    thread.start()

    tb.set_ip_address(f'{node_one_ip}')



    stdscr.getch()



if __name__ == '__main__':
    wrapper(main)