# Valore aggiunto imprese

Questo repository costruisce dati e grafici sul valore aggiunto generato dalle imprese per dimensione, paese, anno e settore.

Il progetto genera dataset locali in CSV e JSON e grafici di analisi. I notebook documentano fonti, controlli, limiti e interpretazione dei risultati.

## Output

```text
data/processed_csv/
data/processed_json/
outputs/charts/
```

## Fonti

Le fonti previste sono Eurostat Structural Business Statistics, Eurostat Business Demography, OECD Structural and Demographic Business Statistics e ISTAT.

## Configurazione

Le variabili operative stanno in codice Python:

```text
src/project_config.py
```

Gli script importano queste variabili e le passano alle funzioni.

## Struttura

```text
src/project_config.py
src/utils/
src/sources/
src/transform/
src/validation/
src/export/
scripts/
notebooks/
docs/
```

## Installazione

```bash
pip install -r requirements.txt
```

## Esecuzione

```bash
python scripts/08_run_full_pipeline.py
```

Singole fasi:

```bash
python scripts/01_download_eurostat_sbs.py
python scripts/02_download_business_demography.py
python scripts/03_download_oecd_sdbs.py
python scripts/04_download_istat_sources.py
python scripts/05_build_clean_datasets.py
python scripts/06_validate_outputs.py
python scripts/07_export_csv_json.py
```

## Stato metodologico

Ogni riga dei dataset finali deve avere `method_status`.

Valori ammessi:

```text
observed_official
distribution_only
estimated_from_distribution
italy_granular_observed
experimental
not_available
```

## Regole di codice

Usare funzioni riutilizzabili in `src/utils/`. Evitare classi e file `__init__.py`. Definire le variabili operative in codice Python. Usare commenti estensivi negli script. Produrre notebook di analisi e grafici commentati.
