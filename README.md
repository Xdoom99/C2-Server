# C2 Server

C2 Server is a Command and Control (C2) framework designed for managing remote clients. It allows you to execute commands on remote systems, maintain persistent connections, and manage multiple sessions through a centralized server interface.

## Features

- **Multi-client support**: Handle multiple clients simultaneously.
- **Command execution**: Execute system commands on remote clients.
- **Session management**: Manage active sessions and interact with individual clients.
- **Persistence**: Techniques to maintain persistent connections on target systems.
- **Cross-platform payloads**: Generate payloads for Windows and Linux.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: `prettytable`, `base64`, `socket`

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/C2Server.git
    cd C2Server
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. **Start the C2 Server:**

    ```sh
    python3 c2_server.py
    ```

2. **Commands:**

    - `help` - Show the help menu.
    - `listeners -g` - Generate a new listener.
    - `winplant py` - Generate a Windows-compatible Python payload.
    - `linplant py` - Generate a Linux-compatible Python payload.
    - `exeplant` - Generate an executable payload for Windows.
    - `pshell_shell` - Generate a PowerShell cradle payload.
    - `sessions -1` - List active sessions.
    - `session -i <id>` - Interact with a specific session.
    - `kill <id>` - Terminate a specific session.

3. **Example:**

    - Generate a listener:
        ```sh
        enter command#> listeners -g
        [+] Enter IP: 127.0.0.1
        [+] Enter Port: 1234
        ```
    - Generate a Windows payload:
        ```sh
        enter command#> winplant py
        [+] Copied winplant.py to <random_name>.py
        ```

    - List active sessions:
        ```sh
        enter command#> sessions -1
        ```

    - Interact with a session:
        ```sh
        enter command#> session -i 0
        ```

## Files

- `c2_server.py`: Main server script.
- `client.py`: Example client script for connecting to the server.
- `winplant.py`: Template for Windows payloads.
- `linplant.py`: Template for Linux payloads.
- `exeplant.py`: Template for Windows executable payloads.
- `requirements.txt`: Required Python libraries.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [ASCII Art](https://www.asciiart.eu)
- [Python](https://www.python.org/)

---

**Note**: This tool is intended for educational and authorized testing purposes only. Unauthorized use of this tool is prohibited.
