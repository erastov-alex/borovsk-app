document.addEventListener('DOMContentLoaded', function () {
    const selectHouseButtons = document.querySelectorAll('.select-house-btn');

    selectHouseButtons.forEach(button => {
        button.addEventListener('click', function () {
            const houseId = button.getAttribute('data-house-id');
            window.location.href = `/calendar?house_id=${houseId}`;
        });
    });
});

