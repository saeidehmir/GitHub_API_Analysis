#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jan   2024

@author: saeideh
"""

from .top_repos import top_repos
from .top_users import top_users
import logging
import yaml
import requests
import matplotlib.pyplot as plt
import sys


class Analysis:
    ''' Load config into an Analysis object

    Load system-wide configuration from `configs/system_config.yml`, user configuration from
    `configs/user_config.yml`, and the specified analysis configuration file
    
    Parameters
    ----------
    analysis_config : str
        Path to the analysis/job-specific configuration file
    
    Returns
    -------
    analysis_obj : Analysis
        Analysis object containing consolidated parameters from the configuration files
    
    Notes
    -----
    The configuration files should include parameters for:
        * GitHub API token
        * Plot color
        * Plot title
        * Plot x and y axis titles
        * Figure size
        * Default save path
    '''
    def __init__(self, analysis_config):
        self.system_config = self.load_config('configs/system_config.yml')
        self.user_config = self.load_config('configs/user_config.yml')
        self.analysis_config = self.load_config(analysis_config)
        self.data = None
        self.starred_repos_data = None
        self.top_users_data = None
        if self.analysis_config["data_source"] != "GitHub":
            print("Currently, only GitHub analysis is supported")
            sys.exit(0)

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
        '''Analyze previously-loaded data.
        This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
        and returns the data in a format of your choice.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        Note: analysis_output is saved into data attribute
        
        '''
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
        ''' Analyze and plot data
        Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
        the path from the configuration file if not specified.
        
        Parameters
        ----------
        save_path : str, optional
            Save path for the generated figure
        
        Returns
        -------
        fig : matplotlib.Figure
        
        '''

        # data plotting
        analysis_type = self.analysis_config.get('analysis_type')
        figure_size = self.system_config.get('figure_size', [14, 8])
        figsize = (figure_size[0], figure_size[1])
        if analysis_type == 'repo':
            # Visualization with Matplotlib
            plt.figure(figsize=figsize)
            plt.subplot(2, 1, 1)
            repo_names, repo_stars = zip(*self.data)
            plt.barh(repo_names, repo_stars, color=self.system_config["plot_color"])
            plt.xlabel(self.system_config["plot_x_axis_title"])
            plt.ylabel(self.system_config["plot_y_axis_title"])
            plt.title(self.system_config["plot_title"])
            plt.tight_layout()
            plt.show()
        if analysis_type == 'user':
            # Visualization with Matplotlib
            plt.figure(figsize=figsize)
            user_logins, user_followers = zip(*self.data)
            plt.subplot(2, 1, 2)
            plt.barh(user_logins, range(1, self.user_config["N_users"]+1), color=self.system_config["plot_color"])  # Placeholder for followers
            plt.xlabel(self.system_config["plot_x_axis_title"])
            plt.ylabel(self.system_config["plot_y_axis_title"])
            plt.title(self.system_config["plot_title"])
            plt.tight_layout()
            plt.show()

        if self.system_config.get('default_save_path'):
            plt.savefig(self.system_config.get('default_save_path'))
        plt.show()
