# Den 3 – Rebase, cherry-pick, stash, reset vs. revert, tagy, AI agenti a Git

Časová dotace: cca 1–2 hodiny.

---

## 1. Teorie (cca 30–40 min)

### 1.1 Rebase vs. merge

- **Merge** zachovává historii tak, jak se skutečně stala (včetně merge commitů) – "poctivé",
  ale historie může být "rozvětvenější".
- **Rebase** *přehraje* commity tvé větve na nový základ (typicky aktuální `main`) – vytvoří
  jejich kopie s novými hashi, jako by od začátku vycházely z novějšího `main`. Výsledkem je
  **lineární** historie.

- **Rebase** je na konci dokumentu detailně vysvětlena.
  
```
Před rebase:
main:     A---B---C
               \
feature:        D---E

Po "git rebase main" (na feature větvi):
main:     A---B---C
                    \
feature:             D'---E'
```

- **Zlaté pravidlo rebase**: nikdy nerebasuj větev, kterou už někdo jiný stáhl/používá
  (přepisuješ historii – cizí kopie by se rozešly s tvou). Na sdílené `main` větvi rebase
  neděláme; na svých vlastních lokálních feature větvích je to běžné a užitečné.

### 1.2 Cherry-pick

`git cherry-pick <hash>` zkopíruje **jeden konkrétní commit** z jiné větve na tu aktuální.
Hodí se, když chceš jen jednu konkrétní opravu, ne celou větev.

*Cherry-pick* — na feature/velky-refaktoring máš rozpracovanou velkou přestavbu (ještě nehotovou, nechceš ji mergovat). Cestou jsi ale objevil a opravil skutečnou chybu — třeba že divide() nehlásí chybu při dělení nulou, ale spadne. Tahle oprava je commitnutá jako samostatný commit uprostřed té větve. Chceš ji dostat na main hned, bez zbytku rozpracované práce:

```bash
git log feature/velky-refaktoring --oneline   # najdeš hash té opravy
git checkout main
git cherry-pick a1b2c3d
```
Oprava je na main, refaktoring zůstává izolovaný a nehotový na své větvi.


### 1.3 Stash

`git stash` dočasně "odloží" rozpracované změny (bez commitu) a vrátí working directory do
čistého stavu – užitečné, když potřebuješ rychle přepnout větev, ale ještě nechceš commitovat.

```bash
git stash            # ulož rozpracované změny
git stash list        # seznam odložených změn
git stash pop         # vrať poslední odloženou změnu zpět a smaž ji ze seznamu
```

*Stash* — jsi na main, rozpracoval jsi úpravu kalkulacka.py (přidáváš modulo()), ale ještě to nechceš commitovat, protože je to napůl hotové a nefunkční. V tu chvíli ti kolega (nebo šéf) napíše, že je na produkci bug a potřebuješ okamžitě přepnout na hotfix větev a opravit ho. Git ti checkout odmítne, dokud máš rozpracované změny, které by se s cílovou větví bily:

```bash
git stash push -m "rozpracovana modulo funkce"
git checkout hotfix
# ... oprava bugu, commit, push ...
git checkout main
git stash pop   # vrátíš se zpátky k modulo() přesně tam, kde jsi skončil
```

Společný vzorec: rebase = "chci čistší historii před sdílením", cherry-pick = "chci jen tenhle jeden kousek jinam", stash = "musím rychle pryč, ale nechci commitovat rozbitý kód".

### 1.4 Reset vs. revert

- **`git reset`** posune ukazatel větve na jiný commit. Existují 3 režimy:
  - `--soft` – posune HEAD, změny zůstanou ve staging area,
  - `--mixed` (výchozí) – posune HEAD, změny zůstanou jen v working directory (odstageované),
  - `--hard` – posune HEAD a **zahodí** všechny změny (nebezpečné, nevratné bez zálohy/reflogu).
  - Reset **přepisuje historii** – vhodné jen na commity, které jsi ještě nikam nepushnul.
- **`git revert <hash>`** vytvoří **nový commit**, který obsahuje opak změn daného commitu.
  Historie zůstává neporušená (nic se nemaže) – proto je `revert` bezpečný i na sdílených
  větvích, kde už jsou commity pushnuté.

### 1.5 Tagy a "release"

Tag je pojmenovaný odkaz na konkrétní commit, typicky pro označení verze:

```bash
git tag -a v1.0 -m "Verze 1.0 kalkulacky"
git push origin v1.0
```

Na GitHubu lze z tagu vytvořit formální "Release" se change-logem a přiloženými soubory.

### 1.6 AI agenti a Git workflow

