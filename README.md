# GitHub API Analysis
Author: Saeideh Mirjalili

A Python package to fetch and visualize the top N starred repositories or top N followed users on GitHub.

## Description

Depending on the type of analysis, the package plots top N repositories on GitHub sorted by the number of stars, or top N users with the highest number of followers. It utilizes the GitHub API to retrieve repository data and then visualizes the results. The scripts include comprehensive error handling, logging, and user input validation for robust performance.

## Getting Started

### Dependencies

- Python 3.x
- `requests` library for API calls
- `matplotlib` library for visualization
- `logging` library for logging

Ensure you have the above dependencies installed in your Python environment.

### Installing

- Clone this repository using `git clone https://github.com/saeidehmir/GitHub_API_Analysis.git`.
- Navigate into the repository folder.

or use the following command:
pip install git+https://github.com/saeidehmir/GitHub_API_Analysis.git

### Running Tests

To run the tests, navigate to the test directory and execute:
```bash
python test_my_package.py
```


### Example

- Run the script using Python:

  ```bash
  !pip install git+https://github.com/saeidehmir/GitHub_API_Analysis.git
  from from GithubAnalysis import Analysis

  analysis_obj = Analysis('./configs/config.yml')
  analysis_obj.load_data()
  analysis_obj.compute_analysis()
  analysis_obj.plot_data()
  ```
