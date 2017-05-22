var http = require("http");
var url = require("url");

var server = http.createServer(function(req, res) {
	var link = url.parse(req["url"], true);
	console.log(link);
	var r = "{}";
	if (link["pathname"] == "/findRecipes") {
		var recipeUrl = link["query"]["url"];
		console.log("Scraping " + recipeUrl);
		var query = require("./db/query");
		// Do query stuff here after scraping
	}
	res.writeHead(200, {"Content-Type": "application/json"});
	res.end(r);
});

server.listen(1337);
