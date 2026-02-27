"""Shared fixtures and configuration for Testinfra tests."""

import os

import pytest


@pytest.fixture()
def admin_group(host):
    """Return the OS-appropriate admin group name."""
    if host.system_info.distribution in ("arch", "archlinux"):
        return "wheel"
    return "sudo"


@pytest.fixture(
    params=[
        {
            "name": "testuser1",
            "expected_keys": ["test-key-1", "test-key-2"],
            "password_hash": True,
            "sudo_passwordless": True,
        },
        {
            "name": "testuser2",
            "expected_keys": ["test-key-3"],
            "password_hash": False,
            "sudo_passwordless": True,
        },
        {
            "name": "testuser3",
            "expected_keys": ["test-key-4"],
            "password_hash": False,
            "sudo_passwordless": False,
        },
    ],
    ids=["testuser1", "testuser2", "testuser3"],
)
def test_user(request):
    """Parameterized fixture yielding each test user dict."""
    return request.param


def is_docker():
    """Return True if running under Docker (not a VM)."""
    return os.environ.get("MOLECULE_DRIVER_NAME", "docker") == "docker"


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "vm_only: mark test to run only on VM scenarios (skip on Docker)"
    )


def pytest_collection_modifyitems(config, items):
    """Skip vm_only tests when running under Docker."""
    if is_docker():
        skip_docker = pytest.mark.skip(reason="VM-only test, skipping on Docker")
        for item in items:
            if "vm_only" in item.keywords:
                item.add_marker(skip_docker)
