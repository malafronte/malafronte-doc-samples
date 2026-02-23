# Esempi di codice utilizzati nei siti didattici del Prof. Gennaro Malafronte

Sito di documentazione per i corsi di informatica del Prof. Gennaro Malafronte all'Istituto "Alessandro Greppi" di Monticello Brianza

## Indice dei Progetti

### [Samples Quarta](#samples-quarta)

- [API Client Server Demos](#api-client-server-demos)
- [Demo Events](#demo-events)
- [Entity Framework Core](#entity-framework-core)
- [LINQ Demo](#linq-demo)

### [Samples Quinta](#samples-quinta)

- [Esempio 1](#esempio-1)

### [Samples Terza](#samples-terza)

### [Tools and Scripts](#tools-and-scripts)

- [GitHub Download Directory](#github-download-directory)

---

## Samples Quarta

### API Client Server Demos

Progetti di esempio per la comunicazione client-server con API REST e mock server.

- **[mock-server-tutorial/](samples-quarta/api_client_server_demos/mock-server-tutorial/)** - Tutorial sull'utilizzo di JSON Server con generazione di dati mock usando Faker.js
- **[ApiClient/](samples-quarta/api_client_server_demos/products/ApiClient/)** - Client .NET che consume un'API REST per la gestione di prodotti
- **[ApiClientAuth/](samples-quarta/api_client_server_demos/products/ApiClientAuth/)** - Client .NET con autenticazione per l'API dei prodotti
- **[MinimalApiCrudSqlite/](samples-quarta/api_client_server_demos/products/MinimalApiCrudSqlite/)** - Minimal API ASP.NET Core con operazioni CRUD su database SQLite per la gestione completa di prodotti (inclusi tag, recensioni, immagini, dimensioni e metadati)
- **[mock-server-auth/](samples-quarta/api_client_server_demos/products/mock-server-auth/)** - Mock server Node.js con autenticazione per testing dei client
- **[mock-server-products/](samples-quarta/api_client_server_demos/products/mock-server-products/)** - Mock server Node.js per testing dell'API prodotti

### Demo Events

Esempi di programmazione orientata agli eventi in C#.

- **[DemoEvents/](samples-quarta/DemoEvents/DemoEvents/)** - Demo completa sugli eventi in C#
- **[DemoEventsSimple/](samples-quarta/DemoEvents/DemoEventsSimple/)** - Versione semplificata della demo sugli eventi

### Entity Framework Core

Esempi pratici di utilizzo di Entity Framework Core per l'accesso ai dati.

- **[DbUtilizziPC/](samples-quarta/EFCore/DbUtilizziPC/DbUtilizziPC/)** - Database per tracciare l'utilizzo dei PC
- **[EFGetStarted/](samples-quarta/EFCore/EFGetStarted/EFGetStarted/)** - Tutorial introduttivo a Entity Framework Core
- **[GestioneFattureClienti/](samples-quarta/EFCore/GestioneFattureClienti/GestioneFattureClienti/)** - Sistema per la gestione delle fatture dei clienti
- **[MigrationsTest/](samples-quarta/EFCore/MigrationsTest/MigrationsTest/)** - Test delle migration di EF Core con database di blog
- **[Romanzi/](samples-quarta/EFCore/Romanzi/Romanzi/)** - Database per la gestione di romanzi
- **[Universita/](samples-quarta/EFCore/Universita/Universita/)** - Database per la gestione universitaria

### LINQ Demo

Esempi di utilizzo di LINQ (Language Integrated Query) in C#.

- **[LINQAlMuseo/](samples-quarta/LINQDemo/LINQAlMuseo/)** - Esempio LINQ con tema museale (artisti, opere, personaggi)
- **[LINQDemo/](samples-quarta/LINQDemo/LINQDemo/)** - Demo base delle funzionalità LINQ
- **[LINQDemo2/](samples-quarta/LINQDemo/LINQDemo2/)** - Esempi avanzati di LINQ
- **[LINQDemo3/](samples-quarta/LINQDemo/LINQDemo3/)** - Ulteriori esempi di LINQ
- **[LINQGym/](samples-quarta/LINQDemo/LINQGym/)** - Esempio LINQ con tema palestra

---

## Samples Quinta

### Esempio 1

- **[esempio1/](samples-quinta/esempio1/)** - Esempio di sviluppo web con HTML, CSS e JavaScript

---

## Samples Terza

Sezione attualmente vuota - in preparazione

---

## Tools and Scripts

### GitHub Download Directory

Script utili per scaricare sottocartelle specifiche da repository GitHub, simile a [download-directory.github.io](https://download-directory.github.io) ma eseguibili localmente.

- **[download-github-folder.py](tools-and-scripts/github-download-directory/download-github-folder.py)** - Script Python base per scaricare cartelle da GitHub su repository pubblici (non supporta repository privati)
- **[download-github-folder.sh](tools-and-scripts/github-download-directory/download-github-folder.sh)** - Script Bash base per scaricare cartelle da GitHub su repository pubblici (non supporta repository privati)
- **[download-github-folder-optimized.py](tools-and-scripts/github-download-directory/download-github-folder-optimized.py)** ⭐ - Versione Python ottimizzata con `git sparse-checkout` (consigliata) - supporta repository privati con token
- **[download-github-folder-optimized.sh](tools-and-scripts/github-download-directory/download-github-folder-optimized.sh)** ⭐ - Versione Bash ottimizzata con `git sparse-checkout` (consigliata) - supporta repository privati con token

**Caratteristiche delle versioni ottimizzate:**

- 📥 Scarica solo la cartella richiesta (non l'intero repository)
- 🎯 Funziona con qualsiasi repository GitHub
- 🛡️ Gestione automatica degli errori
- 🧹 Pulizia automatica dei file temporanei
- 🔐 Supporto ai repository privati tramite token GitHub

Per maggiori dettagli sull'utilizzo, consulta il [README dedicato](tools-and-scripts/github-download-directory/README.md).
