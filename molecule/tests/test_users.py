"""Verify per-user configuration (parameterized via test_user fixture)."""


def test_user_exists(host, test_user):
    """User account must exist."""
    u = host.user(test_user["name"])
    assert u.exists


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


def test_authorized_keys_file(host, test_user):
    """authorized_keys must exist with mode 0600."""
    u = host.user(test_user["name"])
    f = host.file("%s/.ssh/authorized_keys" % u.home)
    assert f.exists
    assert f.is_file
    assert oct(f.mode) == "0o600"


def test_authorized_keys_content(host, test_user):
    """authorized_keys must contain all expected key comments."""
    u = host.user(test_user["name"])
    f = host.file("%s/.ssh/authorized_keys" % u.home)
    for key in test_user["expected_keys"]:
        assert f.contains(key)


def test_profile_exists(host, test_user):
    """~/.config/profile must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/profile" % u.home)
    assert f.exists
    assert f.is_file


def test_profile_content(host, test_user):
    """Profile must contain PATH, bashrc source, and profile.d loop."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/profile" % u.home)
    assert f.contains(".local/bin")
    assert f.contains("bashrc")
    assert f.contains("profile.d")
    assert f.contains(r"\*\.conf")


def test_profiled_directory(host, test_user):
    """~/.config/profile.d/ must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/profile.d" % u.home)
    assert f.exists
    assert f.is_directory


def test_bash_config_directory(host, test_user):
    """~/.config/bash/ must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash" % u.home)
    assert f.exists
    assert f.is_directory


def test_bash_confd_directory(host, test_user):
    """~/.config/bash/conf.d/ must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/conf.d" % u.home)
    assert f.exists
    assert f.is_directory


def test_readline_config_directory(host, test_user):
    """~/.config/readline/ must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/readline" % u.home)
    assert f.exists
    assert f.is_directory


def test_bashrc_exists(host, test_user):
    """~/.config/bash/bashrc must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bashrc" % u.home)
    assert f.exists
    assert f.is_file


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


def test_bash_profile_exists(host, test_user):
    """~/.config/bash/bash_profile must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bash_profile" % u.home)
    assert f.exists
    assert f.is_file


def test_bash_profile_sources_profile(host, test_user):
    """bash_profile must source ~/.profile."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/bash/bash_profile" % u.home)
    assert f.contains(r"\. ~/\.profile")


def test_inputrc_exists(host, test_user):
    """~/.config/readline/inputrc must exist."""
    u = host.user(test_user["name"])
    f = host.file("%s/.config/readline/inputrc" % u.home)
    assert f.exists
    assert f.is_file


def test_symlink_bash_profile(host, test_user):
    """~/.bash_profile must be a symlink to .config/bash/bash_profile."""
    u = host.user(test_user["name"])
    f = host.file("%s/.bash_profile" % u.home)
    assert f.is_symlink
    assert f.linked_to == "%s/.config/bash/bash_profile" % u.home


def test_symlink_bashrc(host, test_user):
    """~/.bashrc must be a symlink to .config/bash/bashrc."""
    u = host.user(test_user["name"])
    f = host.file("%s/.bashrc" % u.home)
    assert f.is_symlink
    assert f.linked_to == "%s/.config/bash/bashrc" % u.home


def test_symlink_profile(host, test_user):
    """~/.profile must be a symlink to .config/profile."""
    u = host.user(test_user["name"])
    f = host.file("%s/.profile" % u.home)
    assert f.is_symlink
    assert f.linked_to == "%s/.config/profile" % u.home


def test_symlink_inputrc(host, test_user):
    """~/.inputrc must be a symlink to .config/readline/inputrc."""
    u = host.user(test_user["name"])
    f = host.file("%s/.inputrc" % u.home)
    assert f.is_symlink
    assert f.linked_to == "%s/.config/readline/inputrc" % u.home


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
