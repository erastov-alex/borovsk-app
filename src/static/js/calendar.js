selectDateButton.addEventListener('click', function () {
    const calendarInput = document.getElementById('airdatepicker').value;
    console.log(calendarInput)

    if (!calendarInput) {
        alert("Выберите даты");
        return;
    }

    const dates = calendarInput.split(', ');
    if (dates.length !== 2) {
        alert("Выберите даты");
        return;
    }

    const houseId = document.getElementById('house_id').value;

    const startDate = new Date(dates[0]);
    const endDate = new Date(dates[1]);

    if (!(startDate instanceof Date && endDate instanceof Date) || isNaN(startDate) || isNaN(endDate)) {
        alert("Выберите даты");
        return;
    }

    const datesBetween = [];
    let currentDate = startDate;
    while (currentDate <= endDate) {
        datesBetween.push(currentDate.toISOString().slice(0, 10)); // YYYY-MM-DD format
        currentDate.setDate(currentDate.getDate() + 1);
    }

    if (datesBetween.some(date => unavailableDates.includes(date))) {
        alert("К сожалению, выбранные даты заняты. Пожалуйста, выберите свободные даты");
    } else {
        // proceed with booking
        const formattedStartDate = dates[0];
        const formattedEndDate = dates[1];
        window.location.href = `/booking_confirmation?house_id=${houseId}&start_date=${formattedStartDate}&end_date=${formattedEndDate}`;
    }
});