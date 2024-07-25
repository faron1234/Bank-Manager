// App/static/js/main.js

import { showCategoryInput, submitNewCategory } from './category.js';
import { searchTransactions } from './transactions.js';

$(document).ready(function() {
    // General initialization code
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

window.showCategoryInput = showCategoryInput;
window.submitNewCategory = submitNewCategory;
