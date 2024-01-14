# GitHub Top Repositories Fetcher
Author: Saeideh Mirjalili

A simple Python script to fetch and visualize the top N starred repositories on GitHub.

## Description

The `get_top_repos(N)` function fetches the top N repositories on GitHub sorted by the number of stars. It utilizes the GitHub API to retrieve repository data and then visualizes the top repositories and their star counts using a horizontal bar chart. The script includes comprehensive error handling, logging, and user input validation for robust performance.

## Getting Started

### Dependencies

- Python 3.x
- `requests` library for API calls
- `matplotlib` library for visualization
- `logging` library for logging

Ensure you have the above dependencies installed in your Python environment.

### Installing

- Clone this repository using `git clone [repository URL]`.
- Navigate into the repository folder.

or use the following command:
pip install git+https://github.com/saeidehmir/TopGithubRepos.git


### Executing Program

- Run the script using Python:

  ```bash
  python get_top_repos.py