Dnešní AI agenti (např. Claude Code, GitHub Copilot Agent/Workspace) dokážou nad repozitářem
autonomně:
- přečíst zadání/issue,
- vytvořit větev,
- napsat kód a testy, udělat commity s popisnými zprávami,
- pushnout větev a otevřít Pull Request s popisem změny,
- reagovat na komentáře recenzenta dalšími commity.

Rozdíl oproti "AI chatu": chat ti **radí**, co napsat do terminálu; agent **sám vykonává**
příkazy (add/commit/push/PR) v rámci nastavených oprávnění. Praktický dopad pro tebe:
- Stále je dobré umět přečíst `git log`/`git diff` a rozumět tomu, co agent udělal – code review
  nad AI-generovanou historií je stejně důležitý (možná důležitější) jako nad lidskou.
- Menší, atomické commity s jasnou zprávou usnadňují i AI agentovi (i tobě) pozdější orientaci,
  případný `revert` nebo `cherry-pick` jen té části, která je potřeba.

---

### 2. Praktická cvičení (cca 45–75 min)

> Předpoklad: jsi na `main`, `main` je pushnutý na GitHub a `git status` hlásí "nothing to
> commit, working tree clean" (pokud ne, nejdřív si to ukliď – dokonči/zahoď rozdělané změny
> z předchozích cvičení).

### Cvičení 3.1 – Rebase na vlastní větvi

**Krok 1 – drobná změna přímo na `main`.**
Otevři `README.md` a přidej na konec libovolný řádek, např.:

```markdown
## Poznámky
Kurz probíhá průběžně, den 3.
```

Ulož soubor a commitni rovnou na `main`:

```bash
git add README.md
git commit -m "Add notes section to README"
```

**Krok 2 – založ feature větev a uprav výstup kalkulačky.**

```bash
git checkout -b feature/format-output
```

Otevři `kalkulacka.py` a najdi řádky s `print`, např.:

```python
print("2 + 3 =", add(2, 3))
```

Přepiš je na f-string zápis:

```python
print(f"2 + 3 = {add(2, 3)}")
```

Uprav tímto způsobem všechny `print` řádky v bloku `if __name__ == "__main__":`. Ulož soubor
a commitni **na této větvi**:

```bash
git add kalkulacka.py
git commit -m "Use f-strings for calculator output"
```

**Krok 3 – vrať se na `main` a posuň ho dál.**

```bash
git checkout main
```

Udělej na `main` ještě jednu **nezávislou** změnu – něco, co se netýká stejných řádků jako
v kroku 2, aby nevznikl zbytečný konflikt. Např. v `kalkulacka.py` doplň na začátek souboru
druhý řádek komentáře:

```python
"""
Jednoducha kalkulacka - vychozi bod pro kurz Git & GitHub.
Verze pro Den 3 - rozsirovano o dalsi operace.
"""
```

```bash
git add kalkulacka.py
git commit -m "Update module docstring"
```

Teď je `main` o jeden commit dál, než byl v okamžiku, kdy z něj vznikla `feature/format-output`.

**Krok 4 – rebase feature větve na aktuální `main`.**

```bash
git checkout feature/format-output
git rebase main
```

Očekávaný výstup v terminálu (přibližně):
```
Successfully rebased and updated refs/heads/feature/format-output.
```

**Krok 5 – ověření.**

```bash
git log --oneline --graph --all
```

