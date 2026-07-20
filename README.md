# Valore aggiunto imprese

Questo repository costruisce dataset e notebook di analisi sul valore aggiunto generato dalle imprese per classe dimensionale, paese, anno e settore.

La pipeline scarica dati Eurostat, crea inventari per OECD e ISTAT, normalizza gli output in uno schema comune, valida i file prodotti ed esporta CSV e JSON locali. I notebook sono fogli di lavoro analitici con tabelle, grafici e commento dei risultati.

## Struttura

```text
valore_aggiunto_imprese/
  analysis.py
  config.py
  export.py
  pipeline.py
  sources.py
  transform.py
  utils.py
notebooks/
data/
outputs/
```

## Installazione

```bash
pip install -r requirements.txt
```

## Esecuzione

```bash
python -m valore_aggiunto_imprese.pipeline
```

Output generati:

```text
data/processed_csv/
data/processed_json/
data/validation/
outputs/charts/
```

I dati scaricati e gli output generati non sono versionati.

## Fonti

Eurostat Structural Business Statistics e la fonte principale per valore aggiunto, imprese, occupazione e produttivita apparente per classe dimensionale nei paesi UE.

Eurostat Business Demography descrive la distribuzione delle imprese nelle classi piu piccole. Non contiene valore aggiunto e non viene usata per imputarlo automaticamente.

OECD Structural and Demographic Business Statistics e predisposta come fonte per estendere il confronto internazionale. La pipeline attuale crea un inventario operativo.

ISTAT e predisposta per verificare fonti italiane piu granulari, per esempio Frame SBS, Frame territoriale, conti economici e microdati.

## Paesi

La configurazione include i 27 Paesi UE con codici Eurostat:

```text
AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, FI, FR, HR, HU, IE, IT,
LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK
```

## Schema Dati

I dataset finali sono salvati in CSV e JSON orientato a record. La chiave logica minima e composta da paese, anno, fonte, settore, classe dimensionale e metrica.

Colonne principali:

```text
country_code
country_name
year
source_name
source_dataset_id
sector_code_original
sector_code_harmonised
size_class_original
size_class_harmonised
metric_code
metric_label
value
unit
method_status
quality_flag
download_timestamp
source_url
notes
```

## Metodologia

Il progetto separa dati osservati, dati di distribuzione e stime.

`observed_official` indica un dato pubblicato direttamente da una fonte ufficiale.

`distribution_only` indica un dato utile per descrivere numero di imprese o occupati, senza valore aggiunto osservato.

`estimated_from_distribution` indica un valore costruito con ipotesi esplicite.

Le classi comparabili Eurostat sono `0-9`, `10-19`, `20-49`, `50-249` e `250+`.

Le micro-classi Business Demography sono usate come distribuzioni descrittive e non trasformano automaticamente il valore aggiunto osservato in stime fini.

## Qualita

La pipeline valida colonne obbligatorie, valori ammessi di `method_status` e duplicati rispetto alle chiavi logiche. Ogni notebook usa l'ultimo anno con valori disponibili per la metrica rappresentata, cosi evita grafici vuoti quando una fonte ha aggiornamenti non uniformi tra indicatori.

I grafici riportano in basso a sinistra fonte dei dati ed elaborazione.
