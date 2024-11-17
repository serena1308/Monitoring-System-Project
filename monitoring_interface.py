#!/usr/bin/env python3

import curses
import csv
import os
import textwrap

def display_metrics(stdscr):

    # colors initialization
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    colors = [curses.color_pair(i) for i in range(1, 8)]

    # List of files and titles
    metric_files = [
        ("CPU Load/ Uptime", "cpu_load.csv"),
        ("Top Memory Processes", "memory_process.csv"),
        ("Top CPU Processes", "cpu_process.csv"),
        ("Memory Usage", "memory_usage.csv"),
        ("Disk Usage", "disk_usage.csv"),
        ("Recent Logins", "recent_logins.csv"),
        ("Authentication Log Activity", "auth_log_activity.csv"),
        ("Network Traffic", "network_traffic.csv"),
        ("System Log Activity", "sys_log_activity.csv")
    ]

    # Read date and IP
    try:
        with open("date_ip.csv", 'r') as file:
            reader = csv.reader(file)
            date_ip = next(reader)
            date_str, user_ip = date_ip
    except FileNotFoundError:
        date_str, user_ip = "N/A", "N/A"

    # Display general title and date/IP
    stdscr.clear()
    stdscr.addstr(0, 0, "System Monitoring Metrics - ( press 'q' for exit )", curses.A_BOLD | curses.color_pair(5))
    stdscr.addstr(2, 0, f"Monitoring started at {date_str} from IP address {user_ip}.", curses.color_pair(7))
    stdscr.refresh()

    # Window size and placement
    term_height, term_width = stdscr.getmaxyx()
    num_columns = 3
    box_width = max(term_width // num_columns, 20)
    box_height = 15  

    # Metric block display
    for idx, (title, filename) in enumerate(metric_files):
        row = idx // num_columns
        col = idx % num_columns
        y = 3 + row * box_height
        x = col * box_width

        # Creating a window for each metric
        try:
            win = curses.newwin(box_height, box_width, y, x)

            color = colors[idx % len(colors)]
            win.attron(color)
            win.box()  
            win.attroff(color)

            # Display window title
            title_x = max(1, (box_width - len(title)) // 2)
            win.addstr(1, title_x, title, curses.A_BOLD | color)

            # Load and display the contents of the metrics file
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    lines = f.readlines()

                current_y = 2  # Start line in window
                for line in lines:
                    wrapped_lines = textwrap.wrap(line.strip(), width=box_width - 2)  # Word wrap
                    for wrapped_line in wrapped_lines:
                        if current_y < box_height - 1:  # Save space for the border
                            win.addstr(current_y, 1, wrapped_line)
                            current_y += 1
                        else:
                            break
            else:
                win.addstr(2, 1, "File not found.")

            win.refresh()
        except curses.error as e:
            stdscr.addstr(term_height - 1, 0, f"Erreur affichage {title}: {e}", curses.color_pair(7))

    # Main loop to exit with 'q
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def main():
    curses.wrapper(display_metrics)

if __name__ == "__main__":
    main()
