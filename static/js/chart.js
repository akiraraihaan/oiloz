/**
 * D3.js Chart Rendering
 * Creates comparison charts for Oil and Water production
 */

function drawComparisonChart(containerId, title, actualValue, optimalValue, unit) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Clear previous chart
    container.innerHTML = '';

    // Data with teal/mint colors
    const data = [
        { label: 'Actual', value: actualValue, color: '#0f766e' }, // Dark teal
        { label: 'Optimal', value: optimalValue, color: '#14b8a6' } // Teal
    ];

    const maxValue = Math.max(actualValue, optimalValue) * 1.2;

    // SVG dimensions
    const margin = { top: 20, right: 20, bottom: 30, left: 60 };
    const width = 300 - margin.left - margin.right;
    const height = 250 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('class', 'd3-chart')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    // Create defs for gradients
    const defs = svg.append('defs');
    
    // Gradient 1 - Muted Teal with reduced opacity
    const grad1 = defs.append('linearGradient')
        .attr('id', `gradient-actual`)
        .attr('x1', '0%').attr('x2', '100%')
        .attr('y1', '0%').attr('y2', '100%');
    
    grad1.append('stop').attr('offset', '0%').attr('stop-color', '#5b9f99').attr('stop-opacity', 0.6);
    grad1.append('stop').attr('offset', '25%').attr('stop-color', '#5b9f99').attr('stop-opacity', 0.6);
    grad1.append('stop').attr('offset', '25%').attr('stop-color', '#7fb3b0').attr('stop-opacity', 0.5);
    grad1.append('stop').attr('offset', '50%').attr('stop-color', '#7fb3b0').attr('stop-opacity', 0.5);
    grad1.append('stop').attr('offset', '50%').attr('stop-color', '#5b9f99').attr('stop-opacity', 0.6);
    grad1.append('stop').attr('offset', '75%').attr('stop-color', '#5b9f99').attr('stop-opacity', 0.6);
    grad1.append('stop').attr('offset', '75%').attr('stop-color', '#7fb3b0').attr('stop-opacity', 0.5);
    grad1.append('stop').attr('offset', '100%').attr('stop-color', '#7fb3b0').attr('stop-opacity', 0.5);

    // Gradient 2 - Muted Mint with reduced opacity
    const grad2 = defs.append('linearGradient')
        .attr('id', `gradient-optimal`)
        .attr('x1', '0%').attr('x2', '100%')
        .attr('y1', '0%').attr('y2', '100%');
    
    grad2.append('stop').attr('offset', '0%').attr('stop-color', '#6db8b0').attr('stop-opacity', 0.6);
    grad2.append('stop').attr('offset', '25%').attr('stop-color', '#6db8b0').attr('stop-opacity', 0.6);
    grad2.append('stop').attr('offset', '25%').attr('stop-color', '#9fcdc6').attr('stop-opacity', 0.5);
    grad2.append('stop').attr('offset', '50%').attr('stop-color', '#9fcdc6').attr('stop-opacity', 0.5);
    grad2.append('stop').attr('offset', '50%').attr('stop-color', '#6db8b0').attr('stop-opacity', 0.6);
    grad2.append('stop').attr('offset', '75%').attr('stop-color', '#6db8b0').attr('stop-opacity', 0.6);
    grad2.append('stop').attr('offset', '75%').attr('stop-color', '#9fcdc6').attr('stop-opacity', 0.5);
    grad2.append('stop').attr('offset', '100%').attr('stop-color', '#9fcdc6').attr('stop-opacity', 0.5);

    const chartGroup = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, width])
        .padding(0.4);

    const yScale = d3.scaleLinear()
        .domain([0, maxValue])
        .range([height, 0]);

    const barRadius = xScale.bandwidth() / 2.5;

    // Bars dengan gradient
    chartGroup.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.label))
        .attr('y', d => yScale(d.value))
        .attr('width', xScale.bandwidth())
        .attr('height', d => height - yScale(d.value))
        .attr('rx', barRadius)
        .attr('ry', barRadius)
        .attr('fill', (d, i) => {
            return i === 0 ? 'url(#gradient-actual)' : 'url(#gradient-optimal)';
        });

    // Value labels on bars
    chartGroup.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('x', d => xScale(d.label) + xScale.bandwidth() / 2)
        .attr('y', d => yScale(d.value) - 8)
        .attr('text-anchor', 'middle')
        .attr('font-weight', '600')
        .attr('font-size', '13px')
        .attr('fill', '#1f2937')
        .text(d => `${d.value.toFixed(2)} ${unit}`);

    // Y-axis styling
    const yAxis = d3.axisLeft(yScale)
        .tickSize(-width)
        .tickFormat(d => d);
    
    chartGroup.append('g')
        .attr('class', 'axis y-axis')
        .call(yAxis);

    // X-axis
    const xAxis = d3.axisBottom(xScale);
    chartGroup.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    // Title
    chartGroup.append('text')
        .attr('x', width / 2)
        .attr('y', -5)
        .attr('text-anchor', 'middle')
        .attr('font-size', '14px')
        .attr('font-weight', '600')
        .attr('fill', '#1f2937')
        .text(title + ` (${unit})`);

    // Y-axis label
    chartGroup.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', '#6b7280')
        .text(unit);
}

/**
 * Time Series Chart with D3
 * Shows production over multiple days
 */
function drawTimeSeriesChart(containerId, title, dates, actualValues, optimalValues) {
    const container = document.getElementById(containerId);
    if (!container || dates.length === 0) return;

    container.innerHTML = '';

    const data = dates.map((date, i) => ({
        date: new Date(date),
        actual: actualValues[i],
        optimal: optimalValues[i]
    }));

    const margin = { top: 20, right: 30, bottom: 30, left: 60 };
    const width = 800 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('class', 'd3-chart')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const xScale = d3.scaleTime()
        .domain(d3.extent(data, d => d.date))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => Math.max(d.actual, d.optimal)) * 1.1])
        .range([height, 0]);

    const lineActual = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.actual));

    const lineOptimal = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.optimal));

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale)
            .tickSize(-height)
            .tickFormat('')
        );

    // Lines
    svg.append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', '#3B82F6')
        .attr('stroke-width', 2)
        .attr('d', lineActual);

    svg.append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', '#10B981')
        .attr('stroke-width', 2)
        .attr('stroke-dasharray', '5,5')
        .attr('d', lineOptimal);

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(yScale));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale));

    // Title
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', -5)
        .attr('text-anchor', 'middle')
        .attr('font-weight', 'bold')
        .attr('fill', '#333')
        .text(title);

    // Legend
    const legend = svg.append('g')
        .attr('transform', `translate(${width - 150}, 0)`);

    legend.append('rect')
        .attr('width', 150)
        .attr('height', 60)
        .attr('fill', 'white')
        .attr('stroke', '#ddd');

    legend.append('line')
        .attr('x1', 10).attr('y1', 15)
        .attr('x2', 30).attr('y2', 15)
        .attr('stroke', '#3B82F6')
        .attr('stroke-width', 2);

    legend.append('text')
        .attr('x', 40).attr('y', 20)
        .attr('font-size', '12px')
        .text('Actual');

    legend.append('line')
        .attr('x1', 10).attr('y1', 40)
        .attr('x2', 30).attr('y2', 40)
        .attr('stroke', '#10B981')
        .attr('stroke-width', 2)
        .attr('stroke-dasharray', '5,5');

    legend.append('text')
        .attr('x', 40).attr('y', 45)
        .attr('font-size', '12px')
        .text('Optimal');
}
