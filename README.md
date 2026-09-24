# 3denní kurz Git & GitHub (s přesahem do AI), cvičný soubor pro kurz Git/GitHub

Kurz je navržený na **1–2 hodiny denně**, pro prostředí:
- VS Code + Git for Windows + GitLens
- Python
- GitHub účet (s existujícím repozitářem nebo nově založeným)
- Lokální složka: `C:\Projects\Git_withClaude`

## Cheat sheet
- Přidal jsem nový soubor - git_github_cheatsheet.PDF, ve kterém je spousta návodů, postupů, best practices s prací s Git/GitHub.

## Jak kurz použít

1. Rozbal tyto soubory do `C:\Projects\Git_withClaude\kurz\` (nebo kamkoliv se ti hodí) –
   samotný **cvičný repozitář** ale založíme přímo v `C:\Projects\Git_withClaude` v Dni 1, krok za krokem.
2. Každý den má vlastní soubor: `den1.md`, `den2.md`, `den3.md`.
3. Struktura každého dne:
   - **Teorie** – krátký výklad konceptů (čti, nemusíš nic psát)
   - **Praktická cvičení** – konkrétní úkoly, které děláš přímo v terminálu/VS Code
   - **Řešení** – očekávaný postup/příkazy, pro kontrolu až cvičení uděláš sám
4. Cvičný Python skript se bude v průběhu 3 dnů postupně vyvíjet a verzovat – najdeš ho
   jako `start_kalkulacka.py`, což je startovní bod pro Den 1.

## Přehled dnů

| Den | Téma | Výstup |
|---|---|---|
| 1 | Co je Git a GitHub, lokální repozitář, staging, commity, `.gitignore`, remote, push/pull, AI jako asistent u commit messages | Repozitář na GitHubu s historií commitů |
| 2 | Větve (branches), merge, konflikty, GitHub Pull Requesty, AI code review | `feature` větev sloučená do `main` přes PR |
| 3 | Rebase vs. merge, cherry-pick, stash, reset vs. revert, tagy/release, AI agenti a Git workflow | Tag `v1.0`, vyřešený "rozjetý" scénář s více větvemi |

## Poznámka k terminologii

- `master` vs `main`: GitHub dnes při založení repa nabízí výchozí název větve `main`.
  Popisuji oboje, ale ve cvičeních použijeme `main`, protože to dnes uvidíš i v novém repozitáři na GitHubu.
- Git příkazy píšu tak, jak je spustíš v terminálu VS Code (PowerShell nebo Git Bash – obojí funguje).

## Příprava na kurz
1. Nainstalovaný VS Code s extensions GitHub, GitLens, Python
2. Nainstalovaný Git
3. Nainstalovaný python
4. Vytvořený účet na GitHub