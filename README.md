# Base Role

Layer 1 Ansible role applied to **all hosts**. Handles core system
configuration that every machine needs.

## What It Does

- Installs essential packages (distro-aware: `base-devel` on Arch,
  `build-essential` on Debian/Ubuntu)
- Creates the primary admin user account with distro-appropriate sudo group
- Deploys a sudoers drop-in for passwordless sudo (configurable)
- Sets timezone and locale
- Deploys a hardened `/etc/ssh/sshd_config`
- Manages `~/.ssh/authorized_keys` for key-only authentication
- Sets up XDG shell skeleton (`~/.config/bash/`) with `conf.d/` sourcing
  loop and symlinks (`~/.bashrc`, `~/.profile`, `~/.inputrc`)

## Supported Platforms

- Arch Linux
- Ubuntu 24.04
- Debian 12

## Security Model

The base role enforces a security-first configuration on all hosts:

- **Hardened sshd**: Root login disabled, password auth disabled, brute-force
  limits (MaxAuthTries, LoginGraceTime), idle session cleanup
  (ClientAliveInterval/CountMax), session multiplexing limits (MaxSessions)
- **Key-only authentication**: PubkeyAuthentication enabled, passwords and
  keyboard-interactive auth disabled
- **Authorized keys deployment**: Public keys are deployed to the admin user's
  `~/.ssh/authorized_keys`. Actual key values belong in the controller
  inventory (`group_vars/all.yml`), not in role defaults
- **Sudoers management**: A validated sudoers drop-in is deployed per admin
  user. The admin group (`wheel` on Arch, `sudo` on Debian/Ubuntu) is
  automatically assigned based on the distribution

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `base_extra_packages` | `[]` | Additional packages beyond the base set |
| `base_user` | `bwright` | Primary admin username |
| `base_user_groups` | `[]` | Additional groups for the user |
| `base_user_shell` | `/bin/bash` | Login shell |
| `base_user_create_home` | `true` | Create home directory |
| `base_timezone` | `America/New_York` | System timezone |
| `base_locale` | `en_US.UTF-8` | System locale |
| `base_sshd_port` | `22` | SSH port |
| `base_sshd_permit_root_login` | `no` | Root SSH login |
| `base_sshd_password_authentication` | `no` | Password auth |
| `base_sshd_pubkey_authentication` | `yes` | Pubkey auth |
| `base_sshd_x11_forwarding` | `no` | X11 forwarding |
| `base_sshd_max_auth_tries` | `3` | Max authentication attempts |
| `base_sshd_login_grace_time` | `30` | Login grace period (seconds) |
| `base_sshd_client_alive_interval` | `300` | Client alive check interval (seconds) |
| `base_sshd_client_alive_count_max` | `2` | Max missed client alive checks |
| `base_sshd_max_sessions` | `3` | Max multiplexed sessions |
| `base_authorized_keys` | `[]` | List of SSH public key strings |
| `base_sudo_passwordless` | `true` | Grant passwordless sudo |
| `base_editor` | `vim` | Default EDITOR/VISUAL |
| `base_histsize` | `10000` | Bash HISTSIZE |

## Shell Skeleton

The role deploys an XDG-compliant bash configuration:

```
~/.config/bash/
  bashrc       # conf.d/ sourcing loop, XDG exports, EDITOR, HISTSIZE
  profile      # sources bashrc, adds ~/.local/bin to PATH
  inputrc      # readline settings
  conf.d/      # drop-in directory for other roles
```

Symlinks are created for compatibility:
- `~/.bashrc` -> `.config/bash/bashrc`
- `~/.profile` -> `.config/bash/profile`
- `~/.inputrc` -> `.config/bash/inputrc`

## Testing

### Prerequisites

- Python 3 + pip
- Docker (running)
- Install the toolchain:

```bash
pip install ansible-core ansible-lint yamllint molecule molecule-plugins[docker]
ansible-galaxy collection install community.general ansible.posix
```

### Lint (fast — run before every commit)

```bash
yamllint .
ansible-lint
```

### Molecule (full integration test)

```bash
# Run full test suite (lint + converge + verify + destroy)
molecule test

# Converge and keep containers running for debugging
molecule converge
molecule login -h archlinux
molecule verify
molecule destroy
```

## License

MIT
