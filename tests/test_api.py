"""
MiniBank 项目接口自动化测试样例
使用 pytest+requests，涵盖正向/异常/边界用例
"""

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.fixture(scope="module")
def accounts():
    """注册两个账户用于后续操作"""
    users = []
    # for i in range(2):
    #     r = requests.post(f"{BASE_URL}/accounts/register", json={
    #         "username": f"autouser{i+1}",
    #         "password": "test123"
    #     })
    #     users.append(r.json()["account_id"])
    for i in range(2):
        username = f"autouser_{i}_{int(time.time())}"
        r = requests.post(f"{BASE_URL}/accounts/register", json={
            "username": username,
            "password": "test123"
        })
        print(f"Register account response: {r.status_code}, {r.text}")
        assert r.status_code == 201
        users.append(r.json()["account_id"])
    return users

def test_register_success():
    r = requests.post(f"{BASE_URL}/accounts/register", json={
        "username": "pytestuser",
        "password": "pytestpwd"
    })
    assert r.status_code == 201
    assert "account_id" in r.json()

def test_register_duplicate():
    # 重复用户名注册
    requests.post(f"{BASE_URL}/accounts/register", json={
        "username": "dupuser",
        "password": "a"
    })
    r = requests.post(f"{BASE_URL}/accounts/register", json={
        "username": "dupuser",
        "password": "b"
    })
    assert r.status_code == 400
    assert "用户名已存在" in r.json()["error"]

def test_deposit(accounts):
    acc_id = accounts[0]
    r = requests.post(f"{BASE_URL}/accounts/{acc_id}/deposit", json={"amount": 1000})
    assert r.status_code == 200
    data = r.json()
    assert data["balance"] == 1000

def test_withdraw(accounts):
    acc_id = accounts[0]
    r = requests.post(f"{BASE_URL}/accounts/{acc_id}/withdraw", json={"amount": 800})
    assert r.status_code == 200
    assert r.json()["balance"] == 200

def test_overdraw(accounts):
    acc_id = accounts[0]
    r = requests.post(f"{BASE_URL}/accounts/{acc_id}/withdraw", json={"amount": 9999})
    assert r.status_code == 400
    assert "余额不足" in r.json()["error"]

def test_negative_deposit(accounts):
    acc_id = accounts[0]
    r = requests.post(f"{BASE_URL}/accounts/{acc_id}/deposit", json={"amount": -100})
    assert r.status_code == 400
    assert "需大于0" in r.json()["error"]

def test_transfer_success(accounts):
    from_acc, to_acc = accounts
    # 先存钱以保证有余额
    requests.post(f"{BASE_URL}/accounts/{from_acc}/deposit", json={"amount": 200})
    r = requests.post(f"{BASE_URL}/accounts/transfer", json={
        "from_account": from_acc,
        "to_account": to_acc,
        "amount": 100
    })
    assert r.status_code == 200
    assert r.json()["from_balance"] >= 0

def test_transfer_no_account():
    r = requests.post(f"{BASE_URL}/accounts/transfer", json={
        "from_account": 9999,
        "to_account": 8888,
        "amount": 1
    })
    assert r.status_code == 404
    assert "账户不存在" in r.json()["error"]

def test_transactions(accounts):
    acc_id = accounts[0]
    r = requests.get(f"{BASE_URL}/accounts/{acc_id}/transactions")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_reconcile(accounts):
    acc_id = accounts[0]
    r = requests.get(f"{BASE_URL}/accounts/{acc_id}/reconcile")
    assert r.status_code == 200
    assert r.json()["is_consistent"]