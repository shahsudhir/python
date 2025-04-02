from tkinter import Tk, Entry, Button, StringVar  # Import necessary widgets and classes from tkinter module

class Calculator:  # Define a class named Calculator to encapsulate the calculator functionality
    def __init__(self, master):  # Constructor method, takes 'master' (the main window) as an argument
        master.title("Calculator")  # Set the title of the window to "Calculator"
        master.geometry('357x420+0+0')  # Set the window size to 357x420 pixels and position it at (0,0) on the screen
        master.config(bg='gray')  # Set the background color of the window to gray
        master.resizable(False, False)  # Disable resizing of the window (width and height are fixed)

        self.equation = StringVar()  # Create a StringVar object to hold and update the display value dynamically
        self.entry_value = ''  # Initialize an empty string to store the current input/equation
        Entry(width=17, bg='#fff', font=('Arial Bold', 28), textvariable=self.equation).place(x=0, y=0)  # Create an Entry widget for displaying the equation, with width 17, white background, Arial Bold font size 28, linked to self.equation, placed at (0,0)

        # Create buttons for calculator operations and digits, each with a command to call the 'show' method with the respective value
        Button(width=17, height=4, text='(', relief='flat', bg='white', command=lambda: self.show('(')).place(x=0, y=50)  # '(' button at (0,50)
        Button(width=17, height=4, text=')', relief='flat', bg='white', command=lambda: self.show(')')).place(x=90, y=50)  # ')' button at (90,50)
        Button(width=17, height=4, text='%', relief='flat', bg='white', command=lambda: self.show('%')).place(x=180, y=50)  # '%' button at (180,50)
        Button(width=17, height=4, text='1', relief='flat', bg='white', command=lambda: self.show(1)).place(x=0, y=125)  # '1' button at (0,125)
        Button(width=17, height=4, text='2', relief='flat', bg='white', command=lambda: self.show(2)).place(x=90, y=125)  # '2' button at (90,125)
        Button(width=17, height=4, text='3', relief='flat', bg='white', command=lambda: self.show(3)).place(x=180, y=125)  # '3' button at (180,125)
        Button(width=17, height=4, text='4', relief='flat', bg='white', command=lambda: self.show(4)).place(x=0, y=200)  # '4' button at (0,200)
        Button(width=17, height=4, text='5', relief='flat', bg='white', command=lambda: self.show(5)).place(x=90, y=200)  # '5' button at (90,200)
        Button(width=17, height=4, text='6', relief='flat', bg='white', command=lambda: self.show(6)).place(x=180, y=200)  # '6' button at (180,200)
        Button(width=17, height=4, text='7', relief='flat', bg='white', command=lambda: self.show(7)).place(x=0, y=275)  # '7' button at (0,275)
        Button(width=17, height=4, text='8', relief='flat', bg='white', command=lambda: self.show(8)).place(x=180, y=275)  # '8' button at (180,275) - Note: Positioning seems inconsistent (should be x=90?)
        Button(width=17, height=4, text='9', relief='flat', bg='white', command=lambda: self.show(9)).place(x=90, y=275)  # '9' button at (90,275)
        Button(width=17, height=4, text='0', relief='flat', bg='white', command=lambda: self.show(0)).place(x=90, y=350)  # '0' button at (90,350)
        Button(width=17, height=4, text='.', relief='flat', bg='white', command=lambda: self.show('.')).place(x=180, y=350)  # '.' button at (180,350)
        Button(width=17, height=4, text='+', relief='flat', bg='white', command=lambda: self.show('+')).place(x=270, y=350)  # '+' button at (270,350)
        Button(width=17, height=4, text='-', relief='flat', bg='white', command=lambda: self.show('-')).place(x=270, y=200)  # '-' button at (270,200)
        Button(width=17, height=4, text='/', relief='flat', bg='white', command=lambda: self.show('/')).place(x=270, y=50)  # '/' button at (270,50)
        Button(width=17, height=4, text='*', relief='flat', bg='white', command=lambda: self.show('*')).place(x=270, y=125)  # '*' button at (270,125)
        Button(width=17, height=4, text='=', relief='flat', bg='white', command=self.solve).place(x=270, y=350)  # '=' button at (270,350) - Calls solve method directly (no lambda needed)
        Button(width=17, height=4, text='C', relief='flat', command=self.clear).place(x=0, y=350)  # 'C' (clear) button at (0,350) - Calls clear method directly

    def show(self, value):  # Method to append a value to the current equation and update the display
        self.entry_value += str(value)  # Append the input value (converted to string) to entry_value
        self.equation.set(self.entry_value)  # Update the StringVar to reflect the new value in the Entry widget

    def clear(self):  # Method to reset the calculator
        self.entry_value = ''  # Reset entry_value to an empty string
        self.equation.set(self.entry_value)  # Update the display to show an empty string

    def solve(self):  # Method to evaluate the equation and display the result
        result = eval(self.entry_value)  # Evaluate the string expression in entry_value (e.g., "2+3" becomes 5)
        self.equation.set(result)  # Update the display with the result

root = Tk()  # Create the main application window (Tk instance)
Calculator = Calculator(root)  # Instantiate the Calculator class, passing the root window as the master
root.mainloop()  # Start the Tkinter event loop to display the window and handle interactions