"""Pytest configuration for the API-driven console tests.

The old direct-SQL viewer fixtures were removed with the legacy routes. Console
route tests now patch BackendClient and never open local SQLite files.
"""
