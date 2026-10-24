# Specifikacija projekta — Data Governance Signal

> Naziv: **Data Governance Signal** (datagovernancesignal.com)
> Podnaslov: *What matters in data governance, and why.*
> Status: v0.2 — naziv odabran, katalog izvora v0.1 izrađen
> Jezik portala: engleski · Jezik projektne dokumentacije: hrvatski

---

## 1. Dogovorene odluke

| # | Tema | Odluka |
|---|------|--------|
| 1 | Niša | Uži fokus na **Data Governance**, uz zasebnu širu rubriku **Data & AI** |
| 2 | Cilj | **Portal kojem se vjeruje** u području Data Governancea; dugoročno **prihod** |
| 3 | Redoslijed | **Portal je glavni proizvod.** Prijava na newsletter postoji od prvog dana, a slanje počinje kad se skupi publika |
| 4 | Tehnologija | **Kod** (statična stranica + automatizacija na GitHubu) |
| 5 | Uredničko vrijeme | Nije ograničenje: svaka vijest prolazi ručno odobrenje |
| 6 | Proračun | Do ~30 € mjesečno u prvoj fazi |
| 7 | AI | Ništa se ne objavljuje bez odobrenja urednika; uloga AI-ja je javno navedena |
| 8 | Naziv i domena | **Data Governance Signal**, `datagovernancesignal.com` (kratko: DG Signal) |

---

## 2. Vizija

Međunarodni stručni portal na engleskom koji prati područje Data Governancea, izdvaja ono što je stvarno važno i objašnjava **zašto je važno i na koga utječe**.

Ne natječemo se brojem objava. Natječemo se:
- **pouzdanošću**: svaka vijest ima izvor, a sažetak je provjeren,
- **uštedom vremena**: urednički odabir umjesto poplave vijesti,
- **kontekstom**: poslovni utjecaj, pogođeno područje governancea, povezane vijesti.

## 3. Publika

**Primarna publika (uži fokus):**
- voditelji Data Governancea i Data Management uredi
- Chief Data Officeri (CDO) i Chief Data & Analytics Officeri
- data stewardi i data owneri
- stručnjaci za privatnost, usklađenost i rizike (DPO, compliance, risk)
- konzultanti za podatke i upravljanje podacima

**Sekundarna publika (širi dio):**
- data arhitekti, data inženjeri, analitičari i AI/ML timovi koje zanima governance kontekst

## 4. Struktura sadržaja

### 4.1 Uži fokus — Data Governance (glavne kategorije)

| Kategorija (EN) | Što pokriva |
|-----------------|-------------|
| Governance Strategy & Operating Models | okviri (DAMA-DMBOK, DCAM…), organizacija, uloge, zrelost |
| Data Quality | alati, metodologije, mjerenje kvalitete, incidenti |
| Metadata, Catalogs & Lineage | data katalozi, poslovni rječnici, lineage, data marketplace |
| Privacy & Data Protection | GDPR, prava ispitanika, anonimizacija, privacy engineering |
| Regulation & Compliance | EU AI Act, Data Act, Data Governance Act, DORA, NIS2, sektorski propisi |
| AI Governance | upravljanje AI modelima, odgovorni AI, AI rizici, standardi (ISO/IEC 42001) |
| Master & Reference Data | MDM, referentni podaci, data products |
| Security & Access | upravljanje pristupom, klasifikacija podataka, DSPM |
| Vendors & Market | lansiranja proizvoda, akvizicije, investicije, analitička izvješća |

### 4.2 Šira rubrika — Data & AI
- Data Platforms & Architecture (lakehouse, data mesh, data fabric)
- Analytics & BI
- AI Industry (samo vijesti s utjecajem na podatke i governance)

Šira rubrika ima **viši prag relevantnosti** kako ne bi zagušila glavni fokus.

### 4.3 Vrste sadržaja (oznake)
`Regulation` · `Product launch` · `Acquisition / Funding` · `Research / Report` · `Standard / Framework` · `Case study` · `Incident / Fine` · `Event`

