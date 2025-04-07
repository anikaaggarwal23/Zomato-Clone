require("dotenv").config({ path: __dirname + "/.env" });

console.log("✅ DATABASE_URL:", process.env.DATABASE_URL);
console.log("✅ ENV test:", process.env.DATABASE_URL);

const { Pool } = require("pg");


const pool = new Pool({
  connectionString: process.env.DATABASE_URL, 
});
pool.connect((err) => {
  if (err) {
    console.error("❌ Database connection failed! Error:", err.stack);
  } else {
    console.log("✅ Database connected successfully!");
  }
});

module.exports = pool;
