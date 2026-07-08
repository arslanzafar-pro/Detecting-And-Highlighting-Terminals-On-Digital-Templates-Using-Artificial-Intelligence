# How to publish this wiki to GitHub

These files are ready-made **GitHub Wiki** pages. GitHub stores a repo's wiki in a separate git repository at `<repo>.wiki.git`. To publish:

## 1. Enable the wiki (one-time)
On GitHub: open the repo → **Settings** → **Features** → tick **Wikis**.
Then open the **Wiki** tab and click **Create the first page** → Save (this initializes the wiki repo so it can be cloned).

## 2. Clone the wiki repo and copy these files in

```bash
# Clone the wiki (note the .wiki.git suffix)
git clone https://github.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence.wiki.git
cd Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence.wiki

# Copy all wiki .md files from this folder into the clone
# (copy everything EXCEPT this HOW-TO-PUBLISH.md file)

git add .
git commit -m "Add project wiki"
git push
```

On Windows PowerShell, the copy step is:

```powershell
Copy-Item "D:\Detecting-Terminals-Wiki\*.md" -Destination . -Exclude "HOW-TO-PUBLISH.md"
```

## 3. Done
Refresh the repo's **Wiki** tab. `Home.md` becomes the landing page, `_Sidebar.md` renders as the navigation panel, and `_Footer.md` shows at the bottom of every page.

---

## Page list

| File | Wiki page |
|------|-----------|
| `Home.md` | Landing page |
| `_Sidebar.md` | Navigation sidebar (auto-rendered) |
| `_Footer.md` | Footer on every page (auto-rendered) |
| `Background-and-Problem.md` | Background & Problem |
| `How-It-Works.md` | How It Works (pipeline + images) |
| `Architecture.md` | Architecture (Mermaid diagram) |
| `Tech-Stack.md` | Tech Stack |
| `Results.md` | Results / metrics |
| `Installation.md` | Installation |
| `Usage.md` | Usage |
| `Project-Structure.md` | Project Structure |
| `Limitations-and-Future-Work.md` | Limitations & Future Work |
| `FAQ.md` | FAQ |

## Notes
- **Images** use absolute `raw.githubusercontent.com` URLs pointing at `main/assets/images/…`, so they render on the wiki as long as those images stay in the main repo on the `main` branch.
- **Mermaid** diagrams (in `Architecture.md`) render natively on GitHub wikis — no extra setup.
- **Internal links** use the page-name form GitHub expects (e.g. `[How It Works](How-It-Works)`), matching the filenames without the `.md` extension.
- Do **not** copy `HOW-TO-PUBLISH.md` into the wiki — it's just this guide.
