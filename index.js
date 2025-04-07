const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'zomato',
  password: 'nirali',
  port: 5432,
});

pool.connect()
  .then(() => console.log('✅ Connected to PostgreSQL'))
  .catch((err) => console.error('❌ Failed to connect to DB:', err));

module.exports = pool;
