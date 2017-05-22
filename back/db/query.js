var exports = module.exports = {};

exports.mergeAndSearch = function(recipe, callback) {
	var q1 = "MERGE (a:Recipe {name: \"" + recipe.recipe + "\", url: \"" + recipe.url + "\"}) FOREACH (x in " + JSON.stringify(recipe.ingredients) + " | MERGE (i:Ingredient {name: x}) MERGE (a)-[:Contains]->(i)) RETURN null";
	var q2 = "MATCH (a:Recipe {name: \"" + recipe.recipe + "\", url: \"" + recipe.url + "\"})-[:Contains]-(:Ingredient)-[:Contains]-(b:Recipe) RETURN DISTINCT b";
	var request = require("request");
	var reqBody = 
		{ "json": {"statements": [
			{ "statement" : q1 },
			{ "statement" : q2 }
		] }};
	console.log(q1);
	console.log(q2);
	request.post("http://localhost:7474/db/data/transaction/commit",
		reqBody, function(err, res, body) {
			if (!err && res.statusCode == 200) {
				var nodes = [];
				for (r of body.results[1].data) {
					nodes.push(r.row[0]);
				}
				callback(null, {"nodes": nodes});
			} else {
				callback(err, res.statusCode);
			}
		}).auth("neo4j", "", false);
}
