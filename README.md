# Proof of Reserve Python Script

This is a Python script that helps you track and verify the proof of reserve for different token balances in a financial system. It allows you to record sessions with user IDs, token balances, and generates a total hash for each session.

## Prerequisites

- Python 3.x

## Getting Started

1. Clone the repository or download the script file to your local machine.

2. Install the required dependencies by running the following command:
   ```shell
   pip install hashlib
   pip install logging
   pip install inquirer

3. Run the script by executing the following command:
   ```shell
   python por.py

4. Follow the prompts to add proof of reserve sessions, check sessions, show the total sum, or end the script.

## Usage

- **Add PoR**: Allows you to record a new proof of reserve session. You will be prompted to enter a user ID, select a token, and enter the token balance.

- **Check PoR**: Allows you to verify and check a specific proof of reserve session. You will be prompted to enter the user ID and select the token for the session.

- **Show Sum**: Displays the total hash and a summary of token balances for all recorded sessions.

- **End Script**: Terminates the script execution.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This script is licensed under the MIT License.
