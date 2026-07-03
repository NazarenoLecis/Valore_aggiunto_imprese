# Valore aggiunto imprese

Questo repository costruisce dati e grafici sul valore aggiunto generato dalle imprese per dimensione, paese, anno e settore.

L’obiettivo è avere una base dati pulita e riutilizzabile per confrontare Italia, paesi europei e paesi OCSE, distinguendo tra classi dimensionali ufficiali, distribuzioni più granulari delle imprese e possibili approfondimenti sull’Italia.

## Cosa produce

Il progetto genera tre tipi di output locali.

Dataset CSV:

```text
data/processed_csv/
```

Dataset JSON:

```text
data/processed_json/
```

Grafici di analisi:

```text
outputs/charts/
```

I notebook contengono anche commenti metodologici, controlli sui dati e spiegazioni dei grafici.

## Cosa analizza

Il progetto serve a studiare:

- valore aggiunto per classe dimensionale d’impresa;
- numero di imprese per classe dimensionale;
- occupazione per classe dimensionale;
- produttività apparente del lavoro;
- confronto tra paesi europei;
- confronto tra paesi OCSE;
- confronto per settore;
- struttura delle microimprese;
- granularità disponibile per l’Italia.

La produttività apparente del lavoro viene calcolata come:

```text
valore aggiunto / persone occupate
```

Non misura la produttività totale dei fattori.

## Fonti previste

Le fonti principali sono:

- Eurostat Structural Business Statistics;
- Eurostat Business Demography;
- OECD Structural and Demographic Business Statistics;
- ISTAT, per verificare eventuali dati più granulari sull’Italia.

Eurostat SBS è la fonte principale per valore aggiunto, imprese e occupazione per classe dimensionale nei paesi europei.

Eurostat Business Demography serve a descrivere meglio la distribuzione delle imprese, soprattutto nelle classi più piccole.

OECD SDBS serve a estendere il confronto ai paesi OCSE.

ISTAT serve a verificare se per l’Italia esistono dati più granulari rispetto alle classi pubblicate nelle fonti internazionali.

## Classi dimensionali

Classi ufficiali Eurostat usate come base comparabile:

```text
0-9
10-19
20-49
50-249
250+
```

Classi disponibili in alcune fonti di distribuzione:

```text
0
1-4
5-9
10+
```

Classi sperimentali da usare solo se supportate da dati osservati o da una metodologia esplicita:

```text
0
1
2-4
5-9
10-14
15-19
20-49
50-99
100-249
250-499
500+
```

## Stato metodologico del dato

Ogni riga dei dataset finali deve avere un campo `method_status`.

Valori ammessi:

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

## Installazione

Creare un ambiente Python e installare le dipendenze:

```bash
pip install -r requirements.txt
```

## Esecuzione

Per eseguire tutta la pipeline:

```bash
python scripts/08_run_full_pipeline.py
```

Per eseguire una singola fase:

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

I notebook servono a controllare i dati e produrre grafici commentati.

Ogni notebook deve contenere:

- obiettivo dell’analisi;
- fonte usata;
- copertura temporale e geografica;
- classi dimensionali disponibili;
- controlli sui valori mancanti;
- grafici;
- commenti interpretativi;
- note metodologiche.

## Regole di codice

Il codice segue queste regole:

- funzioni riutilizzabili dentro `src/utils/`;
- niente classi Python;
- niente `argparse`;
- niente file `__init__.py`;
- configurazione tramite file YAML;
- commenti estensivi negli script;
- notebook per analisi e grafici;
- output CSV, JSON e grafici generati esclusi da Git.

## Documentazione

La metodologia è documentata in:

```text
docs/metodologia.md
```

Le fonti sono documentate in:

```text
docs/fonti.md
```

Il dizionario dei dati è documentato in:

```text
docs/dizionario_dati.md
```

Le note sulla qualità del dato sono documentate in:

```text
docs/note_qualita.md
```

Il contratto dati è documentato in:

```text
docs/data_contract.md
```