Měl bys vidět **lineární** řadu commitů (žádné rozvětvení `\` a `/`) – commit "Use f-strings for
calculator output" bude uveden **až za** "Update module docstring", i když jsi ho psal dřív.
Pokud si zapamatuješ hash commitu "Use f-strings..." před rebase (`git log --oneline` před
krokem 4) a porovnáš ho s hashem po rebase, uvidíš, že se **liší** – Git commit fyzicky vytvořil
znovu.

> **Pokud při `git rebase main` nastane konflikt** (např. jsi upravoval stejný řádek v obou
> krocích): Git rebase zastaví a napíše něco jako `CONFLICT (content): Merge conflict in
> kalkulacka.py`. Postup je stejný jako u merge konfliktu z Dne 2 – otevři soubor, najdi značky
> `<<<<<<<` / `=======` / `>>>>>>>`, uprav na finální podobu, smaž značky, ulož. Pak ale
> **místo `git commit`** napiš:
> ```bash
> git add kalkulacka.py
> git rebase --continue
> ```
> Kdyby ses chtěl z rebase úplně vrátit zpět do stavu před jeho spuštěním, použij
> `git rebase --abort`.

### Cvičení 3.2 – Cherry-pick

**Krok 1 – dva samostatné commity na jedné větvi.**

Zůstaň na `feature/format-output` (z předchozího cvičení). Najdi v `kalkulacka.py` komentář
s překlepem (nebo si nějaký úmyslně vytvoř), např. změň:

```python
# Jednoducha kalkulacka - vychozi bod pro kurz Git & GitHub.
```

na opravenou verzi (např. doplň diakritiku nebo oprav slovo). Ulož a commitni **samostatně**:

```bash
git add kalkulacka.py
git commit -m "Fix typo in module comment"
```

Teď přidej ještě drobnou novou funkci, např. `square(a)` (druhá mocnina), a commitni to jako
**druhý, oddělený** commit:

```bash
git add kalkulacka.py
git commit -m "Add square function"
```

**Krok 2 – najdi hash commitu s opravou překlepu.**

```bash
git log --oneline
```

Zkopíruj si hash řádku `Fix typo in module comment` (např. `f7e8a21`).

**Krok 3 – přepni na `main` a zkopíruj jen tenhle jeden commit.**

```bash
git checkout main
git cherry-pick f7e8a21
```

(nahraď `f7e8a21` skutečným hashem z tvého `git log`)

**Krok 4 – ověření.**

```bash
git log --oneline
```

Na `main` by měl přibýt **jen jeden** nový commit – `Fix typo in module comment`. Commit
`Add square function` na `main` **není** – zůstal jen na `feature/format-output`. Hash
zkopírovaného commitu na `main` bude jiný než na feature větvi (cherry-pick taky vytváří nový
commit objekt, stejně jako rebase).

### Cvičení 3.3 – Stash

**Krok 1 – rozpracuj (a nedokonči) změnu na `main`.**

Otevři `kalkulacka.py` a **rozepiš** novou funkci, ale nedokonči ji ani neulož do funkčního
stavu, např.:

```python
def modulo(a, b):
    # TODO: dodelat osetreni deleni nulou
    return a % b
    print("docasny ladici radek, smazat")
```

Ulož soubor, ale **necommituj** ho.

**Krok 2 – zkus přepnout větev.**

```bash
git checkout feature/power-function
```

Pokud se `power-function` liší na stejném místě souboru, Git checkout odmítne s hláškou
podobnou:
```
error: Your local changes to the following files would be overwritten by checkout: ...
Please commit your changes or stash them before you switch branches.
```

(Pokud náhodou checkout projde bez chyby, není to problém – jen to znamená, že se změny
nepřekrývají; pro účel cvičení je důležité vidět princip stash, i kdyby k chybě nedošlo.)

**Krok 3 – odlož rozpracované změny.**

```bash
git stash push -m "rozpracovana modulo funkce"
```

Ověř, že working directory je čistý:
```bash
git status
```
Mělo by hlásit "nothing to commit, working tree clean". Soubor `kalkulacka.py` je zpátky
v posledním commitnutém stavu.

**Krok 4 – přepni na jinou větev a zase zpátky.**

```bash
git checkout feature/power-function
git log --oneline -3
git checkout main
```

**Krok 5 – vrať si rozpracovanou práci.**

```bash
git stash list
git stash pop
```

`git stash list` ti ukáže odloženou změnu se jménem, které jsi jí dal. `git stash pop` ji vrátí
zpět do working directory **a zároveň ji smaže** ze seznamu stashů. Otevři `kalkulacka.py` –
rozpracovaná `modulo()` funkce by tam měla být přesně tak, jak jsi ji nechal.

> Rozdíl `pop` vs. `apply`: `git stash apply` vrátí změny, ale **nechá** je i v seznamu stashů
> (pro jistotu, kdybys je chtěl použít ještě jednou jinde). `pop` = apply + rovnou smazání ze
> seznamu.

### Cvičení 3.4 – Reset (mixed) vs. revert

**Část A – reset na nepushnutém commitu.**

**Krok 1.** Dokonči a oprav `modulo()` z předchozího cvičení, ale schválně do ní vlož
syntaktickou chybu, např. zapomeň dvojtečku:

```python
def modulo(a, b)
    return a % b
```

Ulož a commitni to i s chybou:

```bash
git add kalkulacka.py
git commit -m "Add modulo function"
```

**Krok 2.** Zkontroluj, že tenhle commit ještě **nikam nepushnul** (`git log --oneline` a
porovnání s `git log origin/main --oneline` – commit s modulo by v origin/main neměl být).

**Krok 3.** Vrať se o commit zpět, ale nech si změny po ruce k opravě:

```bash
git reset --mixed HEAD~1
```

**Krok 4.** Ověř:
```bash
git status
git log --oneline
```
`git log` by neměl obsahovat commit "Add modulo function" (zmizel z historie). `git status`
by měl `kalkulacka.py` ukázat jako změněný, ale **needstagovaný** ("Changes not staged for
commit") – syntaktická chyba v souboru pořád je, jen bez commitu.

**Krok 5.** Oprav chybu (doplň dvojtečku), ulož a commitni pořádně:
```bash
git add kalkulacka.py
git commit -m "Add modulo function"
```

**Část B – revert na "už pushnutém" commitu.**

**Krok 1.** Vytvoř další "chybný" commit – např. v `divide()` schválně smaž ošetření dělení
nulou (`ValueError`), takže funkce začne při dělení nulou padat. Commitni a rovnou pushni:

```bash
git add kalkulacka.py
git commit -m "Remove zero-division guard (oops)"
git push
```

**Krok 2.** Najdi hash tohoto commitu:
```bash
git log --oneline
```

**Krok 3.** Vrať jeho účinek přes revert (ne reset – commit je už na GitHubu):
```bash
git revert <hash-chybneho-commitu>
```
Git otevře editor s předvyplněnou zprávou `Revert "Remove zero-division guard (oops)"` – ulož
a zavři editor (u výchozího nastavení ve VS Code stačí uložit soubor a zavřít záložku).

**Krok 4.** Ověř:
```bash
git log --oneline
```
V historii uvidíš **oba** commity – ten chybný i ten revertující. Otevři `kalkulacka.py` a
zkontroluj, že ošetření dělení nulou je zpátky. Pushni i tenhle commit:
```bash
git push
```

!!!
Praktické poučení do budoucna: než spustíš reset, revert, rebase, nebo merge, je dobrý zvyk spustit git status a ujistit se, že working directory je čistý ("nothing to commit") — ušetří ti to přesně tenhle typ zmatku.
!!!

### Cvičení 3.5 – Tag a release

**Krok 1 – zkontroluj stav `main`.**
```bash
git checkout main
git log --oneline
```
`kalkulacka.py` by měl v tuhle chvíli obsahovat aspoň `add`, `subtract`, `multiply`, `divide`
(pokud `power` a `modulo` zůstaly jen na feature větvích, to je v pořádku – tag děláme na to,
co skutečně je na `main`).

**Krok 2 – vytvoř anotovaný tag.**
```bash
git tag -a v1.0 -m "Prvni stabilni verze kalkulacky"
```

**Krok 3 – ověř tag lokálně.**
```bash
git tag
git show v1.0
```
`git show v1.0` ti ukáže zprávu tagu i commit, na který ukazuje.

**Krok 4 – pushni tag na GitHub.**
```bash
git push origin v1.0
```
(Pozor: `git push` bez dalších parametrů tagy nepushuje automaticky – proto je potřeba tag
jmenovitě uvést.)

**Krok 5 – vytvoř Release na GitHubu.**
Na stránce repozitáře na GitHubu jdi do sekce **Releases → Draft a new release**, vyber tag
`v1.0`, doplň název (např. "v1.0 – první stabilní verze") a krátký popis, co release obsahuje
(sečti si to z `git log --oneline`), a publikuj.

### Cvičení 3.6 (volitelné, AI agent) – Vyzkoušení agentického workflow

Pokud máš k dispozici Claude Code (nebo podobný nástroj s přístupem k tomuto repozitáři):
1. Zadej agentovi úkol formou "issue", např.: *"Přidej do kalkulacka.py funkci na výpočet
   faktoriálu, včetně ošetření záporného čísla, vytvoř k tomu novou větev a commit."*
2. Nech agenta vytvořit větev a commit(y).
3. Sám zkontroluj `git log`, `git diff main <nova-vetev>` – over si, že rozumíš každé změně,
   než bys ji (hypoteticky) smergoval.

Pokud agenta k dispozici nemáš, stejné cvičení zvládneš i s AI chatem: necháš si vygenerovat
kód a commit message, ale příkazy (`add`/`commit`/`branch`) spustíš sám – rozdíl je jen v tom,
kdo "drží ruce na klávesnici" u samotných Git příkazů.

---

## 3. Řešení / kontrolní body

- Po `git rebase main` (Cvičení 3.1) `git log --oneline --graph --all` ukáže lineární historii;
  hash commitu z feature větve se **liší** od hashe před rebase (protože Git commit fyzicky
  vytvořil znovu, jen se stejným obsahem).
- Po `git cherry-pick` (Cvičení 3.2) by se na `main` měl objevit jen jeden nový commit se
  stejnou zprávou jako na feature větvi, ale s **jiným hashem** (cherry-pick taky vytváří nový
  commit objekt).
- `git stash pop` (Cvičení 3.3) vrátí přesně ten stav working directory, který jsi odložil;
  pokud mezitím došlo ke kolizi se změnami na cílové větvi, Git nahlásí konflikt stejně jako
  u merge.
- Po `git reset --mixed HEAD~1` (Cvičení 3.4) `git log` **neobsahuje** resetovaný commit, ale
  soubor se změnou v něm pořád existuje na disku (nezreseskuje se working directory obsah,
  jen historie a staging).
- Po `git revert` `git log --oneline` obsahuje **oba** commity – původní chybný i revert –
  historie je transparentní a nic se neztratilo.
- `git tag` bez `-a` vytvoří "lightweight" tag (jen ukazatel); s `-a` vytvoří "annotated" tag
  (s vlastním objektem, autorem, datem a zprávou) – pro release verze se doporučuje anotovaný.
- Obecná kontrola na konci dne: `git log --oneline --graph --all --decorate` by měl ukázat
  přehlednou historii se všemi větvemi, tagem `v1.0` a bez nevyřešených konfliktů.

## Co dál po kurzu

- Vyzkoušej `git bisect` pro hledání commitu, který zavedl chybu.
- Nastav si v GitHubu "Branch protection rules" pro `main` (vyžaduje PR i review, i když
  pracuješ sám – dobrý návyk).
- Zkus si `git rebase -i` (interaktivní rebase) pro "úklid" historie před otevřením PR
  (squashování drobných "wip" commitů do jednoho smysluplného).



## Rebase - detailní vysvětlení s příkladem
- Výchozí stav
Řekněme, že historie main vypadá takto (zjednodušeně, jen commity co se týkají kalkulacka.py):

main:  A (Initial commit) --- B (Add multiply function)

Ty si z bodu B uděláš svou větev:

```bash
git checkout -b feature/power-function
```

Na ní přidáš `power()`:
main:               A --- B
                            \
feature/power-function:      C (Add power function)

Zatím jsi ještě nic nepushnul, jen máš lokálně tenhle rozdíl.
Mezitím se main posune dál
Za dva dny se ale na GitHubu main změnil — třeba jsi sám (nebo někdo jiný) přidal divide() přímo do main a pushnul to:

main:               A --- B --- D (Add divide function)
                            \
feature/power-function:      C (Add power function)

Tvoje větev pořád vychází z B, ale main je teď o kus dál (D). Tomu se říká, že historie se rozešla (diverged).

Co znamená **přeložit (rebase)**

Spustíš:

```bash
git fetch origin
git rebase origin/main
```

Git teď udělá tohle: vezme tvůj commit C (Add power function), dočasně ho odloží stranou, přesune ukazatel tvé větve na D (aktuální konec main), a pak commit C znovu aplikuje — tedy vezme stejnou změnu (přidání power()) a commitne ji nanovo, ale teď už navazuje na D, ne na B:

main:                     A --- B --- D
                                        \
feature/power-function:                 C' (Add power function)

Všimni si: je to C' (s čárkou), ne C — je to nový commit objekt s novým hashem, i když obsah změny (přidání power()) je stejný. Starý C přestal existovat.

**Analogie**
Představ si, že píšeš kapitolu do knihy (tvůj commit C = "přidat kapitolu o `power()`"). Zatímco ji píšeš, autor hlavní knihy (main) mezitím vydá novou verzi, kde přibyla jiná kapitola před tou tvojí (D = "přidat `divide()`").

*Merge* by znamenalo: "vlepím svou kapitolu do staré verze knihy a pak řeknu — tyhle dvě verze teď spoj do jedné, včetně poznámky, že jsem spojoval". Vznikne extra "spojovací" stránka (merge commit).

*Rebase* znamená: "vezmu svou kapitolu, podívám se, jak přesně teď vypadá nová verze knihy, a napíšu svou kapitolu znovu, na základě té nové verze" — jako bys od začátku psal na aktuální podklad. Výsledek vypadá, jako bys svou kapitolu psal až po té nové kapitole o divide(), ne souběžně s ní.

**Proč je to důležité pro `power()` konkrétně**
Bez rebase by v kalkulacka.py mohl (v jiném scénáři) nastat konflikt, kdyby oba commity upravovaly stejné místo (např. obě přidávaly funkci na konec souboru za if __name__ == "__main__":). Rebase tě donutí ten konflikt vyřešit hned na tvé straně, než otevřeš PR — takže PR pak reviewer vidí jako hladkou, lineární historii: nejdřív `divide()`, pak rovnou `power()`, bez zbytečné "spojovací" zprávy typu Merge branch 'main' into feature/power-function.
