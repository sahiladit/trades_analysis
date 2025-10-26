let alertAlreadyShown = false;

function fetchAnalytics() {
    fetch('/api/analytics')
        .then(response => response.json())
        .then(data => {
            if (!data.sym1 || !data.sym2) {
                document.getElementById('analytics-data').innerHTML = '<p style="color:#ccc;">Waiting for sufficient data...</p>';
                Plotly.purge('price-plot');
                Plotly.purge('spread-plot');
                return;
            }

            const alertThresholdInput = document.getElementById('zscoreThreshold');
            const alertThreshold = alertThresholdInput ? parseFloat(alertThresholdInput.value) : 2;
            const zScoreVal = data.z_score;

            // Show alert popup once when threshold crossed
            if (Math.abs(zScoreVal) > alertThreshold) {
                if (!alertAlreadyShown) {
                    alert(`Z-Score Alert! Value (${zScoreVal.toFixed(4)}) has exceeded your threshold of ${alertThreshold}`);
                    alertAlreadyShown = true;
                }
            } else {
                alertAlreadyShown = false; // reset alert trigger
            }

            let statsHtml = `
                <h3>${data.sym1.toUpperCase()} vs ${data.sym2.toUpperCase()}</h3>
                <p><strong>Hedge Ratio (Beta):</strong> ${data.hedge_beta.toFixed(4)}</p>
                <p><strong>Last Spread:</strong> ${data.last_spread.toFixed(4)}</p>
                <p><strong>Z-Score:</strong> <span style="color:${Math.abs(zScoreVal) > alertThreshold ? 'red' : 'limegreen'};">
                    ${zScoreVal.toFixed(4)}</span></p>
                <p><strong>Rolling Correlation:</strong> ${data.rolling_corr.toFixed(4)}</p>
            `;
            document.getElementById('analytics-data').innerHTML = statsHtml;

            Plotly.newPlot('price-plot', [
                {
                    x: [...Array(data.prices1.length).keys()],
                    y: data.prices1,
                    name: data.sym1.toUpperCase(),
                    mode: 'lines',
                    type: 'scatter'
                },
                {
                    x: [...Array(data.prices2.length).keys()],
                    y: data.prices2,
                    name: data.sym2.toUpperCase(),
                    mode: 'lines',
                    type: 'scatter'
                }
            ], {
                title: 'Price Series',
                margin: { t: 30, b: 40 },
                xaxis: { title: 'Tick Number' },
                yaxis: { autorange: true }
            });

            Plotly.newPlot('spread-plot', [
                {
                    x: [...Array(data.spread_list.length).keys()],
                    y: data.spread_list,
                    name: 'Spread',
                    mode: 'lines',
                    type: 'scatter'
                }
            ], {
                title: 'Spread Series',
                margin: { t: 30, b: 40 },
                xaxis: { title: 'Tick Number' },
                yaxis: { autorange: true }
            });
        })
        .catch(err => {
            console.error('Error fetching analytics:', err);
            document.getElementById('analytics-data').innerHTML = '<p style="color:red;">Failed to load analytics data.</p>';
            Plotly.purge('price-plot');
            Plotly.purge('spread-plot');
        });
}
