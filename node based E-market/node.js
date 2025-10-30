const express = require('express');
const db = require('./config/db'); 

const app = express();
app.use(express.json());

const session = require('express-session');
const MySQLStore = require('express-mysql-session')(session);


const sessionStore = new MySQLStore({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'node_website'
});

app.use(session({
  key: 'session_cookie_name', 
  secret: 'my_secret',
  resave: false,
  saveUninitialized: false,
  store: sessionStore,
  cookie: { maxAge: 300000 }
}));


app.get('/product', (req, res) => {
  const query = 'SELECT * FROM product';
  db.query(query, (err, results) => {
    if (err) {
      console.error(' Database query failed:', err);
      return res.status(500).json({ error: 'Database query failed' });
    }
    res.status(200).json(results);
  });
});

app.get('/order', (req, res) => {
  const query = 'SELECT * FROM booking';
  db.query(query, (err, results) => {
    if (err) {
      console.error(' Database query failed:', err);
      return res.status(500).json({ error: 'Database query failed' });
    }
    res.status(200).json(results);
  });
});


app.get('/session', (req, res) => {
  res.json(req.session);
});


app.get('/sessions', (req, res) => {
  const sql = 'SELECT session_id, data FROM sessions';
  db.query(sql, (err, results) => {
    if (err) return res.status(500).json({ error: 'Failed to fetch sessions' });
    const activeSessions = results.map(s => {
      const data = JSON.parse(s.data);
      return {
        session_id: s.session_id,
        username: data.user ? data.user.username : 'Guest'
      };
    });
    res.json(activeSessions);
  });
});




app.post('/product', (req, res) => {
  const { product_name, product_count } = req.body;

  if (!product_name || !product_count) {
    return res.status(400).json({ error: 'Product name and count are required' });
  }

  
  const checkQuery = 'SELECT * FROM product WHERE product_name = ?';
  db.query(checkQuery, [product_name], (err, results) => {
    if (err) 
      return res.status(500).json({ error: 'Database error' });

    if (results.length > 0) {
      
      const updateQuery = 'UPDATE product SET product_count = product_count + ? WHERE product_name = ?';
      db.query(updateQuery, [product_count, product_name], (err2) => {
        if (err2) 
        return res.status(500).json({ error: 'Update failed' });
        res.json({ message: ` ${product_name} count updated successfully!` });
      });
    } else {
      
      const insertQuery = 'INSERT INTO product (product_name, product_count) VALUES (?, ?)';
      db.query(insertQuery, [product_name, product_count], (err3) => {
        if (err3)
          return res.status(500).json({ error: 'Insert failed' });
        res.json({ message: `${product_name} added successfully!` });
      });
    }
  });
});


app.post('/login', (req, res) => {
  const { username } = req.body;
  if (!username) return res.status(400).json({ error: 'Username is required' });

  // Create a new session ID for each login explicitly
  req.session.regenerate(err => {
    if (err) return res.status(500).json({ error: 'Session regeneration failed' });
    req.session.user = { username };
    res.json({ message: `Welcome ${username}`, sessionId: req.sessionID });
  });
});


app.post('/order', (req, res) => {
  // 1️ Check login session
  if (!req.session.user) {
    return res.status(401).json({ error: 'Login required' });
  }

  const { product_name, order_count } = req.body;

  if (!product_name || !order_count) {
    return res.status(400).json({ error: 'Product name and order count are required' });
  }

  // 2️ Find the product
  const selectQuery = 'SELECT * FROM product WHERE product_name = ?';
  db.query(selectQuery, [product_name], (err, results) => {
    if (err) return res.status(500).json({ error: 'Database error' });
    if (results.length === 0) return res.status(404).json({ error: 'Product not found' });

    const product = results[0];

    // 3️ Check stock availability
    if (product.product_count < order_count) {
      return res.status(400).json({ error: 'Not enough stock available' });
    }

    // 4️ Deduct stock
    const updateQuery = 'UPDATE product SET product_count = product_count - ? WHERE product_name = ?';
    db.query(updateQuery, [order_count, product_name], (err2) => {
      if (err2) return res.status(500).json({ error: 'Failed to update stock' });

      // 5️ Record the order in booking table
      const insertBooking = `
        INSERT INTO booking (product_id, username, product_name, product_count, order_date)
        VALUES (?, ?, ?, ?, NOW())
      `;
      db.query(insertBooking, [product.product_id, req.session.user.username, product_name, order_count], (err3) => {
        if (err3) return res.status(500).json({ error: 'Failed to record order' });

        res.json({
          message: ` Order placed by ${req.session.user.username} for ${order_count} ${product_name}(s)!`
        });
      });
    });
  });
});


app.delete('/product/:name', (req, res) => {
  const { name } = req.params;

  const deleteQuery = 'DELETE FROM product WHERE product_name = ?';
  db.query(deleteQuery, [name], (err, result) => {
    if (err) {
      return res.status(500).json({ error: 'Database error while deleting' });
    }

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }

    res.json({ message: `${name} deleted successfully!` });
  });
});


app.post('/logout', (req, res) => {
  if (req.session.user) {
    const username = req.session.user.username; // keep username for message
    req.session.destroy(err => {
      if (err) {
        return res.status(500).json({ error: 'Failed to logout user' });
      }
      res.clearCookie('session_cookie_name'); // remove cookie from browser/Postman
      res.json({ message: `User ${username} logged out successfully!` });
    });
  } else {
    res.status(400).json({ message: 'No active session to logout' });
  }
});




const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(` Server is running on port ${PORT}`);
});
