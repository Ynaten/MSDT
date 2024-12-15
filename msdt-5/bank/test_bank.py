import pytest
from unittest.mock import MagicMock
from datetime import datetime
from main import BankAccount, Transaction, LoanAccount


# Тест для депозита
def test_deposit():
    account = BankAccount("Test Account", 100)
    account.deposit(50)
    assert account.get_balance() == 150, "Deposit failed"

# Тест для снятия средств
def test_withdraw():
    account = BankAccount("Test Account", 100)
    account.withdraw(50)
    assert account.get_balance() == 50, "Withdrawal failed"

# Тест для снятия средств с ошибкой (недостаточно средств)
def test_withdraw_insufficient_funds():
    account = BankAccount("Test Account", 100)
    account.withdraw(150)
    assert account.get_balance() == 100, "Withdrawal with insufficient funds should fail"

# Тест для перевода средств
def test_transfer():
    account1 = BankAccount("Test Account 1", 100)
    account2 = BankAccount("Test Account 2", 50)
    account1.transfer(50, account2)
    assert account1.get_balance() == 50, "Transfer failed"
    assert account2.get_balance() == 100, "Transfer failed"

# Параметризированный тест для депозита
@pytest.mark.parametrize("initial_balance, deposit_amount, expected_balance", [
    (100, 50, 150),
    (0, 100, 100),
    (200, -50, 200)  # Ожидаем, что отрицательные депозиты не повлияют на баланс
])
def test_deposit_parametrized(initial_balance, deposit_amount, expected_balance):
    account = BankAccount("Test Account", initial_balance)
    account.deposit(deposit_amount)
    assert account.get_balance() == expected_balance, f"Failed for {initial_balance} + {deposit_amount}"

# Мок для тестирования взаимодействия с Transaction
def test_transaction_mock():
    # Создаём моки для метода __str__ класса Transaction
    mock_transaction = MagicMock(spec=Transaction)
    mock_transaction.__str__.return_value = "Mock Transaction"
    
    account = BankAccount("Test Account", 100)
    account.transactions.append(mock_transaction)
    
    assert str(account.transactions[0]) == "Mock Transaction", "Mock transaction did not work as expected"

# Тест на создание и отображение транзакций
def test_show_transactions():
    account = BankAccount("Test Account", 100)
    account.deposit(50)
    account.withdraw(30)
    transactions = [str(transaction).split(': ', 1)[1] for transaction in account.transactions]
    assert "Deposit of 50" in transactions, "Deposit transaction not found"


# Тест для проверки расчета ежемесячных выплат по кредиту
def test_calculate_monthly_payment():
    account = BankAccount("Test Account", 10000)
    loan = LoanAccount(account, 100000, 0.05, 15)  # Сумма кредита 100000, 5% годовых, срок 15 лет
    expected_payment = 790.79  # Ожидаемая ежемесячная выплата
    assert abs(loan.monthly_payment - expected_payment) < 0.01, "Monthly payment calculation is incorrect"
