import jsonServer from "json-server";

const server = jsonServer.create();
const dbFile = process.argv[2] || "./db.json";
const router = jsonServer.router(dbFile);
const middlewares = jsonServer.defaults({ static: "./public" });

server.use(middlewares);

// Intercetta la risposta per gestire ?includeRelated=true
router.render = (req, res) => {
  let data = res.locals.data;

  // Applica il filtro solo per la rotta /products (sia lista che singolo prodotto)
  if (req.path.startsWith("/products")) {
    const includeRelated = req.query.includeRelated === "true";

    if (!includeRelated) {
      // Funzione per rimuovere i campi correlati
      const removeRelated = (product) => {
        // Creiamo una copia dell'oggetto escludendo i campi relazionali
        const { dimensions, meta, tags, images, reviews, ...rest } = product;
        return rest;
      };

      if (Array.isArray(data)) {
        data = data.map(removeRelated);
      } else if (
        data &&
        typeof data === "object" &&
        Object.keys(data).length > 0
      ) {
        data = removeRelated(data);
      }
    }
  }

  res.json(data);
};

server.use(router);

server.listen(3000, () => {
  console.log("JSON Server is running on port 3000");
});
