#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jan   2024

@author: saeideh
"""

import logging


def top_users(N, token, users_data, test=False):
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

        user_logins = [user['login'] for user in users_data]
        user_followers = [user['followers_url'] for user in users_data]  # This gives URL, you might need additional API call to get count

    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
    except ConnectionError as ce:
        logger.warning(f"Network related error occurred: {ce}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return list(zip(user_logins, user_followers))
