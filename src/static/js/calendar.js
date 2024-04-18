document.addEventListener('DOMContentLoaded', function () {
    const selectDateButton = document.getElementById('selectDateButton');

    // Обработчик события для кнопки "Выбрать"
    selectDateButton.addEventListener('click', function () {
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        // Проверяем, чтобы выбраны были обе даты
        if (startDate && endDate) {
            // Проверяем, чтобы конечная дата была позже начальной даты
            if (startDate <= endDate) {
                const houseId = document.getElementById('house_id').value; // Получаем house_id из скрытого поля
                // Переходим на страницу booking_confirmation.html с передачей параметров
                window.location.href = `/booking_confirmation?house_id=${houseId}&start_date=${startDate}&end_date=${endDate}`;
            } else {
                alert('Конечная дата должна быть позже начальной даты');
            }
        } else {
            alert('Пожалуйста, выберите начальную и конечную даты');
        }
    });
});