### 4.4 Format vijesti

Svaka objavljena vijest ima:

1. **Naslov**: vlastiti, informativan, bez clickbaita
2. **Sažetak**: 80–150 riječi, vlastitim riječima
3. **Why it matters**: 2–4 rečenice o poslovnom značenju
4. **Governance area affected**: jedna ili više kategorija iz 4.1
5. **Who should care**: uloge na koje vijest utječe (npr. CDO, DPO, steward)
6. **Importance**: 1–5 (urednička ocjena, AI predlaže)
7. **Sources**: svi izvori s poveznicama i originalnim datumom
8. **Related**: povezane ranije vijesti

Točke 3–5 su naša razlika u odnosu na generičke agregatore.

## 5. Načela povjerenja (urednička politika)

Budući da je glavni cilj **portal kojem se vjeruje**, ova pravila vrijede od prvog dana i bit će javno objavljena na stranici *Editorial Policy*:

1. **Izvor uz svaku vijest**: uvijek poveznica na original; primarni izvori imaju prednost pred prepričavanjem.
2. **Ljudsko odobrenje**: AI priprema nacrte, a urednik odobrava, uređuje ili odbacuje svaku objavu.
3. **Transparentnost o AI-ju**: jasno navedeno kako se AI koristi u pripremi sadržaja.
4. **Bez kopiranja**: samo vlastiti sažeci, bez preuzimanja cijelih tekstova i tuđih slika.
5. **Ispravci**: javna politika ispravaka; ispravljeni članci imaju vidljivu napomenu.
6. **Odvojenost komercijalnog sadržaja**: sponzorirani sadržaj uvijek je jasno označen i nikad ne utječe na uredničku ocjenu važnosti ni na redoslijed vijesti.
7. **Neovisnost o dobavljačima**: vijesti o dobavljačima ocjenjuju se po stvarnom utjecaju, a ne po njihovom marketingu.

## 6. Model prihoda (faze)

Prihod dolazi **nakon** što portal ima publiku i ugled. Prerana komercijalizacija ugrožava povjerenje.

| Faza | Uvjet | Izvor prihoda |
|------|-------|---------------|
| 0 | lansiranje | nema; gradi se sadržaj, SEO i lista pretplatnika |
| 1 | stalna publika i aktivan newsletter | sponzorirani slot u newsletteru (jasno označen) |
| 2 | prepoznatljivost u niši | imenik dobavljača / alata (označene plaćene pozicije), oglasi za poslove |
| 3 | ugled i arhiva podataka | premium izvješća, tržišne analize, plaćeni pregledi trendova |

Cilj prve godine je publika i povjerenje, ne prihod.

## 7. Newsletter

- **Obrazac za prijavu na portalu od prvog dana** (početna stranica, dno svakog članka).
- Tjedni pregled (*Weekly Briefing*) počinje se slati kad lista dosegne smislenu veličinu (okvirno 50–100 pretplatnika). Do tada se isti pregled objavljuje na portalu kao članak.
- Alat: neki od servisa s besplatnim početnim paketom (npr. Buttondown, Beehiiv); odluka u fazi 2.

## 8. Tehnička arhitektura (MVP)

```mermaid
flowchart LR
    A["GitHub Actions<br/>raspored 2-3x dnevno"] --> B["Dohvat izvora<br/>RSS / API / scraping"]
    B --> C["Uklanjanje duplikata<br/>URL + sličnost sadržaja"]
    C --> D["AI ocjena relevantnosti<br/>jeftini model"]
    D -->|ispod praga| E["Zapis u arhivu odbijenih"]
    D -->|iznad praga| F["AI sažetak i analiza<br/>jači model"]
    F --> G["Nacrt kao Pull Request"]
    G --> H{"Urednik"}
    H -->|uredi / odobri = merge| I["Automatski build<br/>i objava stranice"]
    H -->|odbaci = close| E
```

