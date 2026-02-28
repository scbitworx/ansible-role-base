"""Verify non-default variable values in alternate scenario."""


def test_editor_is_nano(host):
    """bashrc must export EDITOR=nano and not the default vim."""
    u = host.user("altuser1")
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains("export EDITOR='nano'")
    assert f.contains("export VISUAL='nano'")
    assert not f.contains("EDITOR='vim'")
    assert not f.contains("VISUAL='vim'")


def test_histsize_is_5000(host):
    """bashrc must export HISTSIZE=5000 and not the default 10000."""
    u = host.user("altuser1")
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains("export HISTSIZE=5000")
    assert f.contains("export HISTFILESIZE=5000")
    assert not f.contains("HISTSIZE=10000")
    assert not f.contains("HISTFILESIZE=10000")


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


def test_sshd_max_auth_tries_override(host):
    """sshd_config must reflect overridden MaxAuthTries."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains("MaxAuthTries 5")
    assert not f.contains("MaxAuthTries 3")


def test_sshd_max_sessions_override(host):
    """sshd_config must reflect overridden MaxSessions."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains("MaxSessions 5")
    assert not f.contains("MaxSessions 3")


def test_sshd_allow_groups(host):
    """sshd_config must contain AllowGroups directive when set."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains("AllowGroups wheel")


def test_sshd_banner(host):
    """sshd_config must contain Banner directive when set."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains("Banner /etc/issue")


def test_timezone_override(host):
    """Timezone must reflect the overridden value (UTC)."""
    result = host.run("timedatectl show --property=Timezone --value")
    assert result.stdout.strip() == "UTC"


def test_locale_override(host):
    """/etc/locale.conf must reflect the overridden locale."""
    f = host.file("/etc/locale.conf")
    assert f.exists
    assert f.contains("LANG=C.UTF-8")
