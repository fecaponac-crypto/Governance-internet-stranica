# Katalog izvora — Data Governance Signal

> Verzija 0.2 · provjereno 24. 10. 2026. (prvo automatsko prikupljanje)
> Strojno čitljiv katalog (koristi ga automatizacija): [`data/sources.yaml`](../data/sources.yaml)

## Sažetak

| | Broj |
|---|---|
| Izvora ukupno | **53** (45 uži fokus, 8 šira rubrika) |
| Automatski putem RSS-a (provjereno da radi) | **39** izvora / 40 feedova |
| Scraping (nema RSS-a, čita se popis članaka) | **7** |
| Ručno praćenje (blokiraju pristup ili JavaScript) | **6** |
| Neaktivno (TDAN se spojio s DATAVERSITY-jem) | **1** |
| Prioritet visok / srednji / nizak | 10 / 26 / 17 |

Svaki RSS feed provjeren je stvarnim dohvatom: radi li, ima li objava i jesu li objave svježe.

## Kako čitati ocjene

- **Pouzdanost 3**: primarni ili službeni izvor (regulator, tijelo za standarde, stručna udruga, vodeći odvjetnički blogovi o privatnosti).
- **Pouzdanost 2**: stručni sekundarni izvor ili dobavljač. Dobavljači pišu u vlastitom interesu, pa su vijest samo njihova lansiranja, akvizicije i istraživanja, a ne marketinški članci.
- **Pouzdanost 1**: opći mediji.
- **Filter**: feed pokriva mnogo tema (npr. sva priopćenja Europske komisije). Prije AI ocjene zadržavaju se samo objave s ključnim pojmovima iz kataloga, čime se štedi na troškovima AI-ja.

## Izvori visokog prioriteta (10)

| Izvor | Vrsta | Način | Zašto |
|-------|-------|-------|-------|
| EDPB | regulator | RSS | smjernice i kazne nacionalnih tijela za GDPR |
| Europska komisija — Press Corner | regulator | RSS + filter | AI Act, Data Act, strategije EU |
| EK — Digital Strategy / AI Office | regulator | ručno | blokira automatski pristup; djelomično pokriveno preko EU AI Act Newslettera |
| UK ICO | regulator | scraping | najaktivniji regulator izvan EU |
| Irski DPC | regulator | scraping | glavni nadzornik za Big Tech u EU |
| IAPP | udruga | scraping | najvažniji izvor za privatnost i AI governance |
| EU AI Act Newsletter | stručni newsletter | RSS | kurirani pregled AI Acta s primarnim izvorima |
| Hunton Privacy Blog | odvjetnički blog | RSS | brze i točne vijesti o propisima |
| Inside Privacy (Covington) | odvjetnički blog | RSS | analize EU i US regulative |
| Gartner Newsroom | analitičar | ručno | predviđanja i istraživanja tržišta |

## Skupine izvora

**Regulatori i institucije (11):** EDPB, EDPS, Europska komisija (Press Corner + Digital Strategy), UK ICO, irski DPC, CNIL, ENISA, FTC, NIST, ISO.

**Udruge i neprofitne organizacije (9):** DAMA International, EDM Association (DCAM, CDMC), IAPP, Future of Privacy Forum, noyb, Partnership on AI, EPIC, Center for Data Innovation.

**Stručni mediji i odvjetnički blogovi (10):** EU AI Act Newsletter, Hunton, Inside Privacy, Privacy World, Robinson+Cole, Tech Policy Press, TDAN, DATAVERSITY, CDO Magazine, Modern Data 101.

**Analitičari (2 + 1 u široj rubrici):** Gartner, Forrester, McKinsey.

**Opći mediji, filtrirani (4 + 1 u široj rubrici):** Euractiv, POLITICO Europe, The Record, SiliconANGLE, MIT Technology Review.

**Dobavljači za governance (10):** Collibra, Alation, Atlan, Informatica, Ataccama, DataHub, Monte Carlo, OneTrust, BigID, Microsoft (Purview).

**Šira rubrika — platforme (6):** Databricks, Snowflake, AWS, Google Cloud, Data Engineering Weekly, dbt Labs.

## Pokrivenost kategorija

| Kategorija | Broj izvora | Ocjena |
|------------|-------------|--------|
| AI Governance | 20 | dobro |
| Privacy & Data Protection | 18 | dobro |
| Regulation & Compliance | 15 | dobro |
| Vendors & Market | 12 | dobro |
| Strategy & Operating Models | 10 | zadovoljavajuće |
| Metadata, Catalogs & Lineage | 10 | zadovoljavajuće |
| Data Quality | 6 | **slabo** |
| Security & Access | 6 | zadovoljavajuće (nije glavni fokus) |
| Master & Reference Data | 2 | **slabo** |

## Što je otkrila provjera

1. **Regulativa i privatnost lako se automatiziraju**, jer većina regulatora i odvjetničkih blogova ima ispravne RSS feedove.
2. **Najvažniji izvori za samu struku teže se dohvaćaju.** IAPP, TDAN, DATAVERSITY, CDO Magazine, Alation, Atlan i Informatica nemaju ispravan RSS i traže scraping. To je glavni posao u fazi 3.
3. **Tri izvora blokiraju automatski pristup** (Gartner, EK Digital Strategy, BigID). Njih pratimo ručno jednom tjedno ili posredno preko drugih izvora.
4. **Neki feedovi su napušteni**: EDM Council od 2025., datagovernance.com od 2020. i Medium kanal DataHuba. Zato su u katalogu zamijenjeni drugim adresama ili scrapingom.
5. **Šum je velik kod širokih izvora.** NIST, ISO, Europska komisija i Euractiv objavljuju uglavnom nevezane teme, pa im je uključen filter ključnih pojmova.

## Što nedostaje (za v0.2)

- **Data Quality i Master Data**: treba dodati više stručnih izvora (npr. Precisely, Reltio, Profisee, Semarchy, Soda, Great Expectations). Precisely blokira pristup, ostale treba provjeriti.
- **Nacionalni regulatori izvan EU**: npr. Singapur (PDPC), Kanada (OPC), Kalifornija (CPPA).
- **Financijski sektor**: BCBS 239, EBA i DORA, ako bude interesa za tu publiku.
- **Pojedinačni stručnjaci i newsletteri** iz data governance zajednice, osobito s LinkedIna. Njih treba odabrati ručno.
- **Tvoji izvori**: dodaj sve što već pratiš i čemu vjeruješ.

## Promjene u v0.2 (faza 3)

- **DATAVERSITY** ima ispravan RSS za članke (`/articles/feed/`) → prebačen na RSS.
- **TDAN** sada preusmjerava na DATAVERSITY → neaktivan.
- **ICO**, **EDM Association**: popis vijesti učitava se JavaScriptom → ručno praćenje.
- **Atlan**: blog više nema vijesti, nego vodiče → ručno, nizak prioritet.
- **Tech Policy Press**: previše općih tema → uključen filter ključnih pojmova.
- **FTC**: feed radi s korisničkim agentom našeg programa.
- Za 7 izvora koji se čitaju sa stranice definirana su pravila prepoznavanja poveznica (`scrape.link_pattern`); CDO Magazine isključuje sponzorirani sadržaj.

## Sljedeći korak

Faza 2 je kostur portala s probnim vijestima. Paralelno se katalog može dopunjavati, a u fazi 3 svi izvori ponovno se provjeravaju automatski.
