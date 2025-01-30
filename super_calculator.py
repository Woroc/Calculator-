import math
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class ScientificCalculator:
    def __init__(self):
        self.history = []
        self.memory = 0
        self.last_result = None
        self.angle_mode = 'rad'  # 'deg' or 'rad'

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        self.clear_screen()
        print(Fore.CYAN + "╔════════════════════════════════════════╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + "         SUPER SCIENTIFIC CALCULATOR      " + Fore.CYAN + "║")
        print(Fore.CYAN + "╠════════════════════════════════════════╣")
        print(Fore.CYAN + "║" + Fore.GREEN + "  Basic Operations:" + " " * 21 + Fore.CYAN + "║")
        print(Fore.CYAN + "║  +, -, *, /, ^, √, !, %               ║")
        print(Fore.CYAN + "║" + Fore.BLUE + "  Scientific Functions:" + " " * 17 + Fore.CYAN + "║")
        print(Fore.CYAN + "║  sin, cos, tan, log, ln, exp, abs      ║")
        print(Fore.CYAN + "║" + Fore.MAGENTA + "  Memory Operations:" + " " * 20 + Fore.CYAN + "║")
        print(Fore.CYAN + "║  mc (memory clear), mr (memory recall) ║")
        print(Fore.CYAN + "║  m+ (memory add), m- (memory subtract) ║")
        print(Fore.CYAN + "║" + Fore.WHITE + "  Special Commands:" + " " * 21 + Fore.CYAN + "║")
        print(Fore.CYAN + "║  cls (clear screen), hist (history)    ║")
        print(Fore.CYAN + "║  angle (toggle degrees/radians)        ║")
        print(Fore.CYAN + "║  exit                                 ║")
        print(Fore.CYAN + "╚════════════════════════════════════════╝")

    def add_to_history(self, operation, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} - {operation} = {result}"
        self.history.append(entry)

    def run(self):
        while True:
            self.show_menu()
            try:
                expression = input(Fore.YELLOW + "\nEnter operation: ").strip().lower()
                
                if expression == 'exit':
                    print(Fore.GREEN + "Exiting calculator. Goodbye!")
                    break
                
                if expression == 'hist':
                    self.show_history()
                    continue
                
                if expression == 'cls':
                    self.clear_screen()
                    continue
                
                if expression == 'angle':
                    self.angle_mode = 'deg' if self.angle_mode == 'rad' else 'rad'
                    print(Fore.BLUE + f"Angle mode switched to {self.angle_mode.upper()}!")
                    input("Press Enter to continue...")
                    continue

                result = self.process_operation(expression)
                if result is not None:
                    self.last_result = result
                    print(Fore.GREEN + f"Result: {result}")
                    input("Press Enter to continue...")

            except Exception as e:
                print(Fore.RED + f"Error: {str(e)}")
                input("Press Enter to continue...")

    def process_operation(self, expr):
        try:
            # Memory operations
            if expr == 'mc':
                self.memory = 0
                print(Fore.BLUE + "Memory cleared!")
                return None
            elif expr == 'mr':
                print(Fore.BLUE + f"Memory recall: {self.memory}")
                return self.memory
            elif expr == 'm+':
                self.memory += self.last_result
                print(Fore.BLUE + f"Added to memory. New value: {self.memory}")
                return None
            elif expr == 'm-':
                self.memory -= self.last_result
                print(Fore.BLUE + f"Subtracted from memory. New value: {self.memory}")
                return None

            # Scientific functions
            if expr.startswith('sin'):
                num = self.get_number(expr[3:])
                return self.sine(num)
            elif expr.startswith('cos'):
                num = self.get_number(expr[3:])
                return self.cosine(num)
            elif expr.startswith('tan'):
                num = self.get_number(expr[3:])
                return self.tangent(num)
            elif expr.startswith('log'):
                num = self.get_number(expr[3:])
                return math.log10(num)
            elif expr.startswith('ln'):
                num = self.get_number(expr[2:])
                return math.log(num)
            elif expr.startswith('exp'):
                num = self.get_number(expr[3:])
                return math.exp(num)
            elif expr.startswith('abs'):
                num = self.get_number(expr[3:])
                return abs(num)

            # Basic operations
            if '+' in expr:
                nums = expr.split('+')
                result = sum(float(n) for n in nums)
            elif '-' in expr:
                nums = expr.split('-')
                result = float(nums[0]) - sum(float(n) for n in nums[1:])
            elif '*' in expr:
                nums = expr.split('*')
                result = math.prod(float(n) for n in nums)
            elif '/' in expr:
                nums = expr.split('/')
                result = float(nums[0])
                for n in nums[1:]:
                    result /= float(n)
            elif '^' in expr:
                base, exp = expr.split('^')
                result = math.pow(float(base), float(exp))
            elif '√' in expr:
                num = expr.split('√')[1]
                result = math.sqrt(float(num))
            elif '!' in expr:
                num = expr.split('!')[0]
                result = math.factorial(int(num))
            elif '%' in expr:
                num, percent = expr.split('%')
                result = (float(num) * float(percent)) / 100
            else:
                return float(expr)

            operation = expr.replace(' ', '')
            self.add_to_history(operation, result)
            return result

        except ValueError:
            raise ValueError("Invalid input format")
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except OverflowError:
            raise ValueError("Result too large")

    def get_number(self, s):
        s = s.strip()
        if s == '' and self.last_result is not None:
            return self.last_result
        return float(s)

    def show_history(self):
        self.clear_screen()
        print(Fore.CYAN + "╔════════════════════════════════════════╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + "            CALCULATION HISTORY           " + Fore.CYAN + "║")
        print(Fore.CYAN + "╠════════════════════════════════════════╣")
        for entry in self.history[-10:]:  # Show last 10 entries
            print(Fore.CYAN + "║ " + Fore.WHITE + entry.ljust(38) + Fore.CYAN + " ║")
        print(Fore.CYAN + "╚════════════════════════════════════════╝")
        input("\nPress Enter to return...")

    def sine(self, num):
        if self.angle_mode == 'deg':
            num = math.radians(num)
        return math.sin(num)

    def cosine(self, num):
        if self.angle_mode == 'deg':
            num = math.radians(num)
        return math.cos(num)

    def tangent(self, num):
        if self.angle_mode == 'deg':
            num = math.radians(num)
        return math.tan(num)

if __name__ == "__main__":
    calc = ScientificCalculator()
    print(Fore.YELLOW + r"""
     _______  ___   _______  __   __  _______  ___      _______ 
    |       ||   | |       ||  | |  ||       ||   |    |       |
    |    ___||   | |_     _||  |_|  ||    ___||   |    |   _   |
    |   | __ |   |   |   |  |       ||   |___ |   |    |  | |  |
    |   ||  ||   |   |   |  |       ||    ___||   |___ |  |_|  |
    |   |_| ||   |   |   |  |   _   ||   |___ |       ||       |
    |_______||___|   |___|  |__| |__||_______||_______||_______|
    """)
    input("Press Enter to start...")
    calc.run()
