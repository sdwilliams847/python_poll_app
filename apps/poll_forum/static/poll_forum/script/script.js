const CHART = document.getElementById("pieChart");
console.log(CHART);
let lineChart = new Chart(CHART, {
    type: 'pie',
    data: {
        labels: ["option1", "option2", "option3", "option4",],
        datasets: [
            {
                label: 'Points',
                backgroundColor: ['#2980b9','#f1c40f','#e67e22','#16a085'],
                data: [65, 59, 20, 81,],
            }
        ]
    },
    options: {
        animation: {
            animateScale: true
        }
    }

});
