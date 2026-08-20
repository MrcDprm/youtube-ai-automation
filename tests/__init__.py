"""Offline test suite.

Every test in this package runs without network access and without API keys. Providers are
served by ``requests_mock``, speech synthesis is monkeypatched, and the Google client is never
constructed.
"""
