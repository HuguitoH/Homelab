# Homelab

Personal homelab running on a Raspberry Pi 5 — infrastructure as code, GitOps, and self-hosted services built for real backend infrastructure learning.

> If it's not in the repo, it doesn't exist.

---

## Hardware

| Component | Details |
|-----------|---------|
| Board | Raspberry Pi 5 8GB |
| Case | Argon NEO 5 BRED |
| OS Storage | SD Card 64GB |
| Data Storage | HDD 1TB USB 3.0 |
| Network | WiFi (Cloudflare Tunnel for external access) |

---

## Architecture

```
Internet
    │
    ▼
Cloudflare Tunnel          # no open ports, no router access needed
    │
    ▼
Nginx Proxy Manager        # reverse proxy + SSL termination
    │
    ├── api.hugohhm.dev    → hugo-api (Go REST API)
    ├── ssh.hugohhm.dev    → hugo-tui (SSH portfolio)
    ├── grafana.hugohhm.dev → Grafana dashboards
    └── ...
    
RPi 5 (Ubuntu Server 24.04)
    ├── Docker + Compose   # everything runs in containers
    ├── Observability      # Beszel + Prometheus + Grafana + Loki
    ├── Security           # Fail2ban + Trivy + SSL
    ├── CI/CD              # GitHub Actions + Ntfy
    └── Services           # Pi-hole + Vaultwarden + Jellyfin + Homepage
```

---

## Stack

### Infrastructure
| Tool | Purpose |
|------|---------|
| Ubuntu Server 24.04 | Base OS |
| Docker + Compose | Container orchestration |
| Nginx Proxy Manager | Reverse proxy + SSL |
| Cloudflare Tunnel | External access without open ports |

### Observability
| Tool | Purpose |
|------|---------|
| Beszel | Server and container monitoring |
| Prometheus | Application metrics (hugo-api) |
| Grafana | Dashboards + alert history |
| Loki + Promtail | Log aggregation |
| Uptime Kuma | Service availability monitoring |

### Security
| Tool | Purpose |
|------|---------|
| Fail2ban | SSH brute force protection |
| Trivy | CVE scanning in CI/CD pipeline |
| Dependabot | Dependency vulnerability alerts |
| SSL everywhere | Nginx + Let's Encrypt |

### DevOps
| Tool | Purpose |
|------|---------|
| GitHub Actions | CI/CD pipeline |
| Ntfy | Push notifications (deploys, alerts) |
| Diun | Docker image update notifications |

### Services
| Service | Purpose |
|---------|---------|
| Pi-hole | DNS ad-blocking (personal devices only) |
| Vaultwarden | Self-hosted password manager |
| Jellyfin | Media server |
| Homepage | Homelab dashboard portal |

---

## Storage Strategy

```
SD 64GB (OS + configs)
├── Ubuntu Server
├── Docker daemon
└── Repo configs

HDD 1TB USB (data)
├── docker/
│   ├── prometheus/    # metrics history
│   ├── loki/          # logs history
│   ├── vaultwarden/   # password vault
│   └── jellyfin/      # media
├── personal/          # personal files
└── backups/           # homelab backups
```

---

## Repo Structure

```
homelab/
├── docker-compose/
│   ├── base.yml           # Nginx, Cloudflare Tunnel
│   ├── monitoring.yml     # Prometheus, Grafana, Loki, Beszel, Uptime Kuma
│   ├── services.yml       # Pi-hole, Vaultwarden, Jellyfin, Homepage, Ntfy
│   └── portfolio.yml      # hugo-api, hugo-tui
├── nginx/
│   └── conf.d/
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   └── dashboards/
├── scripts/
│   ├── backup-vaultwarden.sh   # weekly backup
│   └── backup-logs.sh          # monthly backup
├── .env.example               # required env vars (no values)
├── .gitignore                 # .env always ignored
└── README.md
```

---

## GitOps Workflow

```
Change needed
    │
    ▼
Edit in repo (never directly on server)
    │
    ▼
git push → GitHub Actions → CI validation
    │
    ▼ (if green)
SSH to RPi → git pull → docker compose up -d
    │
    ▼
Ntfy notification → "Deploy successful ✅" or "Failed at [step] ❌"
```

---

## CI/CD Pipeline

Every push triggers:
1. Lint Docker Compose files
2. Validate Nginx configs
3. Security scan with Trivy
4. Deploy to sandbox (develop branch) or production (main branch)
5. Health check post-deploy
6. Ntfy notification with result

---

## Environments

| Environment | Branch | Domain |
|-------------|--------|--------|
| Production | `main` | hugohhm.dev |
| Sandbox | `develop` | dev.hugohhm.dev |

---

## Backup Strategy

| What | Frequency | Where |
|------|-----------|-------|
| Vaultwarden | Weekly (Sunday 2AM) | DigitalOcean Spaces (encrypted) |
| Loki logs | Monthly (1st, 3AM) | DigitalOcean Spaces (encrypted) |
| Infrastructure | Always | This repo |

---

## Secrets

Secrets are never committed to this repo.

- `.env` is in `.gitignore` — lives only on the server
- `.env.example` documents required variables without values
- GitHub Secrets used for CI/CD pipeline

---

## Phases

- [x] **Phase 1** — Base: Ubuntu Server, Docker, Nginx, Cloudflare Tunnel, domain
- [ ] **Phase 2** — Observability: Prometheus, Grafana, Loki, Beszel, Uptime Kuma
- [ ] **Phase 3** — DevOps: GitHub Actions CI/CD, Ntfy
- [ ] **Phase 4** — Services: Pi-hole, Vaultwarden, Jellyfin, Homepage
- [ ] **Phase 5** — AI: Ollama, agent-ops, agent-dev, agent-teacher

---

## Why Each Decision Was Made

**Ubuntu Server over Raspberry Pi OS** — production-grade environment from day one. Same OS family used in real servers.

**Docker over bare metal installs** — reproducible, isolated, easy to update. If a service breaks, only that container is affected.

**Cloudflare Tunnel over port forwarding** — shared student flat with no router access. Tunnel establishes outbound connection — no ports needed, HTTPS automatic.

**Beszel + Prometheus (not one or the other)** — Beszel monitors the server and containers. Prometheus monitors application metrics exposed by hugo-api. Different layers, different responsibilities.

**GitOps** — the repo is the source of truth. If the RPi dies tomorrow, `git clone` + `docker compose up` restores everything. No manual steps, no undocumented state.

**One repo for all homelab** — the homelab is a cohesive system, not a collection of independent projects. Nginx, Prometheus and services are all related. Separating them adds complexity without benefit.

---

*Built and maintained by [Hugo Hernández](https://github.com/hugohhm) — backend engineering student, Madrid.*
