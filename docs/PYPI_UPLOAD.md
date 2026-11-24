# Publishing `scriber-core` to PyPI

This repository publishes through GitHub Actions **Trusted Publishing (OIDC)**. No PyPI API token or `.pypirc` file is needed. The PyPI distribution remains `scriber-core`; its Python import package and command are `eigenscribe`.

## One-time publisher setup

The `scriber-core` PyPI project already exists. In PyPI, open **scriber-core → Settings → Publishing → Add a new publisher** and enter:

| Setting | Value |
| :--- | :--- |
| Owner | `The-Scriber-Experience` |
| Repository | `scriber-core` |
| Workflow | `publish.yml` |
| Environment | `pypi` |

In GitHub repository settings, create an environment named `pypi`. Optionally require reviewer approval there so a release cannot publish without your review. For optional TestPyPI validation, configure its Trusted Publisher with the same owner/repository/workflow and environment `testpypi`, and create that GitHub environment too.

## Before a release

For each release, move the completed notes from `[Unreleased]` under the new version and release date, then create a fresh `[Unreleased]` section. Confirm `pyproject.toml` and `src/eigenscribe/__init__.py` have the same version; the frontend and CLI versions derive from the package version. The `scriber_core` → `eigenscribe` import migration was introduced in `2.0.0` and is not part of this release.

From PowerShell at the repository root, run:

```powershell
uv sync --extra dev
uv run pytest tests
uv build
```

Review the built `.whl` and `.tar.gz` files in `dist/`; `uv build` is also run in CI after the test matrix passes. Do not upload existing files in `dist/` manually: the release workflow builds fresh artifacts from the tagged commit.

## Optional TestPyPI rehearsal

After the release commit is pushed, open the repository's **Actions → Publish to PyPI → Run workflow**, select that commit's branch, and leave the target as `testpypi`. This manual path publishes only to TestPyPI. Check the workflow result and, if desired, install `scriber-core==2.0.2` from TestPyPI in a disposable environment to verify its `eigenscribe` import and CLI. TestPyPI and production PyPI are separate indexes.

## Production release steps

1. Review `git status`, `git diff`, and the test/build results. Stage only the intended release files; do not stage unrelated work accidentally.
2. Commit the reviewed changes and push that commit to the repository's default branch. For a repository whose default branch is `main`, the commands are:

   ```powershell
   git status --short
   git diff --check
   git add <reviewed-paths>
   git diff --cached --check
   git diff --cached
   git commit -m "Prepare v2.0.2 release"
   git push origin main
   ```

   Replace `<reviewed-paths>` with the explicit paths you have reviewed; it is a placeholder, not a command to copy literally. Avoid `git add .` if unrelated or user-owned edits are present.

3. Create and push an annotated tag that exactly matches the version in `pyproject.toml`:

   ```powershell
   git tag -a v2.0.2 -m "Release 2.0.2"
   git push origin v2.0.2
   ```

4. The tag starts the workflow. It runs tests on Python 3.10–3.12, checks that the tag matches `pyproject.toml`, builds and smoke-tests the wheel, then publishes to PyPI using OIDC. Watch **GitHub → Actions** until the `Publish to PyPI` job succeeds, then verify the release at <https://pypi.org/project/scriber-core/>.
5. Test the public install in a clean environment with `pip install --upgrade scriber-core`, then check `eigenscribe --version` and `python -c "import eigenscribe; print(eigenscribe.__version__)"`.

Production publishing is tag-triggered only; a manual workflow run cannot select PyPI. PyPI does not allow reusing a published version: if a release has already uploaded, fix the problem in a new patch release rather than trying to overwrite that version.

## Names and migration

- PyPI install/distribution name: `scriber-core`
- Python import namespace: `eigenscribe` (including `eigenscribe.frontend` and `eigenscribe.cli`)
- Console command: `eigenscribe`
- Existing consumers must migrate imports from `scriber_core` to `eigenscribe`; this breaking change was introduced in `2.0.0`.
