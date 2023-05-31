import hashlib
import logging
import inquirer


class Session:
    def __init__(self, user_id, balance, token):
        self.user_id = user_id
        self.balance = balance
        self.token = token

    def hash_data(self):
        data = f"{self.user_id}:{str(self.balance)}:{self.token}".encode()
        return hashlib.sha256(data).hexdigest()


def input_numeric(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Invalid input. Please enter a non-negative numeric value.")


def calculate_total_hash(sub_hashes):
    while len(sub_hashes) > 1:
        parent_hashes = []
        for i in range(0, len(sub_hashes), 2):
            if i + 1 < len(sub_hashes):
                data = f"{sub_hashes[i]}{sub_hashes[i + 1]}".encode()
                parent_hash = hashlib.sha256(data).hexdigest()
                parent_hashes.append(parent_hash)
            else:
                parent_hashes.append(sub_hashes[i])
        sub_hashes = parent_hashes

    return sub_hashes[0] if sub_hashes else None


def process_session(sessions, token_balances):
    logging.info("--- New Session ---")
    user_id = input_numeric("Please enter your User ID: ")

    token_choices = [
        inquirer.List("token", message="Select token:", choices=["BTC", "ETH", "DAI"])
    ]
    token = inquirer.prompt(token_choices)["token"]

    balance = input_numeric("Enter your balance: ")
    token_balances[token] = token_balances.get(token, 0) + balance

    session = Session(user_id, balance, token)
    sub_hash = session.hash_data()
    sessions.append(sub_hash)

    token_sums = {}
    for session_hash in sessions:
        session_parts = session_hash.split(":")
        if len(session_parts) == 3:
            session_token = session_parts[2]
            session_balance = float(session_parts[1])
            token_sums[session_token] = (
                token_sums.get(session_token, 0) + session_balance
            )

    logging.info("New Session Data Recorded.")
    for session_token, token_sum in token_sums.items():
        logging.info(f"Token: {session_token}, Sum: {token_sum}")

    total_hash = calculate_total_hash(sessions)
    logging.info(f"Total Hash: {total_hash}")

    return sessions, total_hash


def check_session(sessions):
    logging.info("--- Check Session ---")
    user_id = input_numeric("Please enter your User ID: ")

    token_choices = [
        inquirer.List("token", message="Select token:", choices=["BTC", "ETH", "DAI"])
    ]
    token = inquirer.prompt(token_choices)["token"]

    balance = input_numeric("Enter your balance: ")

    check_session = Session(user_id, balance, token)
    check_hash = check_session.hash_data()

    if check_hash in sessions:
        logging.info("YES, proof of reserve is recorded")
    else:
        logging.info("NO, proof of reserve is not recorded")


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )
    sessions = []
    total_hash = None
    token_balances = {"BTC": 0, "ETH": 0, "DAI": 0}
    first_session = True

    while True:
        if first_session:
            sessions, total_hash = process_session(sessions, token_balances)
            first_session = False
        else:
            options = [
                inquirer.List(
                    "action",
                    message="Select an action:",
                    choices=[
                        "Add PoR",
                        "Check PoR",
                        "Show Sum",
                        "End Script",
                    ],
                )
            ]
            action = inquirer.prompt(options)["action"]

            if action == "Add PoR":
                sessions, total_hash = process_session(sessions, token_balances)
            elif action == "Check PoR":
                check_session(sessions)
            elif action == "Show Sum":
                # Display total hash and token balances
                logging.info("Total Hash: {}".format(total_hash))
                logging.info("Summary of Token Balances:")
                for token, balance in token_balances.items():
                    logging.info(f"Token: {token}, Balance: {balance}")
            elif action == "End Script":
                break  # Terminate the program
            else:
                logging.info("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
