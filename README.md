# GPResult
---
The **documentation** can be found at this [link](https://alt-domain.altlinux.team/gpresult).

---

The program is designed to display applied user and machine policies in ALT Linux OS.

GPResult retrieves the applied policies from the `alterator-backend-gpresult` D-Bus service via [`libalterator-glib`](https://altlinux.space/alterator/libalterator-glib). The policies themselves are applied by [`gpupdate`](https://github.com/altlinux/gpupdate), which writes the GPO/GPT settings that the backend then reads.

---
## Required packages
The package is based on the [Sisyphus](https://packages.altlinux.org/ru/sisyphus/) repository.

The `gpresult` package depends on the following packages:

```bash
rpm-build-python3
gettext-tools
python3-module-distro
libalterator-glib
```
---
## Summary
GPResult is a console utility. Help on available options can be obtained with the command `gpresult --help`.

The project supports **Russian** and **English** languages. The system language is used by default.

---
## TODO
> Add error handling

> Get away from using getpwnam

> View applied policies on different nodes for different users

> Which groups the user is a member of

> ...
