#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 22:03:04 2024

@author: saeideh
"""

import requests
import json
import matplotlib.pyplot as plt
import logging


def get_top_repos(N, test=False):
    # Setting up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    if test is True:
        results = []
        for i in range(N):
            results.append(("MyRepo", 1000))
        return results
    try:
        token = input("Please provide your GitHub token:\n")
        if not token:
            raise ValueError("GitHub token is missing. Please provide a valid token.")
    
        # Setting up GitHub API interaction
        url = "https://api.github.com/user"
        headers = {"Authorization": "Bearer " + token}
    
        # Fetching user data
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise ConnectionError(f"Failed to fetch user data: {r.status_code} - {r.text}")
    
        r_json = json.loads(r.text)
        logger.info("User data fetched successfully.")
        logger.debug(r_json)  # Debug message with user data
    
        # Fetch top 10 starred repos
        repos_response = requests.get('https://api.github.com/search/repositories?q=stars:>1&sort=stars', headers=headers)
        if repos_response.status_code != 200:
            raise ConnectionError(f"Failed to fetch repositories: {repos_response.status_code} - {repos_response.text}")
        starred_repos = repos_response.json()['items'][:N]
    
        # Extracting data for visualization
        repo_names = [repo['name'] for repo in starred_repos]
        repo_stars = [repo['stargazers_count'] for repo in starred_repos]
    
        # Visualization with Matplotlib
        plt.figure(figsize=(14, 8))
    
        plt.subplot(2, 1, 1)
        plt.barh(repo_names, repo_stars, color='skyblue')
        plt.xlabel('Stars')
        plt.title(f'Top {N} Starred GitHub Repositories')
        plt.tight_layout()
    
        plt.show()
    
    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
    except ConnectionError as ce:
        logger.warning(f"Network related error occurred: {ce}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return list(zip(repo_names, repo_stars))