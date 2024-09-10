#  Ethereum Deposit Tracker 🎉

**Ethereum Deposit Tracker**! 🚀 This project is designed to monitor and record ETH deposits on the Beacon Deposit Contract efficiently and robustly. With real-time tracking, detailed logging, and alerting features, this tracker ensures you're always up-to-date with Ethereum deposits.

##  Objective 🎯

Develop a robust and efficient Ethereum Deposit Tracker to:
- Monitor ETH deposits on the Beacon Deposit Contract.
- Record deposit details including amount, sender address, timestamp, etc.
- Handle multiple deposits in a single transaction.



##  Project Components🛠️

### Language/Framework

- **Python**: Used for backend logic and integration.
- **Docker**: Containerizes the application for consistency and ease of deployment.
- **Grafana**: For vizualization
- **Postgres**: For Storage

### RPC Integration

- **Alchemy API**: Connects to Ethereum's blockchain to fetch deposit data.
- **Functions**: Handle real-time data fetching and processing.

### Deposit Tracking Logic

- **Contract Address**: Monitors the Beacon Deposit Contract (`0x00000000219ab540356cBB839Cbe05303d7705Fa`).
- **Data Recording**: Stores deposit details in a database.

### Error Handling and Logging

- **Comprehensive Error Handling**: For API calls and RPC interactions.
- **Logging Mechanisms**: Tracks errors and important events for debugging.

### Alerting and Notifications

- **Grafana Dashboard**: Visualizes deposit data and system metrics.
- **Telegram Notifications**: Alerts users of new deposits.

### Documentation

- **Setup Process**: Includes environment configuration and dependency installation.
- **Usage Instructions**: Detailed guide on how to use the tracker.
- **Code Comments**: Ensures readability and maintenance.

## 📁 Project Structure

