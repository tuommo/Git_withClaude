# Den 2 – Větve, merge, konflikty, Pull Requesty na GitHubu, AI code review

Časová dotace: cca 1–2 hodiny.

---

## 1. Teorie (cca 25–35 min)

### 1.1 Co je větev (branch)

Větev je jen **ukazatel na commit** (ne kopie souborů!). `main` je jedna větev mezi mnoha.
Vytvoření nové větve je proto rychlé a levné – Git jen vytvoří nový ukazatel na aktuální commit.

```
main:     A---B---C
                    \
feature:             D---E
```

### 1.2 Proč větvit

- Izolace rozpracované práce od stabilního `main`.
- Paralelní práce více lidí (nebo více úkolů) bez vzájemného rušení.
- Typický model: `main` = vždy funkční, `feature/xyz` = rozpracovaná funkce, po dokončení
  se sloučí (merge) zpět do `main`.

### 1.3 Merge – fast-forward vs. 3-way (true) merge

- **Fast-forward merge**: pokud `main` se od vytvoření větve vůbec nezměnil, Git jen posune
  ukazatel `main` na poslední commit větve. Žádný nový "merge commit" nevzniká.
- **3-way merge**: pokud se `main` mezitím taky změnil, Git vytvoří nový **merge commit**,
  který má **dva rodiče** – spojuje obě historie.

```
main:     A---B---------F (merge commit)
               \       /
feature:        C-----E
```

### 1.4 Konflikt (merge conflict)

Nastane, když stejná část stejného souboru byla změněna jinak na obou větvích. Git to nedokáže
rozhodnout sám a označí místo konfliktu přímo v souboru:

```
<<<<<<< HEAD
kód z aktuální větve
=======
kód z větve, kterou slučuješ
>>>>>>> feature/xyz
```

Řešení: ručně uprav soubor na finální podobu, smaž značky `<<<<<<<`, `=======`, `>>>>>>>`,
pak `git add <soubor>` a `git commit` (u merge Git zprávu často předvyplní).

### 1.5 Pull Request (PR) na GitHubu

PR není součástí samotného Gitu – je to funkce GitHubu (a podobných platforem). Typický tok:

1. Vytvoříš větev, uděláš commity, `git push` na GitHub.
2. Na GitHubu otevřeš Pull Request z `feature/xyz` do `main`.
3. Někdo (nebo ty sám na cvičení) provede **code review** – komentáře, návrhy.
4. Po schválení se PR **smerguje** (GitHub nabízí merge/squash/rebase merge).
5. Volitelně se větev na GitHubu smaže (lokální zůstává, dokud ji sám nesmažeš).

### 1.6 AI v code review

- AI (Copilot code review, nebo vložení diffu do Claude/ChatGPT) umí upozornit na chyby,
  navrhnout lepší pojmenování, najít edge-case (např. dělení nulou), zkontrolovat konzistenci
  s dokumentací.
- Nenahrazuje pochopení kódu recenzentem, ale výrazně zrychluje první průchod.

---

## 2. Praktická cvičení (cca 45–75 min)

### Cvičení 2.1 – Vytvoření feature větve

```bash
git checkout -b feature/power-function
```

(`checkout -b` = vytvoř větev a rovnou na ni přepni; novější ekvivalent je `git switch -c
feature/power-function`.)

Ověř, na které větvi jsi:

```bash
git branch
```

### Cvičení 2.2 – Práce na feature větvi

1. Přidej do `kalkulacka.py` funkci `power(base, exponent)`.
2. Commitni na této větvi:

```bash
git add kalkulacka.py
git commit -m "Add power function"
```

3. Přidej ještě jednoduché testy (nebo aspoň pár `print` ověření ve `__main__` bloku) a udělej
   druhý commit na téže větvi.

### Cvičení 2.3 – Fast-forward merge

Vrať se na `main` a slouč feature větev (main se mezitím nezměnil, takže očekávej fast-forward):

