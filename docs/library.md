# The glinet library

The protocol layer that this integration talks to is published as a
standalone Python package: [`glinet`](https://github.com/vithurshanselvarajah/python-glinet-router).

The integration depends on it via `requirements: ["glinet==0.0.1"]` in
[its manifest](../custom_components/glinet_router/manifest.json).
The library is the only place that imports `aiohttp` and `passlib` —
this integration stays thin.

## Where the docs live

| Page | What's in it |
| --- | --- |
| [glinet wiki home](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/Home.md) | Landing page with a high-level overview and the full doc index. |
| [Authentication](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/authentication.md) | Challenge/response login, supported hashers, and how to register a new one. |
| [Errors](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/errors.md) | Exception hierarchy and the router error code → Python exception mapping. |
| [Architecture](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/architecture.md) | Internal module map, request lifecycle, and design notes. |
| [Router API notes](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/router-api.md) | Endpoint, payload structure, and full module inventory. |
| [Modem API coverage](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/modem-api.md) | Firmware 4.8 vs 4.9 differences and the helpers in `client.modem`. |
| [VPN](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/vpn.md) | WireGuard and OpenVPN client/server, including the unified 4.8/4.9 paths. |
| [Tailscale](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/tailscale.md) | Connection states, retry helpers. |
| [Repeater](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/repeater.md) | Scan, connect, saved-APs, bare mode. |
| [Firewall](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/firewall.md) | Rules, ACLs, port forwards, DMZ, WAN access, zones. |
| [Parental control](https://github.com/vithurshanselvarajah/python-glinet-router/blob/main/docs/parental-control.md) | Groups, time-window rules, filtering mode. |

## When to edit the library vs the integration

- **Edit the library** when:
  - You need to talk to a new router endpoint.
  - The shape of a raw response changes.
  - You want to refactor the protocol layer for reuse outside Home Assistant.

- **Edit the integration** when:
  - You want to add or change a Home Assistant entity, service, or config-flow step.
  - You want to change the polling cadence or coordinator behaviour.
  - You want to change the HA-specific data model (`models.py`).

## Versioning and breaking changes

The library uses [Semantic Versioning](https://semver.org/):

- **Patch** (`0.0.x`): internal refactors, new module methods, bug fixes.
- **Minor** (`0.x.0`): new modules, new public names, backward-compatible
  changes to existing method signatures.
- **Major** (`x.0.0`): breaking changes to existing method signatures,
  renamed/removed public names.

The integration pins the library version in `manifest.json`. Bump the
pin in the same PR that adds the new library version. See the
[release process in the integration's `CONTRIBUTING.md`](../CONTRIBUTING.md#release-process).
