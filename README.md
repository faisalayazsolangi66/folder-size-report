# Folder Size Report

Report the size of each subfolder, largest first.

## Requirements

- Python 3.8+
- No third-party packages (standard library only)

## Usage

```bash
python3 main.py <folder> [--top N] [--human] [--include-files]
```

Sizes include all files in each subfolder recursively.

## Example

```bash
$ python3 main.py ./projects --human
videos/     1.2 GB  ########################################
photos/   340.5 MB  ###########
docs/       2.1 MB

Total: 1.5 GB across 3 shown entries.
```

## License

MIT — see [LICENSE](LICENSE).
