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
    def __init__(self ,transactionType ,amount ,date=None): 
        self.transactionType = transactionType 
        self.amount = amount 
        self.date = date if date else datetime.datetime.now() 

    def __str__(self): 
        return f"{self.date}: {self.transactionType} of {self.amount}" 

class BankAccount: 
    def __init__(self,name ,balance=0): 
        self.name = name 
        self.balance = balance 
        self.transactions = [] 

    def deposit(self, amount): 
        if amount > 0: 
            self.balance += amount 
            self.transactions.append(Transaction("Deposit",amount)) 
        else: 
            print("Amount must be positive") 

    def withdraw(self, amount): 
        if amount > 0 and self.balance >= amount: 
            self.balance -= amount 
            self.transactions.append(Transaction("Withdrawal",amount)) 
        else: 
            print("Insufficient funds or invalid amount") 

    def getBalance(self): 
        return self.balance 

    def showTransactions(self): 
        for transaction in self.transactions: 
            print(transaction)

    def transfer(self, amount, targetAccount): 
        if self.balance >= amount and amount > 0: 
            self.balance -= amount 
            targetAccount.balance += amount 
            self.transactions.append(Transaction("Transfer Out",amount)) 
            targetAccount.transactions.append(Transaction("Transfer In",amount)) 
        else: 
            print("Invalid transfer amount") 

class LoanAccount: 
    def __init__(self, account, loanAmount, interestRate, termYears): 
        self.account = account 
        self.loanAmount = loanAmount 
        self.interestRate = interestRate 
        self.termYears = termYears 
        self.monthlyPayment = self.calculateMonthlyPayment() 
        self.remainingBalance = loanAmount 
        self.paymentHistory = [] 

    def calculateMonthlyPayment(self): 
        rate = self.interestRate / 12 
        termMonths = self.termYears * 12 
        return self.loanAmount * rate / (1 - (1 + rate) ** -termMonths)

    def makePayment(self, amount): 
        if amount >= self.monthlyPayment: 
            self.remainingBalance -= amount 
            self.paymentHistory.append((datetime.datetime.now(), amount)) 
            print(f"Loan payment of {amount} made. Remaining balance: {self.remainingBalance}") 
        else: 
            print(f"Payment is less than the required {self.monthlyPayment}") 

    def getBalance(self): 
        return self.remainingBalance 

    def showPaymentHistory(self): 
        for payment in self.paymentHistory: 
            print(f"Payment on {payment[0]}: {payment[1]}")

class Customer: 
    def __init__(self,name ,bankAccount ,loanAccount=None): 
        self.name = name 
        self.bankAccount = bankAccount 
        self.loanAccount = loanAccount 

    def applyForLoan(self,loanAmount ,interestRate ,termYears): 
        if loanAmount > 0: 
            self.loanAccount = LoanAccount(self.bankAccount ,loanAmount ,interestRate ,termYears) 
            print(f"{self.name} applied for a loan of {loanAmount} at {interestRate*100}% interest for {termYears} years") 
        else: 
            print("Invalid loan amount") 

    def makeLoanPayment(self,amount): 
        if self.loanAccount: 
            self.loanAccount.makePayment(amount) 
        else: 
            print(f"{self.name} has no loan account") 

    def showAccountInfo(self): 
        print(f"Account Info for {self.name}:") 
        print(f"Balance: {self.bankAccount.getBalance()}") 
        if self.loanAccount: 
            print(f"Loan Balance: {self.loanAccount.getBalance()}") 
            self.loanAccount.showPaymentHistory() 
        else: 
            print("No loan account associated")

class Bank: 
    def __init__(self, bankName): 
        self.bankName = bankName 
        self.accounts = [] 
        self.loans = [] 
        self.customers = [] 

    def addAccount(self, account): 
        self.accounts.append(account) 

    def addCustomer(self, customer): 
        self.customers.append(customer) 
        self.accounts.append(customer.bankAccount) 
        if customer.loanAccount: 
            self.loans.append(customer.loanAccount) 

    def getTotalBalance(self): 
        total = sum(account.getBalance() for account in self.accounts) 
        return total

    def getTotalLoanBalance(self): 
        total = sum(loan.getBalance() for loan in self.loans if loan) 
        return total 

    def generateReport(self): 
        print(f"--- Bank Report for {self.bankName} ---") 
        print(f"Total Balance Across All Accounts: {self.getTotalBalance()}") 
        print(f"Total Outstanding Loan Amount: {self.getTotalLoanBalance()}") 
        print(f"Customer Report:") 
        for customer in self.customers: 
            print(f"Customer: {customer.name}") 
            customer.showAccountInfo() 
            print("---------------------------------") 

    def generateRandomTransactions(self, numberOfTransactions): 
        for _ in range(numberOfTransactions): 
            account = random.choice(self.accounts) 
            transactionType = random.choice(["deposit", "withdraw", "transfer"]) 
            amount = random.randint(50 ,5000) 
            if transactionType == "deposit": 
                account.deposit(amount) 
            elif transactionType == "withdraw": 
                account.withdraw(amount) 
            else: 
                targetAccount = random.choice(self.accounts) 
                account.transfer(amount ,targetAccount) 

    def generateLoanReport(self): 
        print(f"--- Loan Report for {self.bankName} ---") 
        totalLoans = sum(loan.getBalance() for loan in self.loans) 
        print(f"Total Loan Amount Outstanding: {totalLoans}") 
        for loan in self.loans: 
            print(f"Loan for {loan.account.name}: Remaining Balance {loan.getBalance()}") 
            loan.showPaymentHistory() 
        print("---------------------------------") 

    def accountPerformanceAnalysis(self): 
        print(f"--- Account Performance Analysis for {self.bankName} ---") 
        accountPerformance = {} 
        for account in self.accounts: 
            accountType = type(account).__name__ 
            if accountType not in accountPerformance: 
                accountPerformance[accountType] = 0 
            accountPerformance[accountType] += account.getBalance() 

        for accountType ,totalBalance in accountPerformance.items(): 
            print(f"Total balance for {accountType}: {totalBalance}") 
        print("---------------------------------") 

    def loanRiskAssessment(self): 
        print(f"--- Loan Risk Assessment for {self.bankName} ---") 
        highRiskLoans = [] 
        for loan in self.loans: 
            riskLevel = loan.getBalance() / loan.account.getBalance() 
            if riskLevel > 0.75: 
                highRiskLoans.append((loan.account.name ,loan.getBalance() ,riskLevel))

        if highRiskLoans: 
            print("High Risk Loans:") 
            for loan in highRiskLoans: 
                print(f"Customer: {loan[0]} ,Loan Balance: {loan[1]} ,Risk Level: {loan[2]:.2f}") 
        else: 
            print("No high-risk loans found.") 
        print("---------------------------------")

