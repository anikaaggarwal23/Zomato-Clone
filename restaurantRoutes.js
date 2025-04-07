const express = require("express");
const pool = require("./db");

const router = express.Router();

router.get("/restaurants", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM restaurants");
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send("Server error");
  }
});

router.get("/restaurants/:id", async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query("SELECT * FROM restaurants WHERE id = $1", [id]);
    if (result.rows.length === 0) return res.status(404).json({ msg: "Restaurant not found" });
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err.message);
    res.status(500).send("Server error");
  }
});

router.get("/restaurants/:id/menu", async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query("SELECT * FROM menu_items WHERE restaurant_id = $1", [id]);
    if (result.rows.length === 0) return res.status(404).json({ msg: "No menu found for this restaurant" });
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send("Server error");
  }
});

module.exports = router;
