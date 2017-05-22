var exports = module.exports = {};

exports.mergeAndSearch = function(recipe) {
	var q1 = "MERGE (a:Recipe {name: \"" + recipe.name + "\", url: \"" + recipe.url + "\"}) FOREACH (x in " + JSON.stringify(recipe.ingredients) + " | MERGE (i:Ingredient {name: x}) MERGE (a)-[:Contains]->(i)) RETURN null";
	var q2 = "MATCH (a:Recipe {name: \"" + recipe.name + "\", url: \"" + recipe.url + "\"})-[:Contains]-(:Ingredient)-[:Contains]-(b:Recipe), (a)-[:Contains]->(ia:Ingredient), (b)-[:Contains]->(ib:Ingredient) RETURN b";
	var request = require("request");
	var reqBody = 
		{ "json": {"statements": [
			{ "statement" : q1 },
			{ "statement" : q2 }
		] }};
	console.log(reqBody);
	request.post("http://localhost:7474/db/data/transaction/commit",
		reqBody, function(err, res, body) {
			if (!err && res.statusCode == 200) {
				return(body.results);
			}
		}).auth("neo4j", "", false);
	return null;
}
