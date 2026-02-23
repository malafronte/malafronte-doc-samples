import { faker } from "@faker-js/faker";
import fs from "fs";

function generateProducts() {
  const products = [];

  // Generiamo 30 prodotti per farli corrispondere alle 30 cartelle di immagini locali
  // che abbiamo copiato precedentemente (da 1 a 30)
  for (let id = 1; id <= 30; id++) {
    products.push({
      id: id,
      title: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      category: faker.commerce.department().toLowerCase(),
      price: parseFloat(faker.commerce.price()),
      discountPercentage: faker.number.float({
        min: 0,
        max: 20,
        fractionDigits: 2,
      }),
      rating: faker.number.float({ min: 1, max: 5, fractionDigits: 2 }),
      stock: faker.number.int({ min: 0, max: 100 }),
      tags: [
        { value: faker.commerce.productAdjective() },
        { value: faker.commerce.productMaterial() },
      ],
      brand: faker.company.name(),
      sku: faker.string.alphanumeric(8).toUpperCase(),
      weight: faker.number.int({ min: 1, max: 10 }),
      dimensions: {
        width: faker.number.float({ min: 5, max: 50, fractionDigits: 2 }),
        height: faker.number.float({ min: 5, max: 50, fractionDigits: 2 }),
        depth: faker.number.float({ min: 5, max: 50, fractionDigits: 2 }),
      },
      warrantyInformation: `${faker.number.int({ min: 1, max: 5 })} year warranty`,
      shippingInformation: `Ships in ${faker.number.int({ min: 1, max: 4 })} weeks`,
      availabilityStatus: faker.helpers.arrayElement([
        "In Stock",
        "Low Stock",
        "Out of Stock",
      ]),
      reviews: [
        {
          rating: faker.number.int({ min: 1, max: 5 }),
          comment: faker.lorem.sentence(),
          date: faker.date.recent().toISOString(),
          reviewerName: faker.person.fullName(),
          reviewerEmail: faker.internet.email(),
        },
      ],
      returnPolicy: `${faker.number.int({ min: 7, max: 90 })} days return policy`,
      minimumOrderQuantity: faker.number.int({ min: 1, max: 10 }),
      meta: {
        createdAt: faker.date.past().toISOString(),
        updatedAt: faker.date.recent().toISOString(),
        barcode: faker.string.numeric(13),
        // URL LOCALI per il QR Code
        qrCode: `http://localhost:3000/assets/products_media/${id}/qrcode/qr-code.png`,
      },
      images: [
        // URL LOCALI per le immagini
        {
          url: `http://localhost:3000/assets/products_media/${id}/images/1.png`,
        },
      ],
      // URL LOCALE per la thumbnail
      thumbnail: `http://localhost:3000/assets/products_media/${id}/thumbnail/thumbnail.png`,
    });
  }

  return { products };
}

const data = generateProducts();
fs.writeFileSync("db-faker.json", JSON.stringify(data, null, 2));
console.log("Generato db-faker.json con 30 prodotti mockati tramite Faker!");
