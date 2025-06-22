def test_import():
    import organizer.cli as cli
    assert callable(cli.main)
