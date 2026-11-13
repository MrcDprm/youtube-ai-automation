"""Configuration package: constants in ``config.constants``, settings in ``config.settings``.

Nothing is imported here on purpose. ``config.settings`` imports ``utils.exceptions``, which
imports ``config.constants``; loading ``config.settings`` from this file closed that loop and
crashed any program that imported a ``utils`` module before ``config``.
"""
