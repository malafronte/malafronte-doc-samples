import bodyParser from "body-parser";
import jsonServer from "json-server";
import jwt from "jsonwebtoken";

const server = jsonServer.create();
const dbFile = process.argv[2] || "./db.json";
const router = jsonServer.router(dbFile);

server.use(bodyParser.urlencoded({ extended: true }));
server.use(bodyParser.json());
server.use(jsonServer.defaults({ static: "./public" }));

const SECRET_KEY = "123456789";
const expiresIn = "1h";

// Create a token from a payload
function createToken(payload) {
  return jwt.sign(payload, SECRET_KEY, { expiresIn });
}

// Verify the token
function verifyToken(token) {
  return jwt.verify(token, SECRET_KEY, (err, decode) =>
    decode !== undefined ? decode : err,
  );
}

// Check if the user exists in database
function isAuthenticated({ email, password }) {
  return email === "admin@example.com" && password === "admin123";
}

// Login endpoint
server.post("/login", (req, res) => {
  const { email, password } = req.body;
  if (isAuthenticated({ email, password }) === false) {
    const status = 401;
    const message = "Incorrect email or password";
    res.status(status).json({ status, message });
    return;
  }
  const access_token = createToken({ email });
  res.status(200).json({ access_token });
});

// Middleware to check token for POST, PUT, DELETE, PATCH
// L'espressione regolare /^(?!\/login).*$/ significa:
// ^        : Inizio della stringa (l'URL della richiesta)
// (?!\/login) : Negative lookahead. Assicura che la stringa NON inizi con "/login"
// .*       : Qualsiasi carattere (eccetto newline), zero o più volte
// $        : Fine della stringa
// In pratica: "Applica questo middleware a TUTTE le rotte TRANNE /login"
server.use(/^(?!\/login).*$/, (req, res, next) => {
  // Controlliamo se il metodo HTTP è uno di quelli che vogliamo proteggere
  if (
    req.method === "POST" ||
    req.method === "PUT" ||
    req.method === "DELETE" ||
    req.method === "PATCH"
  ) {
    // Verifichiamo che l'header 'Authorization' sia presente e che inizi con 'Bearer '
    if (
      req.headers.authorization === undefined ||
      req.headers.authorization.split(" ")[0] !== "Bearer"
    ) {
      const status = 401;
      const message = "Error in authorization format";
      res.status(status).json({ status, message });
      return;
    }
    try {
      // Estraiamo il token (la seconda parte dell'header dopo 'Bearer ')
      let verifyTokenResult;
      verifyTokenResult = verifyToken(req.headers.authorization.split(" ")[1]);

      // Se la verifica fallisce (es. token scaduto o firma non valida), verifyToken restituisce un oggetto Error
      if (verifyTokenResult instanceof Error) {
        const status = 401;
        const message = "Access token not provided or invalid";
        res.status(status).json({ status, message });
        return;
      }
      // Se il token è valido, passiamo il controllo al prossimo middleware (o alla rotta finale)
      next();
    } catch (err) {
      const status = 401;
      const message = "Error access_token is revoked";
      res.status(status).json({ status, message });
    }
  } else {
    // Se il metodo è GET (o un altro non protetto), passiamo direttamente al prossimo middleware
    next();
  }
});

server.use(router);

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

server.listen(3001, () => {
  console.log("JSON Server Auth is running on port 3001");
});
