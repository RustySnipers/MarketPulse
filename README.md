# Market Pulse

Market Pulse is a Python-based application designed for tracking day trades, particularly options. This application offers features like user authentication, trade input, an analytics dashboard, and printable reports.

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
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **User Authentication**: Secure login and user management.
- **Trade Input**: Easy input and management of trades.
- **Analytics Dashboard**: Visual representation of trade performance.
- **Printable Reports**: Generate and print detailed reports of trading activities.

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

    \`\`\`bash
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
    tar -xzf ta-lib-0.4.0-src.tar.gz
    cd ta-lib
    ./configure --prefix=/usr
    make
    sudo make install
    cd ..
    pip install ta-lib
    \`\`\`

## Usage

### Running the Application

After setting up the environment and installing dependencies, you can run the application using the following command:

\`\`\`bash
python main.py
\`\`\`

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

## Contributing

We welcome contributions! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature/YourFeature\`).
3. Make your changes and commit them (\`git commit -m 'Add some feature'\`).
4. Push to the branch (\`git push origin feature/YourFeature\`).
5. Create a new Pull Request.

## License

Distributed under the MIT License. See \`LICENSE\` for more information.
