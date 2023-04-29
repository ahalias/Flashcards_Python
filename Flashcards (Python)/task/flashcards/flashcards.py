import os
from collections import defaultdict
import random
import sys
from Log import LoggerOut, LoggerIn
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--import_from', type=str, required=False, help='File name')
parser.add_argument('--export_to', type=str, required=False, help='File name')

args = parser.parse_args()



class FlashCards:

    def __init__(self):
        self.cards = {}
        self.cards_to_show = defaultdict(list)
        self.card_fails = {}


    def card_check(self, card_element, cards):
        card_item = input(f"The {card_element}:\n")
        while card_item in cards:
            card_item = input(f'The {card_element} "{card_item}" already exists. Try again:\n')
        return card_item

    def add_cards(self):
        term = self.card_check('card', self.cards.keys())
        definition = self.card_check('definition of the card', self.cards.values())
        self.cards[term] = definition
        print(f'The pair ("{term}":"{self.cards[term]}") has been added.')

    def incr_stats(self, term):
        self.card_fails[term] = self.card_fails.get(term, 0) + 1

    def ask_cards(self, ask_number):
        for term, definition in random.choices(list(self.cards.items()), k=ask_number):
            answer = input(f'Print the definition of "{term}":\n')
            if answer == definition:
                verification = 'Correct!'
            elif answer != definition and answer in self.cards.values():
                get_term = [term for term, definition in self.cards.items() if answer == definition]
                verification = f"""Wrong. The right answer is "{definition}", but your definition is correct for "{get_term[0]}"."""
                self.incr_stats(term)
            else:
                verification = f'Wrong. The right answer is "{definition}".'
                self.incr_stats(term)
            print(verification)

    def import_cards(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                content = file.readlines()
                for line in content:
                    term, definition = line.strip().split(":")
                    self.cards[term] = definition
            print(f"{len(content)} cards have been loaded.\n")
        else:
            print("File not found.\n")

    def export_cards(self, file_name):
        with open(file_name, "w") as file:
            for term, definition in self.cards.items():
                file.write(f"{term}:{definition}\n")
        print(f"{len(self.cards)} cards have been saved")

    def remove_cards(self):
        card_to_remove = input("Which card?\n")
        try:
            self.cards.pop(card_to_remove)
            print("The card has been removed.\n")
        except:
            print(f"""Can't remove "{card_to_remove}": there is no such card.\n""")

    def get_hardest_cards(self):
        hardest_cards = []
        if len(self.card_fails.items()) == 0:
            print("There are no cards with errors.")
        else:
            sorted_cards = sorted(self.card_fails.items(), key=lambda x: x[1], reverse=True)
            for card, fails in dict(sorted_cards).items():
                if fails == sorted_cards[0][1]:
                    hardest_cards.append(f'{card}')
            if len(hardest_cards) == 1:
                print(f'The hardest card is "{sorted_cards[0][0]}". You have {sorted_cards[0][1]} errors answering it.')
            else:
                hardest_cards = '", "'.join(hardest_cards)
                print(f'The hardest cards are {hardest_cards}. You have {sorted_cards[0][1]} errors answering them.')

    def get_action(self):
        if args.import_from:
            self.import_cards(args.import_from)
        choice = input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)\n")
        if choice == "import":
            file_name = input("File name:\n")
            self.import_cards(file_name)
        if choice == "export":
            file_name = input("File name:\n")
            self.export_cards(file_name)
        if choice == "add":
            self.add_cards()
        if choice == "remove":
            self.remove_cards()
        if choice == "ask":
            ask_number = int(input("How many times to ask?"))
            self.ask_cards(ask_number)
        if choice == "exit":
            print("Bye bye!")
            if args.export_to:
                self.export_cards(args.export_to)
            exit(1)
        if choice == "log":
            file_name = input("File name:\n")
            os.rename('default.txt', file_name)
            print("The log has been saved.")
        if choice == "hardest card":
            self.get_hardest_cards()
        if choice == "reset stats":
            self.card_fails = {}
            print("Card statistics have been reset.")





default_log = 'default.txt'
sys.stdout = LoggerOut(default_log)
sys.stdin = LoggerIn(default_log)

flash_cards = FlashCards()
while True:
    flash_cards.get_action()

