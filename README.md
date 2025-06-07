# Market Pulse

Market Pulse is a Python-based application designed for tracking day trades, particularly options. This application offers features like user authentication, trade input, an analytics dashboard, and printable reports.

## Windows Quick Start

1. Double-click `install.bat`
2. Click **Install**
3. Click **Launch**

Updates are automatically offered at startup.

*GIFs demonstrating the install and update flows were omitted from this repository.*

## Table of Contents

- [Market Pulse](#market-pulse)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [Building the Executable](#building-the-executable)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **User Authentication**: Secure login and user management.
- **Trade Input**: Easy input and management of trades.
- **Analytics Dashboard**: Visual representation of trade performance.
- **Printable Reports**: Generate and print detailed reports of trading activities.
- **Interactive Calendar**: View and filter market events with color-coded severity and type.
- **Custom Watchlists**: Manage your own list of tickers or import them from your Webull portfolio.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following software installed:

- [Python 3.9+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [TA-Lib](http://ta-lib.org/)
- [PyInstaller](https://www.pyinstaller.org/)

### Installation

1. **Clone the Repository**

    \`\`\`bash
    git clone https://github.com/your-username/market-pulse.git
    cd market-pulse
    \`\`\`

2. **Set Up Virtual Environment**

    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use \`venv\\Scripts\\activate\`
    \`\`\`

3. **Install Dependencies**

    \`\`\`bash
    pip install --upgrade pip
    pip install -r requirements.txt
    \`\`\`

4. **Install TA-Lib**

    ```bash
    pip install TA-Lib==0.4.28
    ```

## Usage

### Running the Application

After setting up the environment and installing dependencies, you can run the application using the following command:

\`\`\`bash
python main.py
\`\`\`
Alternatively, double-click one of the provided start scripts:

- **Windows**: `start_app.bat`
- **macOS/Linux**: `start_app.sh`

These scripts launch `main.py` for you so a terminal isn't required.

### Managing Watchlists and Webull Portfolio

When the GUI is running you can enter a comma-separated list of tickers to set a custom watchlist. Use the **Load Webull Portfolio** button to import your holdings from your Webull account. Credentials are requested at runtime and are never saved.

### Settings and Symbol Review

The application now includes a **Settings** window for adjusting the data CSV path and other options. Use the **Review Symbols** button to open a window showing your current watchlist and loaded portfolio for quick reference.

### Discord Notifications

Set the `DISCORD_WEBHOOK_URL` environment variable to send trading events and
report summaries to a Discord channel. The application will post messages when
trading starts or stops, watchlists change, portfolios are loaded, and when
backtesting or ML training completes.

### Building the Executable

To build an executable using PyInstaller, follow these steps:

1. **Activate Virtual Environment**

    \`\`\`bash
    source venv/bin/activate  # On Windows, use \`venv\\Scripts\\activate\`
    \`\`\`

2. **Install PyInstaller**

    \`\`\`bash
    pip install pyinstaller
    \`\`\`

3. **Build the Executable**

    \`\`\`bash
    pyinstaller --onefile main.py
    \`\`\`

4. **Locate the Executable**

The executable will be located in the \`dist\` directory.

## Testing

Run the automated test suite after installing dependencies:

```bash
pip install -r requirements.txt
pytest
```

## Contributing

We welcome contributions! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature/YourFeature\`).
3. Make your changes and commit them (\`git commit -m 'Add some feature'\`).
4. Push to the branch (\`git push origin feature/YourFeature\`).
5. Create a new Pull Request.

## License

Distributed under the MIT License. See \`LICENSE\` for more information.
