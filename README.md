<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clash Royale Bot - An AI-Powered Player</title>
    <!--
        Infographic Plan:
        1.  **Header:** Introduce the project.
        2.  **Section 1: The Core Loop:** A flow chart showing the bot's main operational cycle (Capture -> Analyze -> Decide -> Act).
        3.  **Section 2: The Vision System:** Detail the visual detection process, including key stats, a breakdown of loaded templates, and a diagram of the detection ROIs.
        4.  **Section 3: The Detection Pipeline:** A sub-flowchart showing the steps from raw screenshot to identified object using template matching.
        5.  **Section 4: The Strategy Engine:** Visualize the bot's decision-making logic, including its placement strategy and a conceptual counter map.
        6.  **Section 5: Performance Snapshot:** Display hypothetical performance metrics using line and radar charts to summarize the bot's effectiveness.

        Visualization Choices:
        -   **Core Loop (Flow Chart):** Goal: Organize. Method: HTML/CSS with Tailwind. Justification: Clearly shows a cyclical process. NO SVG/Mermaid.
        -   **Template Breakdown (Donut Chart):** Goal: Compare. Library: Chart.js. Justification: Ideal for showing part-to-whole composition of loaded templates.
        -   **ROI Diagram:** Goal: Organize. Method: HTML/CSS with Tailwind. Justification: A custom diagram is best for illustrating specific screen regions. NO SVG/Mermaid.
        -   **Detection Pipeline (Flow Chart):** Goal: Organize. Method: HTML/CSS with Tailwind. Justification: Details a linear sub-process effectively. NO SVG/Mermaid.
        -   **Placement Positions (Bar Chart):** Goal: Compare. Library: Chart.js. Justification: Simple comparison of two categories (Offensive vs. Defensive).
        -   **Counter Map (Relationship Diagram):** Goal: Relationships. Method: HTML/CSS with Tailwind. Justification: Clearly shows the relationship between enemy units and counter types. NO SVG/Mermaid.
        -   **Detection Confidence (Line Chart):** Goal: Change. Library: Chart.js. Justification: Perfect for showing a trend over time.
        -   **Bot Performance (Radar Chart):** Goal: Compare. Library: Chart.js. Justification: Excellent for comparing multiple performance metrics on a single entity.

        Color Palette Chosen: "Energetic & Playful"
        -   #FF6B6B (red/pink)
        -   #FFD166 (yellow)
        -   #06D6A0 (green)
        -   #118AB2 (blue)
        -   #073B4C (dark blue/black)

        Confirmation: NEITHER Mermaid JS NOR SVG were used in this output. All charts are rendered on Canvas by Chart.js, and all diagrams are built with structured HTML and Tailwind CSS.
    -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 300px;
            max-height: 400px;
        }
        @media (min-width: 768px) {
            .chart-container {
                height: 350px;
            }
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800">

    <div class="container mx-auto p-4 md:p-8 max-w-5xl">
        
        <header class="text-center my-12">
            <h1 class="text-4xl md:text-6xl font-black text-[#073B4C]">Clash Royale Bot</h1>
            <p class="text-xl md:text-2xl text-[#118AB2] mt-2">An AI-Powered Player, Visualized</p>
        </header>

        <main class="grid grid-cols-1 md:grid-cols-2 gap-8">

            <section id="core-loop" class="md:col-span-2 bg-white rounded-2xl shadow-lg p-6">
                <h2 class="text-2xl font-bold text-[#073B4C] mb-4">The Core Loop: How the Bot Thinks</h2>
                <p class="text-slate-600 mb-6">The bot operates in a continuous cycle, perceiving the game, making a decision, and executing an action. This loop runs every few seconds, allowing the bot to react to the changing battlefield in real-time.</p>
                <div class="flex flex-col md:flex-row items-center justify-around space-y-4 md:space-y-0 md:space-x-4 text-center">
                    <div class="flex flex-col items-center">
                        <div class="bg-[#118AB2] text-white w-24 h-24 rounded-full flex items-center justify-center font-bold text-lg shadow-md">Capture</div>
                        <p class="text-sm mt-2 text-slate-500">ADB Screenshot</p>
                    </div>
                    <div class="text-4xl font-bold text-[#FFD166] self-center md:rotate-0 rotate-90">&rarr;</div>
                    <div class="flex flex-col items-center">
                        <div class="bg-[#06D6A0] text-white w-24 h-24 rounded-full flex items-center justify-center font-bold text-lg shadow-md">Analyze</div>
                        <p class="text-sm mt-2 text-slate-500">Vision System</p>
                    </div>
                    <div class="text-4xl font-bold text-[#FFD166] self-center md:rotate-0 rotate-90">&rarr;</div>
                    <div class="flex flex-col items-center">
                        <div class="bg-[#FF6B6B] text-white w-24 h-24 rounded-full flex items-center justify-center font-bold text-lg shadow-md">Decide</div>
                        <p class="text-sm mt-2 text-slate-500">Strategy Engine</p>
                    </div>
                    <div class="text-4xl font-bold text-[#FFD166] self-center md:rotate-0 rotate-90">&rarr;</div>
                    <div class="flex flex-col items-center">
                        <div class="bg-[#073B4C] text-white w-24 h-24 rounded-full flex items-center justify-center font-bold text-lg shadow-md">Act</div>
                        <p class="text-sm mt-2 text-slate-500">Emulator Control</p>
                    </div>
                </div>
            </section>

            <section id="vision-system" class="md:col-span-2 bg-white rounded-2xl shadow-lg p-6">
                <h2 class="text-2xl font-bold text-[#073B4C] mb-4">The Eyes: Vision System Deep Dive</h2>
                <p class="text-slate-600 mb-8">The Vision System is the bot's perception layer. It analyzes screenshots to identify game state, cards, and enemy units using a library of pre-defined image templates.</p>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                    <div class="lg:col-span-1 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-1 gap-4 text-center">
                        <div class="bg-slate-100 p-4 rounded-lg">
                            <div class="text-4xl font-black text-[#118AB2]">159</div>
                            <p class="text-sm text-slate-500">Card Templates</p>
                        </div>
                        <div class="bg-slate-100 p-4 rounded-lg">
                            <div class="text-4xl font-black text-[#06D6A0]">11</div>
                            <p class="text-sm text-slate-500">Enemy Templates</p>
                        </div>
                        <div class="bg-slate-100 p-4 rounded-lg col-span-2 sm:col-span-1 lg:col-span-1">
                             <div class="chart-container !h-32">
                                <canvas id="uiTemplatesChart"></canvas>
                            </div>
                            <p class="text-sm text-slate-500 mt-2">UI Templates Loaded</p>
                        </div>
                    </div>
                    <div class="lg:col-span-2">
                        <h3 class="text-lg font-bold text-[#073B4C] mb-2 text-center">Regions of Interest (ROIs)</h3>
                        <div class="bg-slate-800 rounded-lg p-4 w-full max-w-sm mx-auto aspect-[9/16] relative flex flex-col justify-between">
                            <div class="text-white/50 text-center text-xs">Screen Top</div>
                             <div class="absolute border-2 border-dashed border-[#FF6B6B]/70 bg-[#FF6B6B]/10" style="top: 11.7%; left: 0%; width: 100%; height: 66.4%;">
                                <span class="absolute top-1 left-1 text-xs text-white/90 bg-[#FF6B6B]/50 px-1 rounded">battlefield_roi</span>
                            </div>
                             <div class="absolute border-2 border-dashed border-orange-400/70 bg-orange-400/10" style="top: 11.7%; left: 0%; width: 100%; height: 37.7%;">
                                <span class="absolute bottom-1 right-1 text-xs text-white/90 bg-orange-400/50 px-1 rounded">enemy_field_roi</span>
                            </div>
                            <div class="absolute border-2 border-dashed border-[#FFD166]/70 bg-[#FFD166]/10" style="bottom: 3.9%; left: 6.9%; width: 86.2%; height: 14.1%;">
                                <span class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-xs text-white/90 bg-[#FFD166]/50 px-1 rounded">hand_roi</span>
                            </div>
                            <div class="text-white/50 text-center text-xs">Screen Bottom</div>
                        </div>
                    </div>
                </div>
            </section>
            
            <section id="detection-pipeline" class="bg-white rounded-2xl shadow-lg p-6">
                <h2 class="text-2xl font-bold text-[#073B4C] mb-4">Detection Pipeline</h2>
                <p class="text-slate-600 mb-6">Each screenshot undergoes a multi-step process to extract meaningful data.</p>
                <ol class="relative border-l border-slate-200 ml-3">                  
                    <li class="mb-6 ml-6">            
                        <span class="absolute flex items-center justify-center w-6 h-6 bg-[#118AB2] rounded-full -left-3 ring-8 ring-white"></span>
                        <h3 class="font-semibold text-slate-900">Raw Screenshot</h3>
                        <p class="text-sm text-slate-500">From ADB Capture</p>
                    </li>
                    <li class="mb-6 ml-6">
                        <span class="absolute flex items-center justify-center w-6 h-6 bg-[#06D6A0] rounded-full -left-3 ring-8 ring-white"></span>
                        <h3 class="font-semibold text-slate-900">Preprocess</h3>
                        <p class="text-sm text-slate-500">Grayscale & Blur Image</p>
                    </li>
                    <li class="mb-6 ml-6">
                        <span class="absolute flex items-center justify-center w-6 h-6 bg-[#FFD166] rounded-full -left-3 ring-8 ring-white"></span>
                        <h3 class="font-semibold text-slate-900">Template Matching</h3>
                        <p class="text-sm text-slate-500">Finds template in image</p>
                    </li>
                    <li class="ml-6">
                        <span class="absolute flex items-center justify-center w-6 h-6 bg-[#FF6B6B] rounded-full -left-3 ring-8 ring-white"></span>
                        <h3 class="font-semibold text-slate-900">Confidence Check</h3>
                        <p class="text-sm text-slate-500">Is match > 85% confident?</p>
                    </li>
                </ol>
            </section>

            <section id="strategy-engine" class="bg-white rounded-2xl shadow-lg p-6">
                 <h2 class="text-2xl font-bold text-[#073B4C] mb-4">The Brain: Strategy Engine</h2>
                <p class="text-slate-600 mb-6">The engine uses vision data to select cards and determine optimal placement.</p>
                <div class="mb-6">
                    <h3 class="font-semibold text-slate-900 mb-2">Defined Placement Positions</h3>
                    <div class="chart-container !h-40">
                        <canvas id="placementChart"></canvas>
                    </div>
                </div>
                <div>
                    <h3 class="font-semibold text-slate-900 mb-3">Conceptual Counter Map</h3>
                    <div class="space-y-3">
                        <div class="flex items-center justify-between bg-slate-100 p-3 rounded-lg">
                            <span class="font-mono text-sm">Enemy: 'Skeleton Army'</span>
                            <span class="text-2xl font-bold text-slate-400 mx-2">&rarr;</span>
                            <span class="font-mono text-sm bg-[#FF6B6B] text-white px-2 py-1 rounded">Counter: 'Splash Damage'</span>
                        </div>
                         <div class="flex items-center justify-between bg-slate-100 p-3 rounded-lg">
                            <span class="font-mono text-sm">Enemy: 'Balloon'</span>
                            <span class="text-2xl font-bold text-slate-400 mx-2">&rarr;</span>
                            <span class="font-mono text-sm bg-[#118AB2] text-white px-2 py-1 rounded">Counter: 'Ranged Anti-Air'</span>
                        </div>
                    </div>
                </div>
            </section>

             <section id="performance" class="md:col-span-2 bg-white rounded-2xl shadow-lg p-6">
                <h2 class="text-2xl font-bold text-[#073B4C] mb-4">Performance Snapshot (Hypothetical)</h2>
                <p class="text-slate-600 mb-8">Metrics illustrate the bot's effectiveness and areas for improvement.</p>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div>
                         <h3 class="font-semibold text-slate-900 mb-2 text-center">Detection Confidence Over Time</h3>
                         <div class="chart-container">
                            <canvas id="confidenceChart"></canvas>
                        </div>
                    </div>
                    <div>
                        <h3 class="font-semibold text-slate-900 mb-2 text-center">Bot Performance Aspects</h3>
                         <div class="chart-container">
                            <canvas id="performanceRadarChart"></canvas>
                        </div>
                    </div>
                </div>
             </section>
        </main>
        
        <footer class="text-center mt-12 py-6 border-t border-slate-200">
            <p class="text-sm text-slate-500">Clash Royale Bot Infographic | Generated 2025</p>
        </footer>

    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const FONT_COLOR = '#334155';
            
            const wrapText = (text, maxLength = 16) => {
                if (text.length <= maxLength) {
                    return text;
                }
                const words = text.split(' ');
                const lines = [];
                let currentLine = '';
                for (const word of words) {
                    if ((currentLine + ' ' + word).length > maxLength) {
                        lines.push(currentLine.trim());
                        currentLine = word;
                    } else {
                        currentLine += ' ' + word;
                    }
                }
                lines.push(currentLine.trim());
                return lines;
            };

            const tooltipTitleCallback = (tooltipItems) => {
                const item = tooltipItems[0];
                let label = item.chart.data.labels[item.dataIndex];
                if (Array.isArray(label)) {
                    return label.join(' ');
                } else {
                    return label;
                }
            };
            
            Chart.defaults.color = FONT_COLOR;
            Chart.defaults.font.family = "'Inter', sans-serif";

            // UI Templates Donut Chart
            const uiTemplatesCtx = document.getElementById('uiTemplatesChart');
            if (uiTemplatesCtx) {
                new Chart(uiTemplatesCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Loaded', 'Missing'],
                        datasets: [{
                            label: 'UI Templates',
                            data: [4, 1],
                            backgroundColor: ['#06D6A0', '#FF6B6B'],
                            borderColor: '#ffffff',
                            borderWidth: 4,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '70%',
                        plugins: {
                            legend: { display: false },
                            tooltip: { callbacks: { title: tooltipTitleCallback } }
                        }
                    }
                });
            }
            
            // Placement Positions Bar Chart
            const placementCtx = document.getElementById('placementChart');
            if(placementCtx) {
                 new Chart(placementCtx, {
                    type: 'bar',
                    data: {
                        labels: ['Defensive Positions', 'Offensive Positions'],
                        datasets: [{
                            label: 'Defined Locations',
                            data: [3, 3],
                            backgroundColor: ['#118AB2', '#FF6B6B'],
                            borderRadius: 4,
                            barPercentage: 0.6,
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: { callbacks: { title: tooltipTitleCallback } }
                        },
                        scales: {
                            x: { grid: { display: false }, ticks: { stepSize: 1 } },
                            y: { grid: { display: false } }
                        }
                    }
                });
            }

            // Detection Confidence Line Chart
            const confidenceCtx = document.getElementById('confidenceChart');
            if(confidenceCtx) {
                 new Chart(confidenceCtx, {
                    type: 'line',
                    data: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        datasets: [{
                            label: 'Card Detection',
                            data: [65, 70, 72, 78, 85, 92],
                            borderColor: '#06D6A0',
                            backgroundColor: 'rgba(6, 214, 160, 0.1)',
                            fill: true,
                            tension: 0.4,
                        }, {
                            label: 'Enemy Detection',
                            data: [50, 55, 62, 68, 75, 81],
                            borderColor: '#FF6B6B',
                            backgroundColor: 'rgba(255, 107, 107, 0.1)',
                            fill: true,
                            tension: 0.4,
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                         plugins: {
                            legend: { position: 'bottom' },
                            tooltip: { callbacks: { title: tooltipTitleCallback } }
                        },
                        scales: { y: { beginAtZero: true, suggestedMax: 100 } }
                    }
                });
            }

            // Performance Radar Chart
            const radarCtx = document.getElementById('performanceRadarChart');
            if(radarCtx) {
                new Chart(radarCtx, {
                    type: 'radar',
                    data: {
                        labels: ['Speed', 'Accuracy', wrapText('Strategy Complexity'), wrapText('Elixir Management'), 'Defense'],
                        datasets: [{
                            label: 'Bot Performance',
                            data: [85, 90, 70, 65, 80],
                            fill: true,
                            backgroundColor: 'rgba(17, 138, 178, 0.2)',
                            borderColor: '#118AB2',
                            pointBackgroundColor: '#118AB2',
                            pointBorderColor: '#fff',
                            pointHoverBackgroundColor: '#fff',
                            pointHoverBorderColor: '#118AB2'
                        }]
                    },
                     options: {
                        responsive: true,
                        maintainAspectRatio: false,
                         plugins: {
                            legend: { display: false },
                            tooltip: { callbacks: { title: tooltipTitleCallback } }
                        },
                        scales: {
                            r: {
                                angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                                suggestedMin: 0,
                                suggestedMax: 100,
                                pointLabels: { font: { size: 12 } }
                            }
                        }
                    }
                });
            }
        });
    </script>
</body>
</html>
