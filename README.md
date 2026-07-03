# Valore aggiunto imprese

Repository per scaricare, pulire, armonizzare, validare e analizzare dati sul valore aggiunto generato dalle imprese per dimensione, paese, anno e settore.

Il progetto genera dataset CSV e JSON, insieme a notebook e grafici di analisi commentati. Non gestisce upload su Cloudflare R2, non contiene codice frontend e non gestisce la dashboard GitHub Pages. L'eventuale pubblicazione dei JSON su R2 e la dashboard pubblica sono fuori dal perimetro di questo repository.

## Obiettivi

Il progetto serve a costruire una base dati comparabile per analizzare:

- valore aggiunto per classe dimensionale d'impresa;
- numero di imprese per classe dimensionale;
- occupazione per classe dimensionale;
- produttività apparente del lavoro, calcolata come valore aggiunto per persona occupata;
- confronto tra paesi europei e OCSE;
- confronto per settore;
- approfondimento specifico sull'Italia, se sono disponibili fonti più granulari.

La pipeline distingue sempre tra dato osservato, dato usato solo per distribuzioni e dato stimato. Ogni riga dei dataset finali contiene un campo `method_status`.

## Perimetro

Incluso nel repository:

- download dati;
- pulizia dati;
- armonizzazione fonti;
- validazione output;
- generazione dataset CSV;
- generazione dataset JSON;
- notebook di analisi;
- notebook di grafici;
- grafici esportati per controllo e riuso analitico;
- commenti metodologici nei notebook;
- documentazione metodologica.

Fuori perimetro:

- upload su Cloudflare R2;
- credenziali R2;
- workflow di caricamento su R2;
- HTML della dashboard;
- JavaScript della dashboard;
- CSS della dashboard;
- layout GitHub Pages;
- workflow di deploy GitHub Pages;
- componenti frontend.

## Fonti principali

Fonti previste nella prima versione:

- Eurostat Structural Business Statistics, per valore aggiunto, imprese e occupazione per classe dimensionale e settore nei paesi europei;
- Eurostat Business Demography, per distribuzioni più granulari di imprese e occupazione;
- OECD Structural and Demographic Business Statistics, per confronto OCSE;
- ISTAT, per verificare se l'Italia consente dettaglio più granulare.

## Output

Output tabellari completi:

```text
data/processed_csv/*.csv
data/processed_json/*.json
```

Output di validazione:

```text
data/validation/validation_report.json
data/validation/validation_report.md
```

Output grafici:

```text
outputs/charts/*.png
outputs/charts/*.html
```

I file CSV e JSON sono generati localmente dalla pipeline. Possono poi essere usati da un altro progetto o caricati su R2 tramite una pipeline separata. Questo repository non esegue il caricamento.

## Flag metodologici

Valori ammessi per `method_status`:

```text
observed_official
```

Dato osservato e pubblicato da fonte ufficiale.

```text
distribution_only
```

Dato ufficiale usato solo per descrivere distribuzioni di imprese o occupati.

```text
estimated_from_distribution
```

Dato stimato dalla pipeline a partire da distribuzioni, vincoli ufficiali e ipotesi documentate.

```text
italy_granular_observed
```

Dato italiano più granulare osservato da fonte ufficiale.

```text
experimental
```

Output in fase di test.

```text
not_available
```

Dato non disponibile.

## Struttura del repository

```text
config/
  settings.yaml
  sources.yaml
  countries.yaml
  sectors.yaml
  size_classes.yaml

src/
  utils/
  sources/
  transform/
  validation/
  export/

scripts/
  01_download_eurostat_sbs.py
  02_download_business_demography.py
  03_download_oecd_sdbs.py
  04_download_istat_sources.py
  05_build_clean_datasets.py
  06_validate_outputs.py
  07_export_csv_json.py
  08_run_full_pipeline.py

notebooks/
  01_esplorazione_fonti_eurostat_sbs.ipynb
  02_esplorazione_business_demography.ipynb
  03_esplorazione_oecd_sdbs.ipynb
  04_fonti_istat_italia_granulare.ipynb
  05_confronto_paesi_classi_ufficiali.ipynb
  06_focus_settoriale.ipynb
  07_metodologia_stima_classi_fini.ipynb
  08_grafici_analisi_commentati.ipynb

docs/
  metodologia.md
  fonti.md
  dizionario_dati.md
  note_qualita.md
  data_contract.md
```

## Regole di codice

Il codice del progetto segue queste regole:

- funzioni riutilizzabili dentro `src/utils/`;
- niente classi Python;
- niente `argparse`;
- niente file `__init__.py`;
- configurazione tramite file YAML;
- commenti estensivi negli script;
- notebook per analisi e grafici;
- nessuna credenziale nel repository;
- output CSV, JSON e grafici generati esclusi da Git.

## Installazione

```bash
pip install -r requirements.txt
```

## Uso

Esecuzione completa:

```bash
python scripts/08_run_full_pipeline.py
```

Esecuzione per singola fase:

```bash
python scripts/01_download_eurostat_sbs.py
python scripts/02_download_business_demography.py
python scripts/03_download_oecd_sdbs.py
python scripts/04_download_istat_sources.py
python scripts/05_build_clean_datasets.py
python scripts/06_validate_outputs.py
python scripts/07_export_csv_json.py
```

## Notebook

I notebook devono essere parte centrale del progetto. Ogni notebook deve contenere:

- obiettivo dell'analisi;
- fonte usata;
- controlli sulla copertura del dato;
- grafici commentati;
- note metodologiche;
- limiti del dato.

I grafici generati dai notebook devono essere esportabili in `outputs/charts/`.

## Documentazione

La metodologia è documentata in `docs/metodologia.md`.

Le fonti sono documentate in `docs/fonti.md`.

Il dizionario dei dati è documentato in `docs/dizionario_dati.md`.

Il contratto dati per eventuali progetti esterni è documentato in `docs/data_contract.md`.
