# Den 1 – Základy Gitu, lokální repozitář, první commity, GitHub, AI jako pomocník

Časová dotace: cca 1–2 hodiny.

---

## 1. Teorie (cca 25–35 min)

### 1.1 Co je Git a co je GitHub

- **Git** je *distribuovaný systém pro správu verzí* (version control system, VCS). Běží lokálně
  na tvém počítači, nepotřebuje internet. Ukládá si "snímky" (snapshoty) stavu tvých souborů v čase.
- **GitHub** je webová služba, která hostuje Git repozitáře online. Přidává k Gitu:
  - zálohu/sdílení kódu,
  - spolupráci (Pull Requesty, code review, issues),
  - CI/CD (GitHub Actions),
  - a dnes i AI nástroje (GitHub Copilot, Copilot Chat, Copilot code review, agentické workflow).
- Git ≠ GitHub. Git můžeš používat čistě lokálně (bez GitHubu) a dnes si to i vyzkoušíme, než
  repozitář propojíme s GitHubem.

### 1.2 Tři vrstvy Gitu

```
Working Directory  --git add-->  Staging Area (Index)  --git commit-->  Repository (.git historie)
```

- **Working directory** – soubory tak, jak je vidíš a upravuješ v editoru.
- **Staging area (index)** – "čekárna" na to, co se dostane do dalšího commitu. `git add` sem
  přesune změny.
- **Repository** – trvalá historie commitů uložená ve složce `.git`.

### 1.3 Co je commit

Commit je *pojmenovaný snímek* stavu staging area v daném okamžiku. Má:
- unikátní hash (identifikátor, např. `a1b2c3d`),
- autora a čas,
- odkaz na rodičovský commit (proto historie tvoří řetězec/graf),
- zprávu (commit message) – měla by stručně a výstižně popsat *proč*, ne jen *co*.

Dobrá commit message: `Add subtraction function to calculator`
Špatná commit message: `update`, `fix`, `asdf`

### 1.4 Co je remote a `origin`

- **Remote** je "vzdálená" verze repozitáře (typicky na GitHubu).
- `origin` je jen zvykové jméno pro tvůj hlavní remote (dá se pojmenovat i jinak).
- `push` = pošli commity z lokálu na remote.
- `pull` = stáhni a slouč commity z remote do lokálu (ve skutečnosti `fetch` + `merge`).
- `clone` = stáhni celý existující repozitář z remote k sobě poprvé.

### 1.5 `.gitignore`

Soubor, který říká Gitu, co má ignorovat (např. `__pycache__/`, `.venv/`, `.vscode/`, dočasné
soubory). Zabraňuje zanesení repozitáře zbytečnostmi nebo citlivými soubory.

### 1.6 Git a AI – kde se dnes potkávají

- **AI chat asistent (např. Claude, ChatGPT, Copilot Chat)**: umí navrhnout commit message na
  základě `git diff`, vysvětlit cizí historii/commit, pomoct rozeplést merge konflikt, napsat
  `.gitignore` pro daný projekt.
- **AI agenti (např. Claude Code, GitHub Copilot Workspace/Agent)**: umí sami vytvořit větev,
  udělat sadu commitů, otevřít Pull Request, reagovat na komentáře v PR – tedy aktivně pracovat
  s Gitem, ne jen radit. V Dni 3 si ukážeme, jak takový workflow vypadá koncepčně a jak si ho
  můžeš vyzkoušet i ty (např. přes Claude Code nad tímto repozitářem).
- Důležité pravidlo: AI je pomocník, ne náhrada za pochopení – zejména u `merge`/`rebase`/`reset`
  je potřeba rozumět, co se děje, protože špatný krok může (opravitelně, ale nepříjemně) poškodit
  historii.

---

## 2. Praktická cvičení (cca 45–75 min)

> Předpoklad: máš nainstalovaný Git for Windows, VS Code s GitLens, Python, a GitHub účet.
> Otevři si terminál ve VS Code (`Ctrl + \``).

### Cvičení 1.1 – Ověření nastavení

Over, že Git je nainstalovaný a nastavený:

```bash
git --version
git config --global user.name
git config --global user.email
```

Pokud jméno/email nejsou nastavené, nastav je (GitHub commity je pak správně přiřadí k tobě):

```bash
git config --global user.name "Tvoje Jméno"
git config --global user.email "tvuj@email.cz"
```

### Cvičení 1.2 – Založení lokálního repozitáře

1. Vytvoř složku `C:\Projects\Git_withClaude` (pokud ještě neexistuje) a otevři ji ve VS Code.
2. V terminálu v této složce spusť:

