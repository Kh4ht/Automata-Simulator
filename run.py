# region IMPORTS


from automata_simulator_gui import AutomataSimulatorGUI
import tkinter as tk

# endregion
#################################################################################

#################################################################################
# region RUN


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataSimulatorGUI(root)
    root.mainloop()


# endregion
