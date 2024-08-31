# Installation

To install the library and set up the Git hook automatically:

```
pip install -e .
```

If you don't want to set up the Git hook automatically, you can install the library without it:

```
pip install --no-deps -e .
```

After installation, you can manually set up the Git hook by running:

```
python -c "from mycodeuncle.setup_hook import install_git_hook; install_git_hook()"
```