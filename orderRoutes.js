const express = require('express');
const router = express.Router();
const pool = require('../db');

router.post('/order', async (req, res) => {
  console.log('➡️ Request received:', req.body);

  const { user_id, restaurant_id, items, quantity } = req.body;

  try {
    const restaurantCheck = await pool.query('SELECT * FROM restaurants WHERE id = $1', [restaurant_id]);
    if (restaurantCheck.rows.length === 0) {
      return res.status(404).json({ error: '❌ Restaurant not found' });
    }

    let total_price = 0;
    for (const item of items) {
      const menuItem = await pool.query('SELECT price FROM menu_items WHERE id = $1', [item.id]);
      if (menuItem.rows.length === 0) {
        return res.status(404).json({ error: `❌ Menu item with id ${item.id} not found` });
      }
      total_price += menuItem.rows[0].price * item.quantity;
    }

    const newOrder = await pool.query(
      `INSERT INTO orders (user_id, restaurant_id, items, total_price, status, quantity) 
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [user_id, restaurant_id, JSON.stringify(items), total_price, 'Pending', quantity]
    );

    res.status(201).json(newOrder.rows[0]);

  } catch (err) {
    console.error('⚠️ SQL Error:', err.stack);
    res.status(500).json({ error: '⚠️ Internal server error', details: err.message });
  }
});

module.exports = router;
