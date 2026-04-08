document.addEventListener('DOMContentLoaded', () => {
    const tempSlider = document.getElementById('sim-temp');
    const tempVal = document.getElementById('temp-val');
    const crSlider = document.getElementById('sim-c-rate');
    const crVal = document.getElementById('cr-val');
    const socSlider = document.getElementById('sim-soc');
    const socVal = document.getElementById('soc-val');
    
    // Update labels
    tempSlider.addEventListener('input', (e) => tempVal.textContent = e.target.value + '°C');
    crSlider.addEventListener('input', (e) => crVal.textContent = e.target.value + 'C');
    socSlider.addEventListener('input', (e) => socVal.textContent = e.target.value + '%');

    // Chart.js Setup
    const ctx = document.getElementById('capacityChart').getContext('2d');
    
    // Gradient for chart
    let gradientArea = ctx.createLinearGradient(0, 0, 0, 400);
    gradientArea.addColorStop(0, 'rgba(0, 229, 255, 0.5)');
    gradientArea.addColorStop(1, 'rgba(0, 229, 255, 0)');

    const chartData = {
        labels: ['0', '200', '400', '600', '800', '1000', '1200', '1400', '1600'],
        datasets: [{
            label: 'AI Optimized Strategy',
            data: [100, 98, 95.5, 93, 89, 86, 84, 82, 80],
            borderColor: '#00e5ff',
            backgroundColor: gradientArea,
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#00e5ff'
        }, {
            label: 'Baseline CC-CV',
            data: [100, 95, 89, 82, 75, 68, 62, 55, 50],
            borderColor: '#ff3366',
            borderWidth: 2,
            borderDash: [5, 5],
            tension: 0.4,
            fill: false,
            pointBackgroundColor: '#ff3366'
        }]
    };

    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#e2e8f0' } }
            },
            scales: {
                y: {
                    min: 40,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Capacity Retention (%)', color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Cycles', color: '#94a3b8' }
                }
            }
        }
    };

    let capacityChart = new Chart(ctx, config);

    // Simulate Experiment Run
    const runBtn = document.getElementById('run-sim-btn');
    runBtn.addEventListener('click', () => {
        runBtn.innerHTML = 'Simulating... <span style="animation: pulse 1s infinite">⚡</span>';
        runBtn.style.opacity = '0.8';
        
        // Randomize some metric values to make it look active
        setTimeout(() => {
            document.getElementById('metric-soh').textContent = (98 + Math.random() * 1.5).toFixed(1) + '%';
            document.getElementById('metric-speed').textContent = Math.floor(35 + Math.random() * 10) + ' min';
            let cycles = Math.floor(1300 + Math.random() * 300);
            document.getElementById('metric-cycles').textContent = cycles;
            
            // Jitter the chart data slightly to show new results
            let newData = chartData.datasets[0].data.map(val => val + (Math.random() * 2 - 1));
            newData[0] = 100; // start at 100
            capacityChart.data.datasets[0].data = newData;
            capacityChart.update();

            runBtn.innerHTML = 'Execute AI Simulation';
            runBtn.style.opacity = '1';

            // change active row in history
            const historyBody = document.getElementById('history-body');
            const newRow = document.createElement('tr');
            newRow.className = 'active-row';
            newRow.innerHTML = "<td>#EXP-807</td><td class='text-cyan'>Bayesian Optimal</td><td>" + 
                document.getElementById('sim-c-rate').value + "C</td><td>" + 
                document.getElementById('sim-temp').value + "°C</td><td>" + 
                (Math.random() > 0.5 ? '96/100' : '94/100') + 
                "</td><td><span class='badge badge-success'>Done</span></td>";
            
            // remove last child and insert new
            historyBody.insertBefore(newRow, historyBody.firstChild);
            if(historyBody.children.length > 5) {
                historyBody.removeChild(historyBody.lastChild);
            }
        }, 1500);
    });
});
