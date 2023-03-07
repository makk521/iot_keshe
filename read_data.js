const sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('C:/Users/ASUS/Desktop/iot_keshe/data.db', (err) => {
    if (err) {
      return console.error(err.message);
    }
    console.log('Connected to the in-memory SQlite database.');
  });



let sql = `SELECT led_status FROM data `;

db.all(sql, [], (err, rows) => {
  if (err) {
    throw err;
  }
  rows.forEach((row) => {
    console.log(row);
  });
});