| Sloj | Izbor | Napomena |
|------|-------|----------|
| Web | **Astro** (statična stranica) | brzo, jeftino, odlično za SEO |
| Sadržaj | Markdown datoteke u repozitoriju | svaka vijest = jedna datoteka, puna povijest izmjena |
| Pretraživanje | **Pagefind** | statično pretraživanje, bez servera |
| Hosting | Cloudflare Pages ili Netlify | besplatni paket, HTTPS uključen |
| Automatizacija | **GitHub Actions** (cron) | dohvat, AI obrada, otvaranje nacrta |
| Stanje obrade | JSON/SQLite u repozitoriju | već viđene vijesti, log grešaka, potrošnja AI-ja; baza se uvodi tek ako zatreba |
| AI | API velikog jezičnog modela | dva modela: jeftini za ocjenu, jači za sažetke; dobavljač se bira u fazi 4 |
| Uredničko odobrenje | **Pull Request na GitHubu** | pregled, izmjena i odobrenje i s mobitela (GitHub aplikacija) |
| Analitika | Cloudflare Web Analytics ili Plausible | bez kolačića, u skladu s GDPR-om |

**Zašto PR kao urednički alat:** nema dodatnog admin sučelja ni troška, svaka izmjena je zabilježena, a odobrenje je jedan klik. Ako se pokaže nepraktičnim, kasnije se može dodati jednostavno urednično sučelje.

**Dogovoreni urednički tijek (odluka 24. 10. 2026.):**
- jedan Pull Request po vijesti, naslov `Draft: <naslov> — Importance N`
- obavijest u GitHub aplikaciji na mobitelu (urednik ju je instalirao)
- **Merge** = objava · **Close** = odbacivanje · uređivanje datoteke u PR-u = ispravak prije objave
- u opisu PR-a: sažetak, Why it matters, Who should care, kategorije, prijedlog kartice, izvori i AI obrazloženje ocjene
- ako se nakon 1–2 tjedna pokaže nespretnim → vlastita urednička stranica (`/editor`, zaštićena prijavom)

**Kontrola troškova:** dnevni i mjesečni limit potrošnje AI-ja u kodu; obrada staje i javlja grešku kad se limit dosegne.

## 9. Katalog izvora

**v0.2:** 53 izvora — 39 RSS, 7 čitanje stranice, 6 ručno, 1 neaktivan. Prikupljanje radi automatski 3× dnevno (`pipeline/ingest.py`, izvještaj u `data/reports/latest.md`). Pregled je u [katalog-izvora.md](katalog-izvora.md), a podaci u [`data/sources.yaml`](../data/sources.yaml).

Cilj: **30–50 izvora** u prvoj verziji. Za svaki izvor bilježimo:

| Polje | Primjer |
|-------|---------|
| Naziv | — |
| URL | — |
| Vrsta | regulator / dobavljač / analitičar / udruga / medij / blog / istraživanje |
| Kategorije | iz 4.1 / 4.2 |
| Način dohvata | RSS / API / scraping / ručno |
| Pouzdanost | 1–3 (primarni izvor = 3) |
| Prioritet | visok / srednji / nizak |
| Napomena | npr. uvjeti korištenja, učestalost objava |

Okvirne skupine izvora:
- **Regulatori i institucije:** Europska komisija, EDPB, nacionalna tijela za zaštitu podataka, ENISA, NIST, ISO
- **Stručne udruge:** DAMA International, EDM Council, IAPP
- **Analitičke kuće:** javno dostupni sažeci i priopćenja
- **Dobavljači:** vodeći alati za governance, katalog, kvalitetu i privatnost (blogovi i priopćenja)
- **Stručni mediji i blogovi:** specijalizirani portali i autori iz područja

## 10. Revidirane faze

