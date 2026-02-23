const fs = require("fs");
const { faker } = require("@faker-js/faker");

// Configurazione
const PRODUCTS_COUNT = 100;
const COMPANIES_COUNT = 100;

console.log("Inizio generazione dati mock...");

// Funzione helper per generare Locations
const generateLocations = () => {
  const locationsCount = faker.number.int({ min: 1, max: 5 });
  const locations = [];

  for (let i = 0; i < locationsCount; i++) {
    locations.push({
      city: faker.location.city(),
      employee_number: faker.number.int({ min: 10, max: 10000 }),
      state: faker.location.state(),
    });
  }
  return locations;
};

// 1. Generazione Companies
const companies = [];
for (let i = 1; i <= COMPANIES_COUNT; i++) {
  const company = {
    id: i,
    name: faker.company.name(),
    revenue: parseFloat(
      faker.finance.amount({ min: 1000000, max: 100000000, dec: 2 }),
    ),
    headquarter: {
      lat: faker.location.latitude(),
      lon: faker.location.longitude(),
    },
    locations: generateLocations(),
  };
  companies.push(company);
}

// 2. Generazione Products
const products = [];
for (let i = 1; i <= PRODUCTS_COUNT; i++) {
  const product = {
    id: i,
    name: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price({ min: 1, max: 1000, dec: 2 })),
    // Assegna casualmente un company_id esistente (da 1 a 100)
    company_id: faker.number.int({ min: 1, max: COMPANIES_COUNT }),
  };
  products.push(product);
}

// Struttura finale del DB
const database = {
  products: products,
  companies: companies,
};

// Scrittura su file db.json
const jsonString = JSON.stringify(database, null, 2);
fs.writeFileSync("db.json", jsonString);

console.log(`Generazione completata!`);
console.log(`- Creati ${products.length} prodotti.`);
console.log(`- Create ${companies.length} compagnie.`);
console.log(`Il file 'db.json' è pronto per essere servito.`);
