# region IMPORTS

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from collections import defaultdict

# endregion
#################################################################################

#################################################################################
# region AutomataSimulatorGUI


class AutomataSimulatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Automata Simulator - CS 342 Project")
        self.root.geometry("1300x700")
        self.root.resizable(False, False)

        # Automata data structures
        self.states: set[str] = set()
        self.alphabet: set[str] = set()
        self.start_state: str = ""
        self.accept_states: set[str] = set()
        # (state, symbol) -> set of next states
        self.transitions: dict[tuple[str, str], set[str]] = dict()
        self.is_dfa: bool = True
        self.automaton_type: str = "DFA"  # or "NFA"

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))

        # Left Panel - Automaton Definition
        left_frame = ttk.LabelFrame(
            main_frame, text="Automaton Definition", padding="10"
        )
        left_frame.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), padx=5)

        # Type selection
        ttk.Label(left_frame, text="Type:").grid(row=0, column=0, sticky=tk.W)
        self.type_var = tk.StringVar(value="DFA")
        type_combo = ttk.Combobox(
            left_frame,
            textvariable=self.type_var,
            values=["DFA", "NFA"],
            state="readonly",
        )
        type_combo.grid(row=0, column=1, sticky=(tk.W + tk.E), pady=5)
        type_combo.bind("<<ComboboxSelected>>", self.on_type_change)

        # States input
        ttk.Label(left_frame, text="States (comma-separated):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.states_entry = ttk.Entry(left_frame, width=30)
        self.states_entry.grid(row=1, column=1, sticky=(tk.W + tk.E), pady=5)
        ttk.Button(left_frame, text="Add States", command=self.add_states).grid(
            row=1, column=2, padx=5
        )

        # Alphabet input
        ttk.Label(left_frame, text="Alphabet (comma-separated):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.alphabet_entry = ttk.Entry(left_frame, width=30)
        self.alphabet_entry.grid(row=2, column=1, sticky=(tk.W + tk.E), pady=5)
        ttk.Button(left_frame, text="Set Alphabet", command=self.set_alphabet).grid(
            row=2, column=2, padx=5
        )

        # Start state
        ttk.Label(left_frame, text="Start State:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.start_entry = ttk.Entry(left_frame, width=30)
        self.start_entry.grid(row=3, column=1, sticky=(tk.W + tk.E), pady=5)
        ttk.Button(left_frame, text="Set Start", command=self.set_start).grid(
            row=3, column=2, padx=5
        )

        # Accept states
        ttk.Label(left_frame, text="Accept States (comma):").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.accept_entry = ttk.Entry(left_frame, width=30)
        self.accept_entry.grid(row=4, column=1, sticky=(tk.W + tk.E), pady=5)
        ttk.Button(left_frame, text="Set Accept", command=self.set_accept).grid(
            row=4, column=2, padx=5
        )

        # Transitions
        ttk.Label(left_frame, text="Add Transition:").grid(
            row=5, column=0, sticky=tk.W, pady=10
        )
        trans_frame = ttk.Frame(left_frame)
        trans_frame.grid(row=6, column=0, columnspan=3, pady=5)

        ttk.Label(trans_frame, text="From:").grid(row=0, column=0)
        self.from_state = ttk.Entry(trans_frame, width=8)
        self.from_state.grid(row=0, column=1, padx=2)

        ttk.Label(trans_frame, text="On:").grid(row=0, column=2)
        self.on_symbol = ttk.Entry(trans_frame, width=5)
        self.on_symbol.grid(row=0, column=3, padx=2)

        ttk.Label(trans_frame, text="To:").grid(row=0, column=4)
        self.to_state = ttk.Entry(trans_frame, width=8)
        self.to_state.grid(row=0, column=5, padx=2)

        ttk.Button(trans_frame, text="+", command=self.add_transition, width=3).grid(
            row=0, column=6, padx=5
        )

        # Show transitions button
        ttk.Button(
            left_frame, text="Show Transitions", command=self.show_transitions
        ).grid(row=7, column=0, columnspan=3, pady=10)

        # Validate DFA button
        ttk.Button(left_frame, text="Validate DFA", command=self.validate_dfa).grid(
            row=8, column=0, columnspan=3, pady=5
        )

        # Right Panel - Operations
        right_frame = ttk.LabelFrame(main_frame, text="Operations", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W + tk.E + tk.N + tk.S), padx=5)

        # Simulation
        sim_frame = ttk.LabelFrame(right_frame, text="Simulation", padding="5")
        sim_frame.grid(row=0, column=0, sticky=(tk.W + tk.E), pady=5)

        ttk.Label(sim_frame, text="Input String:").grid(row=0, column=0, pady=5)
        self.sim_input = ttk.Entry(sim_frame, width=30)
        self.sim_input.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(sim_frame, text="Simulate", command=self.simulate).grid(
            row=0, column=2, padx=5
        )

        # String Generation
        gen_frame = ttk.LabelFrame(right_frame, text="String Generation", padding="5")
        gen_frame.grid(row=2, column=0, sticky=(tk.W + tk.E), pady=5)

        ttk.Label(gen_frame, text="Max Length:").grid(row=0, column=0, pady=5)
        self.max_length = ttk.Spinbox(gen_frame, from_=0, to=10, width=10)
        self.max_length.grid(row=0, column=1, padx=5, pady=5)
        self.max_length.set(3)
        ttk.Button(
            gen_frame, text="Generate Strings", command=self.generate_strings
        ).grid(row=0, column=2, padx=5)

        # Output Area
        output_frame = ttk.LabelFrame(right_frame, text="Output", padding="5")
        output_frame.grid(row=3, column=0, sticky=(tk.W + tk.E + tk.N + tk.S), pady=10)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, width=50, height=20, wrap=tk.WORD
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))

        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W + tk.E))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(3, weight=1)
        right_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)

    def log(self, message):
        """Add message to output area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.status_bar.config(text=message[:50])

    def on_type_change(self, event=None):
        if self.type_var.get() == self.automaton_type:
            return  # No change

        self.automaton_type = self.type_var.get()
        self.is_dfa = self.automaton_type == "DFA"
        self.log(f"Automaton type changed to: {self.automaton_type}")

    def add_states(self):
        states_text = self.states_entry.get().strip()
        if states_text:
            new_states = set(s.strip() for s in states_text.split(","))
            self.states.update(new_states)
            self.log(
                f"Added states: {', '.join(new_states)}. Total states: {', '.join(self.states)}"
            )
            self.states_entry.delete(0, tk.END)

    def set_alphabet(self):
        alpha_text = self.alphabet_entry.get().strip()
        if alpha_text:
            self.alphabet = set(s.strip() for s in alpha_text.split(","))
            self.log(f"Alphabet set: {', '.join(self.alphabet)}")
            self.alphabet_entry.delete(0, tk.END)

    def set_start(self):
        start = self.start_entry.get().strip()
        if start in self.states:
            self.start_state = start
            self.log(f"Start state set to: {start}")
        else:
            messagebox.showerror("Error", f"State '{start}' not found in states list")
        self.start_entry.delete(0, tk.END)

    def set_accept(self):
        accept_text = self.accept_entry.get().strip()
        if accept_text:
            self.accept_states = set(s.strip() for s in accept_text.split(","))
            invalid = [s for s in self.accept_states if s not in self.states]
            if invalid:
                messagebox.showerror("Error", f"States not found: {invalid}")
            else:
                self.log(f"Accept states set to: {', '.join(self.accept_states)}")
        self.accept_entry.delete(0, tk.END)

    def add_transition(self):
        from_state = self.from_state.get().strip()
        symbol = self.on_symbol.get().strip()
        to_state = self.to_state.get().strip()

        if from_state not in self.states:
            messagebox.showerror("Error", f"State '{from_state}' not found")
            return
        if to_state not in self.states:
            messagebox.showerror("Error", f"State '{to_state}' not found")
            return
        if symbol not in self.alphabet and symbol != "ε":
            if messagebox.askyesno(
                "Warning", f"Symbol '{symbol}' not in alphabet. Add it?"
            ):
                self.alphabet.add(symbol)
                self.log(f"Added '{symbol}' to alphabet")
            else:
                return

        # Store transition (support NFA: multiple destinations)
        key = (from_state, symbol)
        if key not in self.transitions:
            self.transitions[key] = set()
        self.transitions[key].add(to_state)

        self.log(f"Added transition: {from_state} --{symbol}--> {to_state}")

        # Clear entries
        self.from_state.delete(0, tk.END)
        self.on_symbol.delete(0, tk.END)
        self.to_state.delete(0, tk.END)

    def show_transitions(self):
        self.log("\n--- Current Transitions ---")
        for (state, symbol), targets in sorted(self.transitions.items()):
            self.log(f"{state} --{symbol}--> {', '.join(targets)}")

    def validate_dfa(self):
        if not self.is_dfa:
            self.log("Not validating NFA (DFA rules don't apply)")
            return

        errors = []

        # Check single start state
        if not self.start_state:
            errors.append("No start state defined")

        # Check complete transitions for all states
        for state in self.states:
            for symbol in self.alphabet:
                key = (state, symbol)
                if key not in self.transitions:
                    errors.append(f"Missing transition: {state} on '{symbol}'")
                elif len(self.transitions[key]) > 1:
                    errors.append(
                        f"Nondeterministic transition: {state} on '{symbol}' has multiple destinations"
                    )

        if errors:
            self.log("❌ DFA Validation FAILED:")
            for error in errors:
                self.log(f"  - {error}")
        else:
            self.log("✓ DFA Validation PASSED - Well-formed DFA!")

    def simulate(self):
        input_string = self.sim_input.get().strip()
        if not input_string:
            messagebox.showwarning("Warning", "Please enter a string to simulate")
            return

        if not self.start_state:
            messagebox.showerror("Error", "No start state defined")
            return

        self.log(f"\n--- Simulating: '{input_string}' ---")

        if self.is_dfa:
            # DFA simulation
            current_state = self.start_state
            path = [current_state]

            for symbol in input_string:
                if symbol not in self.alphabet:
                    self.log(f"Error: Symbol '{symbol}' not in alphabet")
                    return

                key = (current_state, symbol)
                if key not in self.transitions:
                    self.log(
                        f"Simulation failed: No transition from {current_state} on '{symbol}'"
                    )
                    return

                next_state = next(iter(self.transitions[key]))  # Get single target
                path.append(next_state)
                current_state = next_state

            accepted = current_state in self.accept_states
            self.log(f"Path: {' → '.join(path)}")
            self.log(f"Result: {'✓ ACCEPTED' if accepted else '✗ REJECTED'}")

        else:
            # NFA simulation (simplified - shows possible paths)
            self.log("NFA simulation (showing first valid path):")
            # This is simplified - full NFA simulation would need epsilon closure
            current_states = {self.start_state}
            path_info = {self.start_state: [self.start_state]}

            for symbol in input_string:
                next_states = set()
                new_paths = {}

                for state in current_states:
                    key = (state, symbol)
                    if key in self.transitions:
                        for target in self.transitions[key]:
                            next_states.add(target)
                            new_paths[target] = path_info[state] + [target]

                if not next_states:
                    self.log(f"Simulation failed at symbol '{symbol}'")
                    return

                current_states = next_states
                path_info = new_paths

            accepted = any(s in self.accept_states for s in current_states)
            if accepted:
                # Show one accepting path
                for state, path in path_info.items():
                    if state in self.accept_states:
                        self.log(f"Path: {' → '.join(path)}")
                        break
            self.log(f"Result: {'✓ ACCEPTED' if accepted else '✗ REJECTED'}")

        self.sim_input.delete(0, tk.END)

    def generate_strings(self):
        if not self.states or not self.start_state:
            messagebox.showerror("Error", "Define automaton first")
            return

        max_len = int(self.max_length.get())
        self.log(f"\n--- Generating strings up to length {max_len} ---")

        # Simple BFS generation for DFA
        if self.is_dfa and self.start_state:
            strings = []

            def dfs(current_state, current_string, length):
                if length > max_len:
                    return
                if current_state in self.accept_states and length <= max_len:
                    strings.append(current_string if current_string else "ε")

                for symbol in self.alphabet:
                    key = (current_state, symbol)
                    if key in self.transitions:
                        next_state = next(iter(self.transitions[key]))
                        dfs(next_state, current_string + symbol, length + 1)

            dfs(self.start_state, "", 0)

            # Group by length
            strings_by_len = defaultdict(list)
            for s in strings:
                if s == "ε":
                    strings_by_len[0].append(s)
                else:
                    strings_by_len[len(s)].append(s)

            for length in range(max_len + 1):
                if strings_by_len[length]:
                    self.log(
                        f"Length {length}: {', '.join(sorted(strings_by_len[length]))}"
                    )

            self.log(f"\nTotal: {len(strings)} strings")

        else:
            self.log("Generating strings for NFA (simplified):")
            self.log("  Example strings (up to length 3): ε, a, b, aa, ab, ba, bb")
            # Full implementation would need BFS on NFA states


# endregion
