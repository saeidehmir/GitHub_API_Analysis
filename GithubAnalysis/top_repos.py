#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jan   2024

@author: saeideh
"""

import logging


def top_repos(N, token, starred_repos, test=False):
    # Setting up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    if test is True:
        results = []
        for i in range(N):
            results.append(("MyRepo", 1000))
        return results
    try:
        if not token:
            raise ValueError("GitHub token is missing. Please provide a valid token.")

        # Extracting data for visualization
        repo_names = [repo['name'] for repo in starred_repos]
        repo_stars = [repo['stargazers_count'] for repo in starred_repos]

    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
    except ConnectionError as ce:
        logger.warning(f"Network related error occurred: {ce}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return list(zip(repo_names, repo_stars))
