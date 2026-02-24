# Base Role

Layer 1 Ansible role applied to **all hosts**. Handles core system
configuration that every machine needs.

## What It Does

- Installs essential packages (distro-aware: `base-devel` on Arch,
  `build-essential` on Debian/Ubuntu)
- Creates user accounts with distro-appropriate sudo group
- Deploys sudoers drop-ins for passwordless sudo (configurable per user)
- Manages `~/.ssh/authorized_keys` for key-only authentication (per user)
- Sets timezone and locale
- Deploys a hardened `/etc/ssh/sshd_config`
- Sets up XDG shell skeleton (`~/.config/bash/`, `~/.config/profile.d/`)
  with `conf.d/` and `profile.d/` sourcing loops, plus symlinks
  (`~/.bashrc`, `~/.profile`, `~/.inputrc`)

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
- **Authorized keys deployment**: Public keys are deployed per user to
  `~/.ssh/authorized_keys`. Actual key values belong in the controller
  inventory (`group_vars/all.yml`), not in role defaults
- **Sudoers management**: A validated sudoers drop-in is deployed per user.
  The admin group (`wheel` on Arch, `sudo` on Debian/Ubuntu) is automatically
  assigned based on the distribution

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `base_users` | `[]` | List of user accounts to create |
| `base_extra_packages` | `[]` | Additional packages beyond the base set |
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
| `base_editor` | `vim` | Default EDITOR/VISUAL |
| `base_histsize` | `10000` | Bash HISTSIZE |

### Per-User Properties

Each entry in `base_users` supports:

| Property | Default | Description |
|---|---|---|
| `name` | (required) | Username |
| `groups` | `[]` | Additional groups (admin group is added automatically) |
| `shell` | `/bin/bash` | Login shell |
| `create_home` | `true` | Create home directory |
| `authorized_keys` | `[]` | List of SSH public key strings |
| `sudo_passwordless` | `true` | Grant passwordless sudo |

## Shell Skeleton

The role deploys an XDG-compliant shell configuration per user:

```
~/.config/
  profile        # PATH, bashrc source, then profile.d/ sourcing loop
  profile.d/     # drop-in directory for higher-order roles

~/.config/bash/
  bashrc         # conf.d/ sourcing loop, XDG exports, EDITOR, HISTSIZE
  conf.d/        # drop-in directory for other roles

~/.config/readline/
  inputrc        # readline settings
```

The login profile at `~/.config/profile` sets up `~/.local/bin` PATH and
sources bashrc, then sources all `*.conf` files from `~/.config/profile.d/`.
Higher-order roles (server, workstation) can extend or override the login
profile by dropping files into `profile.d/`.

Symlinks are created for compatibility:
- `~/.bashrc` -> `.config/bash/bashrc`
- `~/.profile` -> `.config/profile`
- `~/.inputrc` -> `.config/readline/inputrc`

## Collection Dependencies

This role requires the following Ansible collections:

- `ansible.posix` — `authorized_key` module
- `community.general` — `timezone` and `locale_gen` modules

Install them with:

```bash
ansible-galaxy collection install -r meta/requirements.yml
```

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
