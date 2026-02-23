# Mock Server Auth

Questo progetto è un server mock basato su [json-server](https://github.com/typicode/json-server) che espone un'API RESTful per la gestione di prodotti, **con l'aggiunta di un sistema di autenticazione basato su JWT (JSON Web Token)**. È stato creato per simulare un backend reale che richiede l'autenticazione per le operazioni di modifica dei dati, permettendo lo sviluppo e il test del client C# (`ApiClientAuth`).

## Caratteristiche Principali

- **API REST Completa**: Supporta operazioni CRUD (GET, POST, PUT, DELETE) sulla risorsa `/products`.
- **Autenticazione JWT**: Le operazioni di modifica (POST, PUT, PATCH, DELETE) richiedono un token JWT valido nell'header `Authorization`. Le operazioni di lettura (GET) sono pubbliche.
- **Endpoint di Login**: Fornisce un endpoint `/login` per ottenere un token JWT fornendo credenziali valide.
- **Dati Iniziali (Seed)**: Utilizza i dati provenienti dal file `db.json`, adattati per corrispondere ai DTO attesi dal client C#.
- **Risorse Multimediali Locali**: Le immagini, le miniature e i QR code dei prodotti sono serviti localmente dalla cartella `public/assets/products_media`.
- **Generazione Dati Casuali**: Include uno script basato su [Faker.js](https://fakerjs.dev/) per generare un dataset alternativo di prodotti casuali.

## Prerequisiti

- [Node.js](https://nodejs.org/) installato sul sistema.

## Installazione

1. Apri un terminale nella cartella `mock-server-auth`.
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

Il server sarà in ascolto all'indirizzo: `http://localhost:3001`

### 2. Con dati generati casualmente (Faker)

Questa modalità utilizza il file `db-faker.json`.

```bash
npm run start:faker
```

Il server sarà in ascolto all'indirizzo: `http://localhost:3001`

*Nota: Se il file `db-faker.json` non esiste o vuoi rigenerare i dati, esegui prima il comando:*

```bash
npm run generate
```

## Endpoint Disponibili

Tutti gli endpoint rispondono all'URL base `http://localhost:3001`.

### Autenticazione (`/login`)

- **`POST /login`**: Endpoint per ottenere il token JWT.
  - **Corpo della richiesta (JSON)**:

    ```json
    {
      "email": "admin@example.com",
      "password": "admin123"
    }
    ```

  - **Risposta (JSON)**:

    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### Prodotti (`/products`)

- **`GET /products`**: Recupera la lista di tutti i prodotti. *(Pubblico)*
- **`GET /products/:id`**: Recupera i dettagli di un singolo prodotto tramite il suo ID. *(Pubblico)*
- **`POST /products`**: Crea un nuovo prodotto. *(Richiede Autenticazione)*
- **`PUT /products/:id`**: Aggiorna un prodotto esistente. *(Richiede Autenticazione)*
- **`PATCH /products/:id`**: Aggiorna parzialmente un prodotto esistente. *(Richiede Autenticazione)*
- **`DELETE /products/:id`**: Elimina un prodotto tramite il suo ID. *(Richiede Autenticazione)*

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

## Come usare l'Autenticazione

Per effettuare richieste agli endpoint protetti (POST, PUT, PATCH, DELETE), devi includere il token JWT ottenuto dall'endpoint `/login` nell'header `Authorization` della tua richiesta HTTP, utilizzando lo schema `Bearer`:

```http
Authorization: Bearer <il_tuo_token_jwt>
```

Se il token è mancante, non valido o scaduto, il server risponderà con uno status code `401 Unauthorized`.

## Struttura del Progetto

- `server.js`: Il file principale del server che configura `json-server`, gestisce l'autenticazione JWT e definisce i middleware.
- `db.json`: Il database JSON principale con i dati di seed.
- `db-faker.json`: Il database JSON generato dinamicamente con Faker.js.
- `generate-data.js`: Lo script Node.js che utilizza Faker.js per generare `db-faker.json`.
- `package.json`: Contiene le dipendenze e gli script di avvio.
- `public/`: Cartella che contiene i file statici (immagini, ecc.) serviti dal server.
