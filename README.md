# Ethereum Deposit Tracker 🎉

Welcome to the **Ethereum Deposit Tracker**! 🚀 This project is designed to monitor and record ETH deposits on the Beacon Deposit Contract efficiently and robustly. With real-time tracking, detailed logging, and alerting features, this tracker ensures you're always up-to-date with Ethereum deposits.

## Objective 🎯

Develop a robust and efficient Ethereum Deposit Tracker to:
- Monitor ETH deposits on the Beacon Deposit Contract.
- Record deposit details including amount, sender address, timestamp, etc.
- Handle multiple deposits in a single transaction.

## 🚀 Installation Guide

### Prerequisites
Make sure you have the following installed:

- Docker
- Docker Compose
- Alchemy API Key: For interacting with the Ethereum blockchain.
- Python 3.9 or higher

### Step-by-Step Installation

1. **Clone the Repository:**

   ```
   git clone https://github.com/An-Yay/Luganodes-sde-task.git
   cd Luganodes-sde-task
   ```

2. **Install requirements:**

   ```
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables:**

   Copy the .env.example to .env:

   ```
   cp .env.example .env
   ```

   Fill in your environment variables in the .env file, including:
   - `ALCHEMY_API_KEY`: Your Alchemy API key 🔑
   - `DATABASE_URL`: The connection string for your PostgreSQL database 🗄️
   - `TELEGRAM_NOTIFICATIONS_BOT_TOKEN`: Telegram bot token for notifications 📲
   - `TELEGRAM_NOTIFICATIONS_CHAT_ID`: Chat ID for Telegram alerts 💬
   - `BEACON_DEPOSIT_CONTRACT_ADDRESS`: The address of the Beacon Deposit Contract

4. **Build and Run the Docker Containers:**

   ```
   docker-compose up --build
   ```

   This will:
   - 🗄️ Build and run the Postgres database.
   - ⚙️ Run the Ethereum deposit tracker Python app.
   - 📊 Set up Grafana for visualization.



## Setting up Grafana Dashboards 📊

### Creating the Deposit Table Dashboard

1. Access Grafana by entering `localhost:3001` in your browser.

2. Log in with the following credentials:
   ```
   Email: admin
   Password: admin
   ```

3. Click to create a new dashboard.

4. Add PostgreSQL as a data source with the following configuration:
   ```
   Connection:
   Host URL: postgres:5432
   Database name: grafana

   Authentication:
   Username: grafana
   Password: grafana
   ```

5. Add a new visualization:
   - Select PostgreSQL as the data source
   - Select table `deposits` and column `*`
   - Run the query
   - Switch to table view

Here's what your Grafana dashboard should look like:

![Grafana Dashboard](/assets/images/grafana/image.png)

### Importing the cAdvisor Dashboard

1. Click to import a dashboard.

2. Load the dashboard with ID `19792`.

3. For the Prometheus dropdown, click to configure a new data source:
   - Select Prometheus
   - Use `http://prometheus:9090` as the Prometheus server URL

4. Finally, import the cAdvisor dashboard.

## Docker Setup 🐳

Our project uses Docker for easy deployment and management. Here are some screenshots of the Docker setup:

![Docker Setup 1](/assets/images/docker/image.png)
![Docker Setup 2](/assets/images/docker/image2.png)

## Telegram Notifications 📱

### Bot Setup
1. **Obtain your BOT API Token:**
   - Text @BotFather on Telegram to create a new bot and get your API token.

2. **Set up your Telegram group:**
   - Create a new Telegram group.
   - Add @raw_data_bot
   - Add your bot to this group.

3. **Get your Chat ID:**
   - Send a message to your bot in the group.
   - Visit `https://api.telegram.org/bot<YOUR_BOT_API_TOKEN>/getUpdates` in your browser.
   - Look for the "chat" object in the JSON response and find the "id" field. This is your Chat ID.

4. **Configure your .env file:**
   - Add your Bot API Token to the `TELEGRAM_NOTIFICATIONS_BOT_TOKEN` variable.
   - Add your Chat ID to the `TELEGRAM_NOTIFICATIONS_CHAT_ID` variable.

Once set up, you'll receive alerts for new deposits. Here's what they look like:

![Telegram Notification 1](assets/images/telegram/img1.png)
![Telegram Notification 2](assets/images/telegram/img2.png)
![Telegram Notification 3](assets/images/telegram/img3.png)

If you've set up Telegram notifications, you'll receive alerts for new deposits. Here's what they look like:

![Telegram Notification 1](/assets/images/telegram/img4.png)
![Telegram Notification 2](/assets/images/telegram/img5.png)
![Telegram Notification 3](/assets/images/telegram/img6.png)

## Usage

After installation, the tracker will automatically start monitoring the Beacon Deposit Contract for new deposits. You can view the collected data and metrics through the Grafana dashboard.

6. **Telegram Alerts (Optional):**

   If configured, you will start receiving Telegram notifications for each new Ethereum deposit 📲.

## Project Components 🛠️

### Language/Framework

- **Python**: Used for backend logic and integration.
- **Docker**: Containerizes the application for consistency and ease of deployment.
- **Grafana**: For visualization.
- **Postgres**: For storage.

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

## 📁 Project Structure

```
C:.
│   .dockerignore
│   .env
│   .env.example
│   .gitignore
│   docker-compose.yml
│   Dockerfile
│   prometheus.yml
│   README.md
│   requirements.txt
│   schema.sql
│
├───app
│       app.py
│       config.py
│       db.py
│       logger.py
│       migrations.py
│       notifications.py
│       test.py
│       tracker.py
│       utils.py
│
├───assets
│   ├───images
│   │   ├───docker
│   │   │       image.png
│   │   │       image2.png
│   │   │
│   │   ├───grafana
│   │   │       image.png
│   │   │
│   │   └───telegram
│   │           img1.png
│   │           img2.png
│   │           img3.png
│   │
│   └───videos
│           do-not-open-this.gif
│
└───grafana
    └───provisioning
        ├───dashboards
        └───datasources
                postgres.yml
```



## Troubleshooting

If you encounter any issues during setup or operation, please check the following:

1. Ensure all environment variables are correctly set in your `.env` file.
2. Verify that all required ports are available and not being used by other applications.
3. Check the Docker logs for any error messages:
   ```
   docker-compose logs
   ```

If problems persist, please open an issue in this repository with a detailed description of the problem and any relevant log outputs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Ethereum Foundation for the Beacon Chain specifications.
- Alchemy for providing robust Ethereum API services.

## Support

If you encounter any problems or have any questions, please open an issue in this repository.

Happy tracking! 🎉