```bash
git checkout main
git merge feature/power-function
git log --oneline --graph
```

Všimni si, že nevznikl žádný speciální merge commit – `main` se jen posunul.

### Cvičení 2.4 – Vyvolání a vyřešení konfliktu

1. Na `main` uprav řádek s `print("Kalkulacka v0.1")` na `print("Kalkulacka v1.0")` a commitni.
2. Vytvoř novou větev ze **staršího** stavu, abys měl divergenci – nejjednodušší je:

```bash
git checkout -b feature/conflict-demo HEAD~1
```

3. Na této větvi uprav **stejný řádek** jinak, např. na `print("Moje kalkulacka")`, a commitni.
4. Přepni na `main` a zkus sloučit:

```bash
git checkout main
git merge feature/conflict-demo
```

Git nahlásí konflikt. Otevři `kalkulacka.py` ve VS Code – uvidíš značky konfliktu (VS Code je
navíc barevně zvýrazní a nabídne tlačítka "Accept Current/Incoming/Both").

5. Rozhodni se pro finální text řádku, uprav soubor, pak:

```bash
git add kalkulacka.py
git commit
```

(Git předvyplní zprávu typu "Merge branch 'feature/conflict-demo'" – můžeš ji nechat nebo
upravit.)

### Cvičení 2.5 – Push větve a Pull Request na GitHubu

1. Vytvoř další drobnou feature větev, např. `feature/readme-update`, uprav `README.md`
   (přidej sekci "Jak spustit"), commitni.

```bash
git checkout -b feature/readme-update
```

2. Pushni tuto větev na GitHub:

```bash
git push -u origin feature/readme-update
```

3. Na GitHubu otevři Pull Request z `feature/readme-update` do `main`.
4. V popisu PR napiš, co změna dělá. Zkus (i jen sám na sebe) přidat komentář k řádku v diffu.
5. Merguj PR tlačítkem na GitHubu (zkus možnost "Squash and merge" a přečti si, jak se liší od
   běžného merge – squash spojí všechny commity větve do jednoho).
6. Lokálně si stáhni změnu zpět:

```bash
git checkout main
git pull
```

7. Smaž lokální i vzdálenou větev, která už splnila účel:

```bash
git branch -d feature/readme-update
git push origin --delete feature/readme-update
```

### Cvičení 2.6 (volitelné, AI) – AI code review

Vezmi `git diff main feature/power-function` (než smažeš větev, nebo si ho ulož předem) a vlož
ho do AI chatu s promptem *"Zkontroluj tento diff jako code reviewer – najdi chyby, edge-case a
navrhni zlepšení pojmenování."* Porovnej návrhy s tím, co bys našel sám.

---

## 3. Řešení / kontrolní body

- `git branch` po Cvičení 2.1 by měl ukázat hvězdičku u `feature/power-function`.
- Po fast-forward merge (Cvičení 2.3) `git log --oneline --graph` ukáže **lineární** historii
  (žádné rozvětvení v grafu, žádný merge commit).
- Po vyřešení konfliktu (Cvičení 2.4) `git log --oneline --graph` ukáže naopak **rozvětvení a
  spojení** – merge commit se dvěma rodiči (na řádku uvidíš `|\` a `|/`).
- V souboru po vyřešení konfliktu **nesmí zůstat** žádné `<<<<<<<`, `=======`, `>>>>>>>` –
  pokud tam jsou, `git commit` sice projde, ale kód bude rozbitý; zkontroluj `git diff --check`
  před commitem, pokud si nejsi jistý.
- Na GitHubu by po smergovaném PR měl `main` obsahovat úpravu README a historie by se měla
  shodovat s lokální po `git pull`.
- `git branch -d` (malé d) odmítne smazat větev, která nebyla smergovaná – to je záměrná
  pojistka. Force smazání je `git branch -D` (velké D), ale používej ho vědomě.
