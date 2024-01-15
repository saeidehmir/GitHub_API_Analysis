#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jan  2024

@author: saeideh
"""

import unittest
from GithubAnalysis.top_repos import top_repos
from GithubAnalysis.top_users import top_users

class TestTopRepos(unittest.TestCase):
    def test_get_top_repos_returns_data(self):
        """Test that the function returns a list of tuples with the correct length."""
        N = 5
        result = top_repos(N, None, None, test=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), N)

class TestTopUsers(unittest.TestCase):
    def test_get_top_users_returns_data(self):
        """Test that the function returns a list of tuples with the correct length."""
        N = 5
        result = top_users(N, None, None, test=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), N)

if __name__ == '__main__':
    unittest.main()