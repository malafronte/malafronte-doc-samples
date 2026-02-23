# Mock Server Products

Questo progetto è un server mock basato su [json-server](https://github.com/typicode/json-server) che espone un'API RESTful per la gestione di prodotti. È stato creato per simulare il comportamento di un backend reale (come quello in `MinimalApiCrudSqlite`) e permettere lo sviluppo e il test del client C# (`ApiClient`).

## Caratteristiche Principali

- **API REST Completa**: Supporta operazioni CRUD (GET, POST, PUT, DELETE) sulla risorsa `/products`.
- **Dati Iniziali (Seed)**: Utilizza i dati provenienti dal file `db.json`, che sono stati adattati per corrispondere esattamente ai DTO (Data Transfer Objects) attesi dal client C#.
- **Risorse Multimediali Locali**: Le immagini, le miniature (thumbnails) e i QR code dei prodotti sono serviti localmente dalla cartella `public/assets/products_media`, simulando un vero file server.
- **Generazione Dati Casuali**: Include uno script basato su [Faker.js](https://fakerjs.dev/) per generare un dataset alternativo di prodotti casuali.

## Prerequisiti

- [Node.js](https://nodejs.org/) installato sul sistema.

## Installazione

1. Apri un terminale nella cartella `mock-server-products`.
2. Installa le dipendenze eseguendo:

   ```bash
   npm install
   ```

## Avvio del Server

Puoi avviare il server in due modalità diverse:

### 1. Con i dati originali (Seed)

Questa modalità utilizza il file `db.json` che contiene i dati originali adattati.

```bash
npm start
```

Il server sarà in ascolto all'indirizzo: `http://localhost:3000`

### 2. Con dati generati casualmente (Faker)

Questa modalità utilizza il file `db-faker.json`.

```bash
npm run start:faker
```

Il server sarà in ascolto all'indirizzo: `http://localhost:3000`

*Nota: Se il file `db-faker.json` non esiste o vuoi rigenerare i dati, esegui prima il comando:*

```bash
npm run generate
```

## Endpoint Disponibili

Tutti gli endpoint rispondono all'URL base `http://localhost:3000`.

### Prodotti (`/products`)

- **`GET /products`**: Recupera la lista di tutti i prodotti.
- **`GET /products/:id`**: Recupera i dettagli di un singolo prodotto tramite il suo ID.
- **`POST /products`**: Crea un nuovo prodotto. Invia i dati del prodotto nel corpo della richiesta in formato JSON.
- **`PUT /products/:id`**: Aggiorna un prodotto esistente. Invia i dati aggiornati nel corpo della richiesta in formato JSON.
- **`PATCH /products/:id`**: Aggiorna parzialmente un prodotto esistente.
- **`DELETE /products/:id`**: Elimina un prodotto tramite il suo ID.

### Relazioni (`?includeRelated=true`)

Per simulare il comportamento dell'API C# (Entity Framework), di default gli endpoint `GET /products` e `GET /products/:id` **non** restituiscono i campi relazionali (`dimensions`, `meta`, `tags`, `images`, `reviews`).

Per includere questi campi nella risposta, è necessario aggiungere il parametro di query `?includeRelated=true`:

- `GET /products?includeRelated=true`
- `GET /products/1?includeRelated=true`

### Risorse Statiche (Media)

Le immagini e i file associati ai prodotti sono accessibili tramite URL statici. Ad esempio, per il prodotto con ID `1`:

- **Immagine**: `GET /assets/products_media/1/images/1.png`
- **Miniatura**: `GET /assets/products_media/1/thumbnail/thumbnail.png`
- **QR Code**: `GET /assets/products_media/1/qrcode/qr-code.png`

## Struttura del Progetto

- `db.json`: Il database JSON principale con i dati di seed.
- `db-faker.json`: Il database JSON generato dinamicamente con Faker.js.
- `generate-data.js`: Lo script Node.js che utilizza Faker.js per generare `db-faker.json`.
- `package.json`: Contiene le dipendenze e gli script di avvio.
- `public/`: Cartella che contiene i file statici (immagini, ecc.) serviti dal server.
