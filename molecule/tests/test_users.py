"""Verify per-user configuration (parameterized via test_user fixture)."""

import pytest


def test_user_exists(host, test_user):
    """User account must exist."""
    u = host.user(test_user["name"])
    assert u.exists


def test_user_shell(host, test_user):
    """User must have the correct login shell."""
    u = host.user(test_user["name"])
    assert u.shell == "/bin/bash"


def test_home_directory(host, test_user):
    """Home directory must exist, be owned by the user."""
    u = host.user(test_user["name"])
    f = host.file(u.home)
    assert f.exists
    assert f.is_directory
    assert f.user == test_user["name"]
    assert f.group == test_user["name"]


def test_user_private_group(host, test_user):
    """User's primary group must match username (UPG convention)."""
    u = host.user(test_user["name"])
    assert u.group == test_user["name"]


def test_user_in_admin_group(host, test_user, admin_group):
    """User must be a member of the OS admin group (wheel/sudo)."""
    u = host.user(test_user["name"])
    assert admin_group in u.groups


def test_sudoers_dropin_exists(host, test_user):
    """Sudoers drop-in must exist with mode 0440."""
    f = host.file("/etc/sudoers.d/%s" % test_user["name"])
    assert f.exists
    assert f.is_file
    assert oct(f.mode) == "0o440"


def test_sudoers_dropin_content(host, test_user):
    """Sudoers drop-in must match the sudo_passwordless setting."""
    f = host.file("/etc/sudoers.d/%s" % test_user["name"])
    if test_user["sudo_passwordless"]:
        assert f.contains("NOPASSWD")
    else:
        assert not f.contains("NOPASSWD")
        assert f.contains("%s ALL=" % test_user["name"])


def test_ssh_directory(host, test_user):
    """~/.ssh must exist with mode 0700, owned by the user."""
    u = host.user(test_user["name"])
    f = host.file("%s/.ssh" % u.home)
    assert f.exists
    assert f.is_directory
    assert oct(f.mode) == "0o700"
    assert f.user == test_user["name"]
    assert f.group == test_user["name"]


def test_authorized_keys_file(host, test_user):
    """authorized_keys must exist with mode 0600, owned by the user."""
    u = host.user(test_user["name"])
    f = host.file("%s/.ssh/authorized_keys" % u.home)
    assert f.exists
    assert f.is_file
    assert oct(f.mode) == "0o600"
    assert f.user == test_user["name"]
    assert f.group == test_user["name"]


def test_authorized_keys_content(host, test_user):
    """authorized_keys must contain all expected key comments."""
    u = host.user(test_user["name"])
    f = host.file("%s/.ssh/authorized_keys" % u.home)
    for key in test_user["expected_keys"]:
        assert f.contains(key)


def test_authorized_keys_exclusive(host, test_user):
    """authorized_keys must not contain keys outside the expected set."""
    u = host.user(test_user["name"])
    result = host.run("wc -l < %s/.ssh/authorized_keys" % u.home)
    line_count = int(result.stdout.strip())
    assert line_count == len(test_user["expected_keys"])


@pytest.mark.parametrize(
    "subpath",
    [
        ".config/profile.d",
        ".config/bash",
        ".config/bash/conf.d",
        ".config/readline",
    ],
)
def test_config_directory(host, test_user, subpath):
    """XDG config subdirectories must exist, owned by the user."""
    u = host.user(test_user["name"])
    f = host.file("%s/%s" % (u.home, subpath))
    assert f.exists
    assert f.is_directory
    assert f.user == test_user["name"]
    assert f.group == test_user["name"]


@pytest.mark.parametrize(
    "subpath",
    [
        ".config/profile",
        ".config/bash/bashrc",
        ".config/bash/bash_profile",
        ".config/readline/inputrc",
    ],
)
def test_config_file_ownership(host, test_user, subpath):
    """Shell config files must exist as regular files, owned by the user."""
    u = host.user(test_user["name"])
    f = host.file("%s/%s" % (u.home, subpath))
    assert f.exists
    assert f.is_file
    assert f.user == test_user["name"]
    assert f.group == test_user["name"]


def test_profile_content(host, test_user):
    """Profile must contain PATH, bashrc source, and profile.d loop."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/profile" % u.home)
    assert f.contains(".local/bin")
    assert f.contains("bashrc")
    assert f.contains("profile.d")
    assert f.contains(r"\*\.conf")


def test_bashrc_confd_sourcing(host, test_user):
    """bashrc must contain conf.d sourcing loop."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains(r"conf\.d/\*\.bash")


def test_bashrc_editor_visual(host, test_user):
    """bashrc must export EDITOR and VISUAL."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains("export EDITOR=")
    assert f.contains("export VISUAL=")


def test_bashrc_histsize(host, test_user):
    """bashrc must export HISTSIZE and HISTFILESIZE."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains("export HISTSIZE=")
    assert f.contains("export HISTFILESIZE=")


def test_bashrc_xdg_dirs(host, test_user):
    """bashrc must export XDG base directories."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.contains("export XDG_CONFIG_HOME=")
    assert f.contains("export XDG_DATA_HOME=")
    assert f.contains("export XDG_STATE_HOME=")
    assert f.contains("export XDG_CACHE_HOME=")


def test_bash_profile_sources_profile(host, test_user):
    """bash_profile must source ~/.profile."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bash_profile" % u.home)
    assert f.contains(r"\. ~/\.profile")


@pytest.mark.parametrize(
    ("link_name", "target"),
    [
        (".bash_profile", ".config/bash/bash_profile"),
        (".bashrc", ".config/bash/bashrc"),
        (".profile", ".config/profile"),
        (".inputrc", ".config/readline/inputrc"),
    ],
)
def test_home_symlink(host, test_user, link_name, target):
    """Home directory symlinks must point to XDG config locations."""
    u = host.user(test_user["name"])
    f = host.file("%s/%s" % (u.home, link_name))
    assert f.is_symlink
    assert f.linked_to == "%s/%s" % (u.home, target)


def test_password_hash_set(host, test_user):
    """Users with password_hash=True must have a SHA-512 hash in shadow."""
    if not test_user["password_hash"]:
        return
    result = host.run("getent shadow %s" % test_user["name"])
    shadow_hash = result.stdout.split(":")[1]
    assert shadow_hash.startswith("$6$")


def test_account_locked_when_no_password(host, test_user):
    """Users without password_hash must have a locked account."""
    if test_user["password_hash"]:
        return
    result = host.run("getent shadow %s" % test_user["name"])
    shadow_hash = result.stdout.split(":")[1]
    assert shadow_hash in ("!", "*", "!!", "")