```bash
git init
git status
```

3. Zkopíruj do složky soubor `start_kalkulacka.py` (přejmenuj na `kalkulacka.py`) a soubor
   `README.md` s krátkým popisem projektu (klidně jednu větu – "Cvičný projekt pro kurz Git/GitHub").

4. Spusť znovu `git status` – co vidíš? (Nápověda: soubory by měly být "untracked".)

### Cvičení 1.3 – `.gitignore`

Vytvoř soubor `.gitignore` s obsahem:

```
__pycache__/
*.pyc
.vscode/
```

Zkus si vytvořit i prázdnou složku `__pycache__` s libovolným souborem uvnitř a ověř přes
`git status`, že ji Git ignoruje.

### Cvičení 1.4 – První commit

1. Přidej soubory do staging area a zkontroluj rozdíl mezi `git status` před a po:

```bash
git add kalkulacka.py .gitignore README.md
git status
```

2. Udělej první commit:

```bash
git commit -m "Initial commit: add calculator script and gitignore"
```

3. Zobraz historii:

```bash
git log
git log --oneline
```

### Cvičení 1.5 – Druhá a třetí verze skriptu (postupné verzování)

1. V `kalkulacka.py` přidej funkci `multiply(a, b)` a v `if __name__ == "__main__":` bloku
   přidej ukázkové volání. Ulož soubor.
2. Zkontroluj rozdíl před commitem:

```bash
git diff
```

3. Přidej a commitni:

```bash
git add kalkulacka.py
git commit -m "Add multiply function"
```

4. Přidej ještě funkci `divide(a, b)` – ošetři dělení nulou (např. vyhoď `ValueError`). Znovu
   `git diff`, `git add`, `git commit -m "Add divide function with zero-division guard"`.

5. Zkus si v GitLens (v postranním panelu VS Code, záložka "Source Control" nebo "GitLens")
   prohlédnout historii commitů – uvidíš graf a detail každé změny (tzv. "blame" a "history").

### Cvičení 1.6 – Založení repozitáře na GitHubu a propojení

1. Na GitHubu vytvoř nový **prázdný** repozitář (bez README, bez `.gitignore` – ty už máš
   lokálně), např. `Git_withClaude`.
2. GitHub ti ukáže příkazy pro propojení existujícího lokálního repozitáře – typicky:

```bash
git remote add origin https://github.com/<tvuj-ucet>/Git_withClaude.git
git branch -M main
git push -u origin main
```

3. Obnov stránku repozitáře na GitHubu – měl bys vidět své 3 commity.

### Cvičení 1.7 (volitelné, AI) – Commit message s pomocí AI

Udělej libovolnou malou úpravu v `kalkulacka.py` (např. přidej docstring k funkci). Spusť:

```bash
git diff
```

Zkopíruj výstup do AI chatu (Claude/Copilot Chat) s promptem *"Navrhni stručnou commit message
v conventional commits stylu pro tuto změnu"* a použij navrženou zprávu pro `git commit -m "..."`.

---

## 3. Řešení / kontrolní body

- Po `git init` by `git status` měl hlásit "no commits yet" a "nothing to commit" dokud nic
  nepřidáš.
- Po vytvoření souborů by `git status` měl ukázat `kalkulacka.py`, `.gitignore`, `README.md`
  jako **Untracked files** (červeně v GitLens/VS Code).
- Po `git add` se stejné soubory objeví jako **Changes to be committed** (zeleně).
- `__pycache__/` by se v `git status` neměl objevit vůbec (je ignorovaný) – pokud se objeví,
  zkontroluj přesný obsah a název `.gitignore`.
- `git log --oneline` by měl na konci Dne 1 ukazovat min. 3 commity, např.:
  ```
  d4e5f6a Add divide function with zero-division guard
  b2c3d4e Add multiply function
  a1b2c3d Initial commit: add calculator script and gitignore
  ```
- Po `git push -u origin main` by GitHub měl zobrazovat identickou historii jako `git log`
  lokálně – to je dobrý způsob, jak si ověřit, že je vše synchronizované.

**Časté chyby a jak je poznat:**
- `fatal: not a git repository` → jsi ve špatné složce, nebo jsi zapomněl `git init`.
- `git push` vyžaduje přihlášení → Git for Windows spustí přihlašovací okno (Git Credential
  Manager); přihlas se GitHub účtem.
- Pokud omylem commitneš něco, co jsi commitovat nechtěl (např. `__pycache__` před přidáním
  `.gitignore`), řešení si ukážeme v Dni 3 (`git rm --cached`).
