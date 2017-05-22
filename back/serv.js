var http = require("http");
var url = require("url");

var server = http.createServer(function(req, res) {
	var link = url.parse(req["url"], true);
	var r = "{}";
	if (link["pathname"] == "/findRecipes") {
		var recipeUrl = link["query"]["url"];
		console.log("Scraping " + recipeUrl);
		var child = require("child_process");
		var scraper = child.spawn("python3", ["./scraper/allRecipes.py", recipeUrl]);
		var scraped = "";
		scraper.stdout.on("data", function(data) {
			scraped = scraped + data.toString();
		});
		scraper.stdout.on("end", function() {
			scraped = JSON.parse(scraped);
			var query = require("./db/query");
			query.mergeAndSearch(scraped, function (err, data) {
				res.writeHead(200, {"Content-Type": "application/json"});
				res.end(JSON.stringify(data));
				console.log(JSON.stringify(data));
			});
		});
	}
});

server.listen(1337);
