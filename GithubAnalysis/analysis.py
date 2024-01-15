#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jan   2024

@author: saeideh
"""

from top_repos import top_repos
from top_users import top_users
import logging
import yaml
import requests


class Analysis:
    def __init__(self, analysis_config):
        self.system_config = self.load_config('configs/system_config.yml')
        self.user_config = self.load_config('configs/user_config.yml')
        self.analysis_config = self.load_config(analysis_config)
        self.data = None
        self.starred_repos_data = None
        self.top_users_data = None

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Config file '{config_file}' not found.")
            raise

    def load_data(self):
        ''' Retrieve data from the GitHub API
        This function makes an HTTPS request to the GitHub API and retrieves your selected data. The data is
        stored in the Analysis object.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        
        '''
        # Setting up GitHub API interaction
        headers = {"Authorization": "Bearer " + self.system_config["github_api_token"]}
        # Fetch top N starred repos
        repos_response = requests.get('https://api.github.com/search/repositories?q=stars:>1&sort=stars', headers=headers)
        if repos_response.status_code != 200:
            raise ConnectionError(f"Failed to fetch repositories: {repos_response.status_code} - {repos_response.text}")
        self.starred_repos_data = repos_response.json()['items'][:self.user_config["N_repos"]]
        # Fetch top N followed users
        users_response = requests.get('https://api.github.com/search/users?q=followers:>1&sort=followers', headers=headers)
        self.top_users_data = users_response.json()['items'][:self.user_config["N_users"]]


    def compute_analysis(self):
        analysis_type = self.analysis_config.get('analysis_type')
        if analysis_type == 'repo':
            self.data = top_repos(self.user_config["N_repos"],
                                  self.system_config["github_api_token"],
                                  self.starred_repos_data,
                                  test=False)
        elif analysis_type == 'user':
            self.data = top_users(self.user_config["N_repos"],
                                  self.system_config["github_api_token"],
                                  self.top_users_data,
                                  test=False)
        else:
            logging.error(f"Invalid analysis type: {analysis_type}")
            raise ValueError(f"Invalid analysis type: {analysis_type}")


    def plot_data(self, save_path=None):
        import matplotlib.pyplot as plt

        # data plotting
        analysis_type = self.analysis_config.get('analysis_type')
        if analysis_type == 'repo':
            # Visualization with Matplotlib
            plt.figure(figsize=(14, 8))
            plt.subplot(2, 1, 1)
            repo_names, repo_stars = zip(*self.data)
            plt.barh(repo_names, repo_stars, color='skyblue')
            plt.xlabel('Stars')
            plt.title(f'Top {self.user_config["N_repos"]} Starred GitHub Repositories')
            plt.tight_layout()
            plt.show()
        if analysis_type == 'user':
            # Visualization with Matplotlib
            plt.figure(figsize=(14, 8))

            user_logins, user_followers = zip(*self.data)
            plt.subplot(2, 1, 2)
            plt.barh(user_logins, range(1, self.user_config["N_users"]+1), color='lightgreen')  # Placeholder for followers
            plt.xlabel('Followers (Placeholder)')
            plt.title(f'Top {self.user_config["N_users"]} Followed GitHub Users')
            plt.tight_layout()

            plt.show()
            pass

        if save_path:
            plt.savefig(save_path)
        plt.show()
