document.addEventListener('DOMContentLoaded', function () {
    const selectDateButton = document.getElementById('selectDateButton');

    // Обработчик события для кнопки "Выбрать"
    selectDateButton.addEventListener('click', function () {
        // Получаем значение поля ввода с идентификатором 'airdatepicker'
        const calendarInput = document.getElementById('airdatepicker').value;
        
        // Разделяем строку на две части по ', '
        const dates = calendarInput.split(', ');

        // Получаем отдельные части массива
        const startDate = dates[0];
        const endDate = dates[1];
        
        // Получаем значение поля ввода с идентификатором 'house_id'
        const houseId = document.getElementById('house_id').value;

        // Переходим на страницу booking_confirmation.html с передачей параметров
        window.location.href = `/booking_confirmation?house_id=${houseId}&start_date=${startDate}&end_date=${endDate}`;
    });
});