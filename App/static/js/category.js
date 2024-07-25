// App/static/js/category.js

export function showCategoryInput() {
    document.getElementById("new-category-button").style.display = "none";
    document.getElementById("new-category-form").classList.remove("hidden");
}

export function submitNewCategory(event) {
    event.preventDefault();
    let category = document.getElementById("new-category-input").value;
    if (!category) return;

    $.ajax({
        url: createCategoryUrl, // Ensure this variable is set in your HTML
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            account: accountName, // Ensure this variable is set in your HTML
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
