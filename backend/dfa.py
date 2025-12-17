"""
Deterministic Finite Automaton (DFA) for Sri Lankan NIC Validation
-------------------------------------------------------------------
This module implements a DFA to validate the structural format of Sri Lankan
National Identity Card (NIC) numbers.

Automaton Specification:
-----------------------
Type: Deterministic Finite Automaton (DFA)
Purpose: Validate NIC number format (structure only, not semantic validity)

Alphabet (Σ): {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, V, v, X, x}

Valid Formats:
1. Old NIC: 9 digits followed by 'V' or 'X' (e.g., 981234567V)
2. New NIC: 12 digits (e.g., 199812345678)

States (Q):
-----------
- q0: Start state (no characters processed)
- q1 to q9: Processing digits 1 through 9
- q10: Accept state for old NIC (9 digits + V/X)
- q11: Processing 10th digit (for new NIC)
- q12: Processing 11th digit (for new NIC)
- q13: Accept state for new NIC (12 digits)
- q_reject: Reject state (invalid input)

Accepting States (F): {q10, q13}
Start State (q0): q0

Transition Function (δ):
------------------------
The DFA processes each character sequentially and transitions between states
based on the current state and input character.
"""


class NICDFA:
    """
    A Deterministic Finite Automaton for validating Sri Lankan NIC numbers.
    
    This class implements a character-by-character state machine that accepts
    valid NIC formats and rejects invalid ones.
    """
    
    def __init__(self):
        """Initialize the DFA with defined states."""
        self.START = 'q0'
        self.DIGIT_1 = 'q1'
        self.DIGIT_2 = 'q2'
        self.DIGIT_3 = 'q3'
        self.DIGIT_4 = 'q4'
        self.DIGIT_5 = 'q5'
        self.DIGIT_6 = 'q6'
        self.DIGIT_7 = 'q7'
        self.DIGIT_8 = 'q8'
        self.DIGIT_9 = 'q9'
        self.OLD_NIC_ACCEPT = 'q10'
        self.DIGIT_10 = 'q11'
        self.DIGIT_11 = 'q12'
        self.NEW_NIC_ACCEPT = 'q13'
        self.REJECT = 'q_reject'
        
        self.accepting_states = {self.OLD_NIC_ACCEPT, self.NEW_NIC_ACCEPT}
        self.current_state = self.START
    
    def reset(self):
        """Reset the DFA to its start state."""
        self.current_state = self.START
    
    def is_digit(self, char):
        """Check if a character is a digit (0-9)."""
        return char in '0123456789'
    
    def is_valid_suffix(self, char):
        """Check if a character is a valid old NIC suffix (V, v, X, or x)."""
        return char.upper() in 'VX'
    
    def transition(self, char):
        """
        Execute a state transition based on the current state and input character.
        
        This is the core DFA transition function δ(q, a) -> q'
        where q is the current state, a is the input character,
        and q' is the next state.
        
        Args:
            char: The input character to process
            
        Returns:
            None (updates self.current_state)
        """
        if self.current_state == self.START:
            if self.is_digit(char):
                self.current_state = self.DIGIT_1
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_1:
            if self.is_digit(char):
                self.current_state = self.DIGIT_2
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_2:
            if self.is_digit(char):
                self.current_state = self.DIGIT_3
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_3:
            if self.is_digit(char):
                self.current_state = self.DIGIT_4
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_4:
            if self.is_digit(char):
                self.current_state = self.DIGIT_5
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_5:
            if self.is_digit(char):
                self.current_state = self.DIGIT_6
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_6:
            if self.is_digit(char):
                self.current_state = self.DIGIT_7
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_7:
            if self.is_digit(char):
                self.current_state = self.DIGIT_8
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_8:
            if self.is_digit(char):
                self.current_state = self.DIGIT_9
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_9:
            if self.is_valid_suffix(char):
                self.current_state = self.OLD_NIC_ACCEPT
            elif self.is_digit(char):
                self.current_state = self.DIGIT_10
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.OLD_NIC_ACCEPT:
            self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_10:
            if self.is_digit(char):
                self.current_state = self.DIGIT_11
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.DIGIT_11:
            if self.is_digit(char):
                self.current_state = self.NEW_NIC_ACCEPT
            else:
                self.current_state = self.REJECT
        
        elif self.current_state == self.NEW_NIC_ACCEPT:
            self.current_state = self.REJECT
        
        elif self.current_state == self.REJECT:
            self.current_state = self.REJECT
    
    def validate(self, nic_string):
        """
        Validate a NIC string using the DFA.
        
        This method processes the input string character by character,
        executing state transitions according to the DFA's transition function.
        
        Args:
            nic_string: The NIC number string to validate
            
        Returns:
            tuple: (result, state)
                - result: "ACCEPT" if the NIC is valid, "REJECT" otherwise
                - state: The final state reached by the DFA
        """
        self.reset()
        
        if not nic_string:
            return "REJECT", self.REJECT
        
        for i, char in enumerate(nic_string):
            self.transition(char)
        
        if self.current_state in self.accepting_states:
            return "ACCEPT", self.current_state
        else:
            return "REJECT", self.current_state
    
    def validate_with_trace(self, nic_string):
        """
        Validate a NIC string and return detailed trace information.
        
        Useful for educational purposes and debugging.
        
        Args:
            nic_string: The NIC number string to validate
            
        Returns:
            dict: Contains result, final_state, and trace of all transitions
        """
        self.reset()
        
        trace = []
        
        if not nic_string:
            return {
                "result": "REJECT",
                "final_state": self.REJECT,
                "trace": [{"step": 0, "input": "", "state": self.REJECT}]
            }
        
        trace.append({
            "step": 0,
            "input": "",
            "state": self.START
        })
        
        for i, char in enumerate(nic_string):
            self.transition(char)
            trace.append({
                "step": i + 1,
                "input": char,
                "state": self.current_state
            })
        
        result = "ACCEPT" if self.current_state in self.accepting_states else "REJECT"
        
        return {
            "result": result,
            "final_state": self.current_state,
            "trace": trace
        }


def main():
    """
    Command-line interface for testing the NIC DFA.
    """
    print("=" * 70)
    print("Sri Lankan NIC Validator - Deterministic Finite Automaton (DFA)")
    print("=" * 70)
    print("\nValid Formats:")
    print("  1. Old NIC: 9 digits + V/X (e.g., 981234567V)")
    print("  2. New NIC: 12 digits (e.g., 199812345678)")
    print("\nNote: This validator checks ONLY the structural format.")
    print("=" * 70)
    print()
    
    dfa = NICDFA()
    
    print("Enter NIC numbers to validate (type 'quit' to exit):")
    print()
    
    while True:
        nic_input = input("NIC Number: ").strip()
        
        if nic_input.lower() in ['quit', 'exit', 'q']:
            print("\nExiting...")
            break
        
        if not nic_input:
            print("Error: Please enter a NIC number.\n")
            continue
        
        result_data = dfa.validate_with_trace(nic_input)
        
        print(f"\nInput: {nic_input}")
        print(f"Result: {result_data['result']}")
        print(f"Final State: {result_data['final_state']}")
        
        print("\nState Transitions:")
        for step in result_data['trace']:
            if step['step'] == 0:
                print(f"  Start -> {step['state']}")
            else:
                print(f"  Read '{step['input']}' -> {step['state']}")
        
        print()


if __name__ == "__main__":
    main()
