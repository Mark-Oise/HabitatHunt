/**
 * Clears all filters in the leads filter form
 * Resets both checkboxes and number input fields
 */
function clearAllFilters() {
    // Clear all checkboxes in the filter form
    const filterForm = document.querySelector('#accordion-flush form');
    if (filterForm) {
        // Clear checkboxes
        const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

        // Clear number inputs (for sentiment and engagement scores)
        const numberInputs = filterForm.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.value = '';
        });
    }
}
