import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (requires LLM API key, "
        "use -m integration to run)",
    )
    config.addinivalue_line(
        "markers",
        "live_deepseek: mark test as live DeepSeek smoke test (requires explicit live env)",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("-m") or config.getoption("--markers"):
        return
    skip_integration = pytest.mark.skip(
        reason="integration test (use -m integration to run)"
    )
    for item in items:
        if "integration" in item.keywords or "live_deepseek" in item.keywords:
            item.add_marker(skip_integration)
