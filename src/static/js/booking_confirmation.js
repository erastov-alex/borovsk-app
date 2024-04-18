document.addEventListener('DOMContentLoaded', function () {
    const confirmationSection = document.getElementById('confirmation');
    const backButtonConfirmation = document.getElementById('backButtonConfirmation');
    const bookingForm = document.getElementById('booking-form');
    let selectedHouseId = null;

    // Получаем параметры бронирования из URL
    const urlParams = new URLSearchParams(window.location.search);
    const houseId = urlParams.get('house_id');
    const startDate = urlParams.get('start_date');
    const endDate = urlParams.get('end_date');

    // Убеждаемся, что все необходимые элементы присутствуют на странице
    if (confirmationSection && backButtonConfirmation && bookingForm) {
        // Отображаем информацию о бронировании на странице
        const bookingInfoParagraph = document.getElementById('booking-info');
        bookingInfoParagraph.textContent = `Вы выбрали дом с ID ${houseId} c ${startDate} по ${endDate}`;

        // Устанавливаем значения для скрытых полей в форме
        const houseIdInput = document.getElementById('house_id');
        const startDateInput = document.getElementById('start_date_input');
        const endDateInput = document.getElementById('end_date_input');
        if (houseIdInput && startDateInput && endDateInput) {
            houseIdInput.value = houseId;
            startDateInput.value = startDate;
            endDateInput.value = endDate;
        }

        // Создаем случайную величину для итоговой стоимости (пока без реальных вычислений)
        const totalCost = Math.floor(Math.random() * 1000) + 500; // Пример случайной величины от 500 до 1500
        const totalCostParagraph = document.getElementById('total-cost-info');
        if (totalCostParagraph) {
            totalCostParagraph.textContent = `Итоговая стоимость: $${totalCost}`;
        }

        backButtonConfirmation.addEventListener('click', function () {
            // Переход на страницу /calendar с параметром house_id
            window.location.href = '/calendar?house_id=' + houseId;
        });

        bookingForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Создаем объект с данными формы
            const formData = {
                house_id: houseIdInput.value,
                start_date: startDateInput.value,
                end_date: endDateInput.value
            };

            console.log('Form data:', formData); // Добавим вывод данных формы в консоль для отладки

            // Отправляем данные на сервер в формате JSON
            fetch('/booking_confirmation', {
                method: 'POST',
                body: new FormData(bookingForm),
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response from server:', data);
                // Скрываем блок с подтверждением бронирования
                confirmationSection.style.display = 'none';
                // Показываем сообщение о подтверждении бронирования и кнопку "Личный кабинет"
                document.getElementById('confirmation2').style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
