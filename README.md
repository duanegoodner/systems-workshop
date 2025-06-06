# 🛠️ systems-workshop

This repo gathers smaller-scale tools and demos related to systems programming and infrastructure. Topics include low-level I/O, process and signal management, access control, backup automation, and environment tooling.

All included projects are tracked as Git submodules and live inside the `projects/` directory. This allows each tool to remain independently versioned while making them easy to explore as a group. See below for cloning instructions if you're unfamiliar with Git submodules.

---

## 📦 Included Projects

| Submodule         | Description |
|-------------------|-------------|
| [`assembly-io`](https://github.com/duanegoodner/assembly-io) | MASM-based 32-bit Windows program for low-level integer I/O and mean calculation. Demonstrates the verbosity and intricacy of even basic tasks in Assembly. |
| [`smallsh`](https://github.com/duanegoodner/smallsh) | A lightweight Linux shell written in C. Supports job control, I/O redirection, and foreground/background process management. |
| [`pygetfacl`](https://github.com/duanegoodner/pygetfacl) | Python wrapper for the Linux `getfacl` command. Converts ACL information into structured Python objects for programmatic access. |
| [`btrfs-restic`](https://github.com/duanegoodner/btrfs-restic) | Backup tool that snapshots BTRFS subvolumes and sends them to a remote Restic repository. Emphasizes snapshot-based consistency and simple, secure remote storage. |
| [`convertpytoml`](https://github.com/duanegoodner/convertpytoml) | Command-line utility to convert pyproject.toml files between pip-style and Poetry-style formats. Helps smooth workflow transitions between packaging tools. |


---

## 🔄 Cloning the Full Workspace

This repository uses Git submodules. To clone it with all nested projects included:

```bash
git clone --recurse-submodules https://github.com/duanegoodner/systems-workshop.git
```

If you’ve already cloned the repo and need to initialize the submodules afterward:

```
git submodule update --init --recursive
```

## 🧩 Contributing
This is a personal collection of exploratory systems tools and demos. Feel free to fork, explore, and adapt individual components to your needs. If you have ideas for new additions or enhancements, open an issue or PR in the relevant submodule.

## ⚖️ License

Each submodule includes its own license file, which governs usage of that component. Please consult individual repos for terms.
