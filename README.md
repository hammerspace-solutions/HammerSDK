# HammerSDK

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

The HammerSDK is a Python software development kit designed to simplify interaction with the Hammerspace API. It provides a convenient and Pythonic way to automate and manage your Hammerspace environment.

---

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Copyright and License](#copyright-and-license)

---

## Introduction

This SDK is a client library for the Hammerspace REST API. It handles the details of authentication, request signing, and response parsing, allowing you to focus on building powerful automation and integration scripts for your Hammerspace data orchestration.

---

## Installation

You can install the HammerSDK using pip:

```bash
pip install HammerSDK
```

---

## Quick Start

Here's a simple example of how to connect to a Hammerspace Anvil, log in, and list the configured nodes:

```python
from HammerSDK.hammer_client import HammerClient
import os

# --- Configuration ---
# It's recommended to use environment variables for credentials
anvil_host = os.environ.get("HAMMERSPACE_HOST", "your-anvil-hostname")
anvil_user = os.environ.get("HAMMERSPACE_USER", "admin")
anvil_pass = os.environ.get("HAMMERSPACE_PASSWORD", "your-password")

try:
    # 1. Create a client instance
    # For development with self-signed certs, you might need:
    # client = HammerClient(anvil_host, verify="/path/to/your/anvil.crt")
    client = HammerClient(anvil_host)

    # 2. Log in to the Anvil
    client.login(anvil_user, anvil_pass)
    print("Successfully logged in to Hammerspace!")

    # 3. Use the SDK to interact with the API
    print("\nFetching list of nodes...")
    nodes = client.nodes.list_nodes()

    if nodes:
        for node in nodes:
            print(f"- Node Name: {node.get('name')}, State: {node.get('nodeState')}")
    else:
        print("No nodes found.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 4. The connection will close automatically, but you can be explicit
    if 'client' in locals():
        client.close()
        print("\nConnection closed.")
```

---

## Features

* **Full API Coverage:** Provides access to all Hammerspace REST API endpoints for comprehensive management.
* **Clean, Pythonic Interface:** Interacting with the API feels natural and straightforward.
* **Automatic Task Polling:** Handles asynchronous operations by automatically polling for task completion.
* **Custom Exceptions:** Rich, specific exceptions for better error handling and more robust scripts.
* **Well-Documented:** Clear docstrings and type hinting for better developer experience and IDE integration.

---

## Documentation

For a complete guide to all available modules and functions, please see the **[Full API Documentation](https://your-documentation-url-here.com)**. *(Note: Link is a placeholder)*

---

## Contributing

We welcome contributions! To post feedback, submit feature ideas, or report bugs, please use the **Issues** section of this GitHub repository. For details on how to contribute code, please see our [CONTRIBUTING](CONTRIBUTING.md) file.

---

## Copyright and License

Copyright © 2023-2025 [Hammerspace](https://hammerspace.com/)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

All other trademarks referenced herein are the property of their respective owners.

### Contributors

* [Michael Kade](https://github.com/mikekade)
