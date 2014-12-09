$("#searchButton").on("click", function(e) {
        e.preventDefault();
        searchTerm = $("#searchForm")[0].value
        $.ajax({
                type: "GET",
                url: "/trackflix/search?q="+searchTerm,
        })
        .done(function(html) {
                // first we clear out anything in the results section
                $(".search-results").empty();
                // next we add in the html from the search call
                $(".search-results").append(html);
        });
});
$('#searchButton').keypress(function(e) {
    e.preventDefault();
    if (e.which == '13') {
         searchTerm = $("#searchForm")[0].value
         $.ajax({
                type: "GET",
                url: "/trackflix/search?q="+searchTerm,
         })
         .done(function(html) {
                // first we clear out anything in the results section
                $(".search-results").empty();
                // next we add in the html from the search call
                $(".search-results").append(html);
         });
    }
});