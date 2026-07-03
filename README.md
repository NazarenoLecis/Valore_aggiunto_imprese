# Valore aggiunto imprese

Data pipeline per scaricare, pulire, armonizzare, validare ed esportare dati sul valore aggiunto generato dalle imprese per dimensione, paese, anno e settore.

Il repository produce file JSON e Parquet da caricare su Cloudflare R2. La dashboard pubblica sarà sviluppata in un progetto separato su GitHub Pages e leggerà i JSON pubblicati su R2. Questo repository non contiene codice frontend, layout dashboard o workflow di deploy GitHub Pages.

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
- esportazione JSON per dashboard esterna;
- esportazione Parquet per archivio e riuso analitico;
- upload su Cloudflare R2;
- notebook di analisi;
- notebook di grafici;
- documentazione metodologica.

Fuori perimetro:

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

Output analitici completi:

```text
data/processed/*.parquet
data/processed/validation_report.json
data/processed/validation_report.md
```

Output per dashboard esterna:

```text
data/dashboard_json/*.json
```

I file vengono caricati su R2 con questa struttura logica:

```text
valore_aggiunto_imprese/
  latest/
    official_eurostat_sbs.json
    official_oecd_sdbs.json
    business_demography_distribution.json
    italy_granular_sources.json
    dashboard_country_sector_size.json
    dashboard_metadata.json
    sources.json
    data_dictionary.json
  archive/
    YYYY-MM-DD/
      ...
```

La dashboard GitHub Pages deve leggere i file da `latest`.

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
  r2_paths.yaml

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
  07_export_json_for_dashboard.py
  08_upload_to_r2.py
  09_run_full_pipeline.py

notebooks/
  01_esplorazione_fonti_eurostat_sbs.ipynb
  02_esplorazione_business_demography.ipynb
  03_esplorazione_oecd_sdbs.ipynb
  04_fonti_istat_italia_granulare.ipynb
  05_confronto_paesi_classi_ufficiali.ipynb
  06_focus_settoriale.ipynb
  07_metodologia_stima_classi_fini.ipynb
  08_grafici_per_dashboard.ipynb

docs/
  metodologia.md
  fonti.md
  dizionario_dati.md
  note_qualita.md
  r2_setup.md
  github_actions.md
  data_contract_dashboard.md
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
- dati raw, processed e dashboard JSON esclusi da Git.

## Installazione

```bash
pip install -r requirements.txt
```

## Uso

Esecuzione completa:

```bash
python scripts/09_run_full_pipeline.py
```

Esecuzione per singola fase:

```bash
python scripts/01_download_eurostat_sbs.py
python scripts/02_download_business_demography.py
python scripts/03_download_oecd_sdbs.py
python scripts/04_download_istat_sources.py
python scripts/05_build_clean_datasets.py
python scripts/06_validate_outputs.py
python scripts/07_export_json_for_dashboard.py
python scripts/08_upload_to_r2.py
```

## Configurazione R2

Le credenziali R2 devono essere impostate come variabili ambiente o come GitHub Actions secrets:

```text
R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET_NAME
R2_PUBLIC_BASE_URL
```

## Documentazione

La metodologia è documentata in `docs/metodologia.md`.

Le fonti sono documentate in `docs/fonti.md`.

Il contratto dati per la dashboard esterna è documentato in `docs/data_contract_dashboard.md`.

Il setup R2 è documentato in `docs/r2_setup.md`.
