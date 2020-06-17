
# Run Program
#   Used to run the note-taking program


# Local Modules
import review

# NonLocal Modules
import curses



def run(win):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    win.nodelay(True)
    review.main(win)

curses.wrapper(run)


# Free Software