class SavingsAccount(BankAccount): 
    def __init__(self,name ,balance=0 ,interestRate=0.02): 
        super().__init__(name ,balance) 
        self.interestRate = interestRate 

    def applyInterest(self): 
        interest = self.balance * self.interestRate 
        self.deposit(interest) 
        print(f"Interest applied: {interest} to {self.name}'s account") 

class CheckingAccount(BankAccount): 
    def __init__(self,name ,balance=0 ,overdraftLimit=500): 
        super().__init__(name ,balance) 
        self.overdraftLimit = overdraftLimit 

    def withdraw(self, amount): 
        if self.balance + self.overdraftLimit >= amount: 
            self.balance -= amount 
            self.transactions.append(Transaction("Withdrawal", amount)) 
        else: 
            print("Insufficient funds and overdraft limit reached")

class FixedDepositAccount(BankAccount): 
    def __init__(self,name ,balance=0 ,termYears=5 ,interestRate=0.04): 
        super().__init__(name ,balance) 
        self.termYears = termYears 
        self.interestRate = interestRate 
        self.maturityDate = datetime.datetime.now() + datetime.timedelta(days=365 * termYears) 

    def applyInterest(self): 
        if datetime.datetime.now() >= self.maturityDate: 
            interest = self.balance * self.interestRate 
            self.deposit(interest) 
            print(f"Interest applied: {interest} to {self.name}'s Fixed Deposit Account") 
        else: 
            print(f"Account will mature on {self.maturityDate}. Interest cannot be applied yet.") 

class CreditCardAccount: 
    def __init__(self,name ,limit=5000): 
        self.name = name 
        self.limit = limit 
        self.balance = 0 
        self.transactions = []

    def makePurchase(self, amount): 
        if self.balance + amount <= self.limit: 
            self.balance += amount 
            self.transactions.append(Transaction("Purchase",amount)) 
        else: 
            print("Purchase exceeds credit limit") 

    def makePayment(self, amount): 
        if amount <= self.balance: 
            self.balance -= amount 
            self.transactions.append(Transaction("Payment",amount)) 
        else: 
            print("Payment exceeds balance") 

    def withdraw(self, amount): 
        if self.balance + amount <= self.limit: 
            self.balance += amount 
            self.transactions.append(Transaction("Withdrawal",amount)) 
        else: 
            print("Insufficient funds for withdrawal")

    def transfer(self, amount, targetAccount): 
        if self.balance >= amount and amount > 0: 
            self.balance -= amount 
            targetAccount.balance += amount 
            self.transactions.append(Transaction("Transfer Out",amount)) 
            targetAccount.transactions.append(Transaction("Transfer In",amount)) 
        else: 
            print("Invalid transfer amount")

    def deposit(self, amount): 
        if amount > 0: 
            self.balance -= amount  
            self.transactions.append(Transaction("Deposit",amount)) 
        else: 
            print("Deposit amount must be positive")

    def getBalance(self): 
        return self.balance

def main(): 
    bank = Bank("Greatest Bank") 
    aliceAccount = BankAccount("Alice",1000) 
    bobAccount = BankAccount("Bob",1500) 
    charlieAccount = SavingsAccount("Charlie",5000) 
    daveAccount = CheckingAccount("Dave",2000) 
    eveAccount = FixedDepositAccount("Eve",3000,termYears=3) 
    frankAccount = CreditCardAccount("Frank") 
    bank.addAccount(aliceAccount) 
    bank.addAccount(bobAccount) 
    bank.addAccount(charlieAccount) 
    bank.addAccount(daveAccount) 
    bank.addAccount(eveAccount) 
    bank.addAccount(frankAccount)

    aliceCustomer = Customer("Alice",aliceAccount) 
    bobCustomer = Customer("Bob",bobAccount) 
    charlieCustomer = Customer("Charlie",charlieAccount) 
    bank.addCustomer(aliceCustomer) 
    bank.addCustomer(bobCustomer) 
    bank.addCustomer(charlieCustomer) 

    bank.generateRandomTransactions(5) 
    bank.generateReport() 
    bank.generateLoanReport() 
    bank.accountPerformanceAnalysis() 
    bank.loanRiskAssessment() 

main()
