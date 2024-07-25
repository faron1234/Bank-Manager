// App/static/app.js

function showCategoryInput() {
    document.getElementById("new-category-button").style.display = "none";
    document.getElementById("new-category-form").classList.remove("hidden");
}

function submitNewCategory(event) {
    event.preventDefault();
    let category = document.getElementById("new-category-input").value;
    if (!category) return;

    $.ajax({
        url: createCategoryUrl, // Dynamic URL placeholder
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            account: accountName, // Dynamic account name placeholder
            category: category
        }),
        success: function(response) {
            location.reload();
        },
        error: function(response) {
            alert("Error creating category: " + response.responseText);
        }
    });
}

function searchTransactions(query) {
    $.ajax({
        url: searchTransactionsUrl, // Dynamic URL placeholder
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

$(document).ready(function() {
    $('.sortable').click(function() {
        const sortValue = $(this).data('sort');
        let sortDirection = $(this).data('direction');
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('sort_by', sortValue);
        urlParams.set('sort_direction', sortDirection);
        window.location.search = urlParams.toString();
    });

    $('#search-input').on('keyup', function() {
        const query = $(this).val();
        searchTransactions(query);
    });
});
