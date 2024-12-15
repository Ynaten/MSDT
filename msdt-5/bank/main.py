
import datetime
import itertools
import json
import logging
import os
import random
import socket
import sys
import time
import urllib

import numpy as np
import pandas as pd
import requests
import scipy
from collections import Counter, deque


class Transaction:
    """
    Represents a financial transaction.
    Attributes:
        transaction_type (str): Type of the transaction (e.g., "Deposit", "Withdrawal").
        amount (float): Amount involved in the transaction.
        date (datetime): Date and time when the transaction occurred.
    """

    def __init__(self, transaction_type, amount, date=None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date if date else datetime.datetime.now()

    def __str__(self):
        return f"{self.date}: {self.transaction_type} of {self.amount}"


class BankAccount:
    """
    Represents a bank account with the ability to deposit, withdraw, and transfer funds.
    Attributes:
        name (str): Name of the account holder.
        balance (float): Current balance of the account.
        transactions (list): List of transactions associated with the account.
    """

    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        """Deposits a specified amount into the account."""
        if amount > 0:
            self.balance += amount
            self.transactions.append(
                Transaction("Deposit", amount)
            )
        else:
            print("Amount must be positive")

    def withdraw(self, amount):
        """Withdraws a specified amount from the account."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transactions.append(
                Transaction("Withdrawal", amount)
            )
        else:
            print("Insufficient funds or invalid amount")

    def get_balance(self):
        """Returns the current balance of the account."""
        return self.balance

    def show_transactions(self):
        """Displays all transactions associated with the account."""
        for transaction in self.transactions:
            print(transaction)

    def transfer(self, amount, target_account):
        """Transfers funds to another account."""
        if self.balance >= amount and amount > 0:
            self.balance -= amount
            target_account.balance += amount
            self.transactions.append(
                Transaction("Transfer Out", amount)
            )
            target_account.transactions.append(
                Transaction("Transfer In", amount)
            )
        else:
            print("Invalid transfer amount")


class LoanAccount:
    """
    Represents a loan account with the ability to make payments.
    Attributes:
        account (BankAccount): The bank account associated with the loan.
        loan_amount (float): The total loan amount.
        interest_rate (float): The annual interest rate for the loan.
        term_years (int): The term of the loan in years.
        monthly_payment (float): The calculated monthly payment for the loan.
        remaining_balance (float): The remaining balance on the loan.
        payment_history (list): A list of payments made towards the loan.
    """

    def __init__(self, account, loan_amount, interest_rate, term_years):
        self.account = account
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.monthly_payment = self.calculate_monthly_payment()
        self.remaining_balance = loan_amount
        self.payment_history = []

    def calculate_monthly_payment(self):
        """Calculates the monthly payment for the loan."""
        rate = self.interest_rate / 12
        term_months = self.term_years * 12
        return self.loan_amount * rate / (
            1 - (1 + rate) ** -term_months
        )

    def make_payment(self, amount):
        """Makes a payment towards the loan."""
        if amount >= self.monthly_payment:
            self.remaining_balance -= amount
            self.payment_history.append(
                (datetime.datetime.now(), amount)
            )
            print(
                f"Loan payment of {amount} made. Remaining balance: "
                f"{self.remaining_balance}"
            )
        else:
            print(
                f"Payment is less than the required "
                f"{self.monthly_payment}"
            )

    def get_balance(self):
        """Returns the remaining balance on the loan."""
        return self.remaining_balance

    def show_payment_history(self):
        """Displays the payment history for the loan."""
        for payment in self.payment_history:
            print(f"Payment on {payment[0]}: {payment[1]}")


class Customer:
    """
    Represents a customer of the bank.
    Attributes:
        name (str): Name of the customer.
        bank_account (BankAccount): The customer's bank account.
        loan_account (LoanAccount, optional): The customer's loan account.
    """

    def __init__(self, name, bank_account, loan_account=None):
        self.name = name
        self.bank_account = bank_account
        self.loan_account = loan_account

    def apply_for_loan(self, loan_amount, interest_rate, term_years):
        """Applies for a loan for the customer."""
        if loan_amount > 0:
            self.loan_account = LoanAccount(
                self.bank_account, loan_amount, interest_rate, term_years
            )
            print(
                f"{self.name} applied for a loan of {loan_amount} at "
                f"{interest_rate*100}% interest for {term_years} years"
            )
        else:
            print("Invalid loan amount")

    def make_loan_payment(self, amount):
        """Makes a loan payment for the customer."""
        if self.loan_account:
            self.loan_account.make_payment(amount)
        else:
            print(f"{self.name} has no loan account")

    def show_account_info(self):
        """Displays the account information for the customer."""
        print(f"Account Info for {self.name}:")
        print(f"Balance: {self.bank_account.get_balance()}")
        if self.loan_account:
            print(f"Loan Balance: {self.loan_account.get_balance()}")
            self.loan_account.show_payment_history()
        else:
            print("No loan account associated")


class Bank:
    """
    Represents a bank, which contains multiple accounts and customers.
    Attributes:
        bank_name (str): The name of the bank.
        accounts (list): List of bank accounts associated with the bank.
        loans (list): List of loan accounts associated with the bank.
        customers (list): List of customers of the bank.
    """

    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.accounts = []
        self.loans = []
        self.customers = []

    def add_account(self, account):
        """Adds a bank account to the bank."""
        self.accounts.append(account)

    def add_customer(self, customer):
        """Adds a customer to the bank."""
        self.customers.append(customer)
        self.accounts.append(customer.bank_account)
        if customer.loan_account:
            self.loans.append(customer.loan_account)

    def get_total_balance(self):
        """Returns the total balance across all accounts in the bank."""
        total = sum(account.get_balance() for account in self.accounts)
        return total

    def get_total_loan_balance(self):
        """Returns the total loan balance across all loans in the bank."""
        total = sum(loan.get_balance() for loan in self.loans if loan)
        return total

    def generate_report(self):
        """Generates a financial report for the bank."""
        print(f"--- Bank Report for {self.bank_name} ---")
        print(f"Total Balance Across All Accounts: {self.get_total_balance()}")
        print(f"Total Outstanding Loan Amount: {self.get_total_loan_balance()}")
        print(f"Customer Report:")
        for customer in self.customers:
            print(f"Customer: {customer.name}")
            customer.show_account_info()
            print("---------------------------------")

    def generate_random_transactions(self, number_of_transactions):
        """Generates random transactions for the bank."""
        for _ in range(number_of_transactions):
            account = random.choice(self.accounts)
            transaction_type = random.choice(["deposit", "withdraw", "transfer"])
            amount = random.randint(50, 5000)
            if transaction_type == "deposit":
                account.deposit(amount)
            elif transaction_type == "withdraw":
                account.withdraw(amount)
            else:
                target_account = random.choice(self.accounts)
                account.transfer(amount, target_account)

    def generate_loan_report(self):
        """Generates a report of loans and their payment history."""
        print(f"--- Loan Report for {self.bank_name} ---")
        total_loans = sum(loan.get_balance() for loan in self.loans)
        print(f"Total Loan Amount Outstanding: {total_loans}")
        for loan in self.loans:
            print(f"Loan for {loan.account.name}: Remaining Balance {loan.get_balance()}")
            loan.show_payment_history()
        print("---------------------------------")

    def account_performance_analysis(self):
        """Analyzes the performance of the accounts in the bank."""
        print(f"--- Account Performance Analysis for {self.bank_name} ---")
        account_performance = {}
        for account in self.accounts:
            account_type = type(account).__name__
            if account_type not in account_performance:
                account_performance[account_type] = 0
            account_performance[account_type] += account.get_balance()

        for account_type, total_balance in account_performance.items():
            print(f"Total balance for {account_type}: {total_balance}")
        print("---------------------------------")

    def loan_risk_assessment(self):
        """Assesses the risk level of loans in the bank."""
        print(f"--- Loan Risk Assessment for {self.bank_name} ---")
        high_risk_loans = []
        for loan in self.loans:
            risk_level = loan.get_balance() / loan.account.get_balance()
            if risk_level > 0.75:
                high_risk_loans.append(
                    (loan.account.name, loan.get_balance(), risk_level)
                )

        if high_risk_loans:
            print("High Risk Loans:")
            for loan in high_risk_loans:
                print(
                    f"Customer: {loan[0]}, Loan Balance: {loan[1]}, "
                    f"Risk Level: {loan[2]:.2f}"
                )
        else:
            print("No high-risk loans found.")
        print("---------------------------------")


class SavingsAccount(BankAccount):
    """
    Represents a savings account with the ability to apply interest.
    Attributes:
        interest_rate (float): The annual interest rate for the savings account.
    """

    def __init__(self, name, balance=0, interest_rate=0.02):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        """Applies interest to the savings account."""
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print(f"Interest applied: {interest} to {self.name}'s account")


class CheckingAccount(BankAccount):
    """
    Represents a checking account with an overdraft limit.
    Attributes:
        overdraft_limit (float): The overdraft limit for the checking account.
    """

    def __init__(self, name, balance=0, overdraft_limit=500):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """Withdraws an amount from the checking account, considering the overdraft limit."""
        if self.balance + self.overdraft_limit >= amount:
            self.balance -= amount
            self.transactions.append(Transaction("Withdrawal", amount))
        else:
            print("Insufficient funds and overdraft limit reached")


class FixedDepositAccount(BankAccount):
    """
    Represents a fixed deposit account with a maturity period and interest rate.
    Attributes:
        term_years (int): The number of years the account is locked in.
        interest_rate (float): The annual interest rate for the fixed deposit account.
        maturity_date (datetime): The date when the fixed deposit matures.
    """

    def __init__(self, name, balance=0, term_years=5, interest_rate=0.04):
        super().__init__(name, balance)
        self.term_years = term_years
        self.interest_rate = interest_rate
        self.maturity_date = datetime.datetime.now() + datetime.timedelta(
            days=365 * term_years
        )

    def apply_interest(self):
        """Applies interest to the fixed deposit account once it matures."""
        if datetime.datetime.now() >= self.maturity_date:
            interest = self.balance * self.interest_rate
            self.deposit(interest)
            print(
                f"Interest applied: {interest} to {self.name}'s Fixed Deposit Account"
            )
        else:
            print(
                f"Account will mature on {self.maturity_date}. "
                f"Interest cannot be applied yet."
            )


class CreditCardAccount:
    """
    Represents a credit card account with the ability to make purchases and payments.
    Attributes:
        limit (float): The credit limit for the card.
        balance (float): The current balance on the card.
    """

    def __init__(self, name, limit=5000):
        self.name = name
        self.limit = limit
        self.balance = 0
        self.transactions = []

    def make_purchase(self, amount):
        """Makes a purchase on the credit card."""
        if self.balance + amount <= self.limit:
            self.balance += amount
            self.transactions.append(Transaction("Purchase", amount))
        else:
            print("Purchase exceeds credit limit")

    def make_payment(self, amount):
        """Makes a payment towards the credit card balance."""
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(Transaction("Payment", amount))
        else:
            print("Payment exceeds balance")

    def withdraw(self, amount):
        """Withdraws an amount from the credit card."""
        if self.balance + amount <= self.limit:
            self.balance += amount
            self.transactions.append(Transaction("Withdrawal", amount))
        else:
            print("Insufficient funds for withdrawal")

    def transfer(self, amount, target_account):
        """Transfers an amount from the credit card to another account."""
        if self.balance >= amount and amount > 0:
            self.balance -= amount
            target_account.balance += amount
            self.transactions.append(Transaction("Transfer Out", amount))
            target_account.transactions.append(Transaction("Transfer In", amount))
        else:
            print("Invalid transfer amount or insufficient funds")


    def deposit(self, amount):
        """deposit an amount from the credit card to another account."""
        if amount > 0:
            self.balance -= amount
            self.transactions.append(Transaction("Deposit", amount))
        else:
            print("Deposit amount must be positive")

    def get_balance(self):
        """get balance"""
        return self.balance


def main():
    bank = Bank("Greatest Bank")
    alice_account = BankAccount("Alice", 1000)
    bob_account = BankAccount("Bob", 1500)
    charlie_account = SavingsAccount("Charlie", 5000)
    dave_account = CheckingAccount("Dave", 2000)
    eve_account = FixedDepositAccount("Eve", 3000, term_years=3)
    frank_account = CreditCardAccount("Frank")
    bank.add_account(alice_account)
    bank.add_account(bob_account)
    bank.add_account(charlie_account)
    bank.add_account(dave_account)
    bank.add_account(eve_account)
    bank.add_account(frank_account)

    alice_customer = Customer("Alice", alice_account)
    bob_customer = Customer("Bob", bob_account)
    charlie_customer = Customer("Charlie", charlie_account)
    bank.add_customer(alice_customer)
    bank.add_customer(bob_customer)
    bank.add_customer(charlie_customer)

    bank.generate_random_transactions(5)
    bank.generate_report()
    bank.generate_loan_report()
    bank.account_performance_analysis()
    bank.loan_risk_assessment()


main()