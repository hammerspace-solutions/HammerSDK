# Contributing to HammerSDK

First off, thank you for considering contributing to HammerSDK! It's people like you that make open source such a great community. We welcome any form of contribution, from reporting bugs and suggesting features to writing code and improving documentation.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior.

---

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for HammerSDK. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

- **Check the documentation** to see if the behavior is intended.
- **Perform a cursory search** on the issue tracker to see if the bug has already been reported.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://github.com/hammerspace-solutions/hammersdk/issues). Explain the problem and include additional details to help maintainers reproduce the problem:

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as much detail as possible.
- **Provide specific examples** by including code snippets or executable test cases.
- **Include details about your environment**, such as Python version, SDK version, and Hammerspace Anvil version.

---

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for HammerSDK, including completely new features and minor improvements to existing functionality.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/hammerspace-solutions/hammersdk/issues).

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as much detail as possible.
- **Explain why this enhancement would be useful** to most HammerSDK users.
- **Provide code examples** of how the feature would be used.

---

### Your First Code Contribution

Unsure where to begin contributing to HammerSDK? You can start by looking through these `good-first-issue` and `help-wanted` issues:

- **Good first issues** - issues which should only require a few lines of code, and a test or two.
- **Help wanted issues** - issues which should be a bit more involved than `good-first-issue` issues.

### Pull Requests

The process described here has several goals:

- Maintain HammerSDK's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible HammerSDK
- Enable a sustainable system for HammerSDK's maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1.  **Fork the repo** and create your branch from `main`.
2.  If you've added code that should be tested, **add tests**.
3.  If you've changed APIs, **update the documentation**.
4.  Ensure the **test suite passes**.
5.  Make sure your code **lints**.
6.  **Issue that pull request!**

---

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issues and pull requests liberally after the first line.

### Python Styleguide

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) and should be formatted with a tool like `black`. Docstrings should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#3.8-comments-and-docstrings).
