"""Verify sshd hardening configuration."""

import pytest


def test_sshd_config_exists(host):
    """sshd_config must exist as a regular file with mode 0600."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.exists
    assert f.is_file
    assert oct(f.mode) == "0o600"


@pytest.mark.parametrize(
    "setting",
    [
        "PermitRootLogin no",
        "PasswordAuthentication no",
        "PubkeyAuthentication yes",
        "PermitEmptyPasswords no",
        "KbdInteractiveAuthentication no",
        "MaxAuthTries 3",
        "LoginGraceTime 30",
        "ClientAliveInterval 300",
        "ClientAliveCountMax 2",
        "MaxSessions 3",
        "X11Forwarding no",
        "PrintMotd no",
        "UsePAM yes",
    ],
)
def test_sshd_hardened_setting(host, setting):
    """Each hardened sshd setting must be present in the config."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains(setting)


@pytest.mark.parametrize(
    "directive",
    [
        "Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,"
        "aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr",
        "MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,"
        "umac-128-etm@openssh.com",
        "KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,"
        "diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,"
        "diffie-hellman-group-exchange-sha256",
        "HostKeyAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256",
    ],
)
def test_sshd_algorithm_directive(host, directive):
    """Algorithm hardening directives must be present in sshd_config."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains(directive)


@pytest.mark.parametrize(
    "host_key",
    [
        "HostKey /etc/ssh/ssh_host_rsa_key",
        "HostKey /etc/ssh/ssh_host_ed25519_key",
    ],
)
def test_sshd_host_key_directive(host, host_key):
    """Host key directives must be present in sshd_config."""
    f = host.file("/etc/ssh/sshd_config")
    assert f.contains(host_key)


def test_sshd_sftp_subsystem(host):
    """Subsystem sftp must use the distro-correct path."""
    f = host.file("/etc/ssh/sshd_config")
    if host.system_info.distribution in ("arch", "archlinux"):
        assert f.contains("Subsystem sftp /usr/lib/ssh/sftp-server")
    else:
        assert f.contains("Subsystem sftp /usr/lib/openssh/sftp-server")


@pytest.mark.parametrize(
    "weak",
    [
        "aes128-cbc",
        "aes256-cbc",
        "3des-cbc",
        "arcfour",
        "hmac-sha1 ",
        "hmac-md5",
        "diffie-hellman-group1-sha1",
        "diffie-hellman-group14-sha1",
        "ssh-dss",
        "ecdsa-sha2",
    ],
)
def test_sshd_no_weak_algorithm(host, weak):
    """Weak algorithms must NOT be present in sshd_config."""
    f = host.file("/etc/ssh/sshd_config")
    assert not f.contains(weak)


@pytest.mark.vm_only
def test_sshd_service_running(host):
    """sshd service must be running and enabled (VM only)."""
    svc_name = "sshd"
    if host.system_info.distribution in ("ubuntu", "debian"):
        svc_name = "ssh"
    svc = host.service(svc_name)
    assert svc.is_running
    assert svc.is_enabled
