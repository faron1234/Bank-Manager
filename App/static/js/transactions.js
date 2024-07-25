// App/static/js/transactions.js

export function searchTransactions(query) {
    $.ajax({
        url: searchTransactionsUrl, // Ensure this variable is set in your HTML
        method: "GET",
        data: { query: query },
        success: function(response) {
            $('#transactions-body').html(response.transactions);
            $('#stats-container').html(response.stats);
        },
        error: function(xhr, status, error) {
            alert("Error searching transactions: " + error);
        }
    });
}
