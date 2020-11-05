var fs = require('fs');
var parse = require('csv-parse');
const http = require('http');
const hostname = 'localhost';
const port = 2998;

var parse = require('csv-parse');

const server = http.createServer((req, res) => {

  let data = []
  req.on('data', chunk => {
    data.push(chunk);
  });

  req.on('end', () => {

    var parser = parse(
      {
        columns: ["Год", "Месяц", "День", "Час", "Минута", "Секунда", "Hs", "Tz"],
        delimiter: " "
      }, function (err, records) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(records[records.length-1]));
    });

    fs.createReadStream('D:/FTPROOT/wavenergy/buoy/res.txt').pipe(parser);
  })
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
