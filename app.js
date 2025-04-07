const express = require('express');
const app = express();
const orderRoutes = require('./routes/orderRoutes');

app.use(express.json());

app.use('/api', orderRoutes);

app.listen(9000, () => console.log('🚀 Server running on http://localhost:9000'))
  .on('error', (err) => console.error('🔥 Server failed to start:', err));