| Faza | Sadržaj | Rezultat |
|------|---------|----------|
| 1 ✅ | Specifikacija + katalog izvora | ovaj dokument + `data/sources.yaml` |
| 2 ✅ | Kostur portala: početna, kategorije, članak, pretraživanje, Editorial Policy, prijava na newsletter | portal s probnim vijestima (lokalno / testna adresa) |
| 3 ✅ | Dohvat izvora, duplikati, log grešaka | automatski dotok vijesti u arhivu |
| 4 | AI ocjena, sažetak, „why it matters", nacrti kao PR | AI priprema nacrte za odobrenje |
| 5 | Interni pilot 2 tjedna: točnost, duplikati, troškovi, ispadi izvora | pouzdan proces |
| 6 | Naziv, domena, HTTPS, SEO, analitika, početni sadržaj | javno lansiranje |

## 10a. Plan faze 4 (dogovoreno, čeka 3–5 dana podataka iz prikupljanja)

1. ✅ **Dobavljač AI modela** — Anthropic Claude (Haiku 5.5 za trijažu, Opus 5.5 za nacrte); API ključ u GitHub secretu, mjesečni limit 12 $ u kodu. Procjena ~8–10 $/mj.; prvo pokretanje 24. 10.: 5 stavki, 1 nacrt, 0,04 $.
2. ✅ **AI obrada** (`pipeline/draft.py`) — ocjena relevantnosti (jeftini model), nacrt članka u dogovorenom formatu (jači model): sažetak, Why it matters, Who should care, kategorije, važnost, prijedlog kartice; povezivanje iste vijesti iz više izvora.
3. ✅ **Nacrti kao Pull Requestovi** — jedan PR po vijesti, urednik je zatražen kao recenzent i dodijeljen (obavijest u GitHub aplikaciji).
4. **Newsletteri kao izvori** — adresa `sources@datagovernancesignal.com`; Cloudflare Email Worker sprema izdanja, automatizacija vadi poveznice. Članci se pišu iz izvornog članka, uz navod „via …” za newsletter. Prvi: newsletter Nenada Bakića (Substack) — `sources@` pretplaćen 24. 10. 2026., izdanja nedjeljom ujutro. Poveznice u e-mailu idu preko Substack/Mailgun preusmjeravanja (`email.mg-d0.substack.com/c/…`) — pipeline ih mora razriješiti do izvornog članka i preskočiti odjavu i interne Substack poveznice.
5. **Substack izvori** (EU AI Act Newsletter, Modern Data 101) blokiraju GitHub — dohvat preko Cloudflare posrednika.
6. **AI ilustracije** za vijesti važnosti 4–5 (opcija C), uz odobrenje urednika.
7. **Stranica Privacy** (Cloudflare Web Analytics bez kolačića, newsletter) — prije lansiranja.

## 11. Kriteriji uspjeha

**Operativni (od lansiranja):**
- svaka vijest ima izvor i poveznicu
- nula duplikata u objavljenim vijestima
- evidencija neuspjelih obrada i potrošnje AI-ja
- AI troškovi unutar zadanog limita

**Publika i povjerenje (prvih 3–6 mjeseci):**
- broj pretplatnika na newsletter
- udio povratnih posjetitelja
- organski promet za ključne pojmove iz niše
- citiranja i dijeljenja (LinkedIn, poveznice s drugih stranica)

## 12. Otvorena pitanja

- [x] Naziv portala: Data Governance Signal
- [x] Kupljena domena datagovernancesignal.com (Namecheap, 2026-10-24)
- [x] DNS prebačen na Cloudflare (aktivno 2026-10-24)
- [x] E-mail editor@datagovernancesignal.com (Cloudflare Email Routing, prosljeđivanje na Gmail)
- [ ] Provjera žiga (EUIPO/USPTO)
- [ ] Dobavljač AI modela (faza 4)
- [ ] Newsletter servis (prije lansiranja)
- [x] Statistika posjeta: Cloudflare Web Analytics (bez kolačića)
- [x] Hosting: Cloudflare Pages (statična stranica, Astro)
- [ ] Dopuna kataloga izvorima koje već pratiš (vidi „Što nedostaje” u katalogu)
