"""Verify non-default variable values in alternate scenario."""


def test_editor_is_nano(host):
    """bashrc must export EDITOR=nano."""
    u = host.user("altuser1")
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains('export EDITOR="nano"')
    assert f.contains('export VISUAL="nano"')


def test_histsize_is_5000(host):
    """bashrc must export HISTSIZE=5000."""
    u = host.user("altuser1")
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains("export HISTSIZE=5000")
    assert f.contains("export HISTFILESIZE=5000")


def test_tree_package_installed(host):
    """tree binary must exist from base_extra_packages."""
    assert host.file("/usr/bin/tree").exists


def test_altuser1_exists(host):
    """altuser1 must exist."""
    u = host.user("altuser1")
    assert u.exists


def test_altuser1_authorized_keys(host):
    """altuser1 authorized_keys must contain the expected key."""
    u = host.user("altuser1")
    f = host.file("%s/.ssh/authorized_keys" % u.home)
    assert f.exists
    assert f.contains("alt-key-1")
