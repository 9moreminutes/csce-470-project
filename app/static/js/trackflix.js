$("#searchButton").on("click", function(e) {
	e.preventDefault();
	$.ajax({
		type: "GET",
		url: "/search",
		data: $("#searchForm").serialize()
	})
	.done(function(html) {
		// first we clear out anything in the results section
		$(".search-results").empty();
		// next we add in the html from the search call
		$(".search-results").append(html);
	});
});