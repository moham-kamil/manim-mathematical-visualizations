# Publication handoff

The repository was created publicly with the author's explicit authorization:
https://github.com/moham-kamil/manim-mathematical-visualizations

The instructions below are retained as a guide for creating another copy or
maintaining this project.

## Repository settings

- Name: `manim-mathematical-visualizations`
- Description: A collection of mathematical visualizations and educational animations created with Python and Manim, featuring matrix operations, linear algebra, and procedural mathematical animation.
- Suggested topics: `manim`, `python`, `mathematical-visualization`, `linear-algebra`, `animation`, `gauss-jordan`
- Default branch: `main`

## Rights decision before publication

No `LICENSE` has been added. `RIGHTS.md` reserves the author's rights. This is
intentional: an MIT or Apache-2.0 license would allow others to reuse the code
commercially under its terms. Selecting an open-source license is a separate
decision for Mohamed Kamil. A public GitHub repository allows viewing and forking
under GitHub's terms even without an open-source license; making it private later
does not retrieve copies already obtained.

Keep the existing rights notice if the intent is portfolio review without a
general reuse grant. Read [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
before making this decision. No claim is made that this notice prevents all
copying or replaces a license tailored to a specific collaboration.

## Upload only after the author decides to publish

Extract the package and keep the directory structure intact. The ZIP includes
the hidden `.github` folder and `.gitignore`. From the project directory:

```bash
git init -b main
git add .
git commit -m "Add standalone Manim mathematical visualizations"
```

Then create an **empty** repository on GitHub using the settings above. Do not
ask GitHub to create a README, `.gitignore` or license automatically. After
reviewing the destination and visibility, the author can connect and push it:

```bash
git remote add origin https://github.com/moham-kamil/manim-mathematical-visualizations.git
git push -u origin main
```

These commands are instructions for the author, not actions already taken.
After publication, confirm GIF rendering on the actual repository page and check
the first Actions run before linking the project in an application.

## Video storage

The four selected H.264 files are deliberately short and small enough to bundle.
Do not add Manim's `media/` tree. For future long/high-bitrate videos, attach
exports to GitHub Releases and link them from README instead of accumulating
large video revisions in git history.
