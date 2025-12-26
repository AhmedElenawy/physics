document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM Content Loaded - Initializing Superman Flight Simulator');

    const canvas = document.getElementById('simCanvas');
    if (!canvas) {
        console.error('❌ Canvas element not found!');
        return;
    }

    const ctx = canvas.getContext('2d');
    const dataScript = document.getElementById('simulation-data');
    const resultsPanel = document.getElementById('results-panel');

    // Load Superman sprite
    const supermanImg = new Image();
    supermanImg.src = '/static/images/superman_sprite.png';
    let supermanLoaded = false;
    supermanImg.onload = () => {
        supermanLoaded = true;
        console.log('✅ Superman sprite loaded');
    };

    // Check if we are in Practice Mode
    const isPracticeMode = dataScript && dataScript.getAttribute('data-mode') === 'practice';
    if (isPracticeMode) {
        console.log('🛡️ Practice Mode Detected: Spoilers will be hidden');
    }

    // Resize canvas
    function resizeCanvas() {
        const parent = canvas.parentElement;
        if (parent) {
            canvas.width = parent.clientWidth;
            canvas.height = parent.clientHeight || 500;
        }
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    if (!dataScript) return;

    try {
        const physicsData = JSON.parse(dataScript.textContent);
        startSimulation(physicsData);
    } catch (e) {
        console.error('❌ Error parsing data:', e);
    }

    function startSimulation(physicsData) {
        // Show results panel only if NOT in practice mode
        if (resultsPanel && !isPracticeMode) {
            resultsPanel.classList.remove('hidden');
        }

        const trajectory = physicsData.trajectory || [];
        if (trajectory.length === 0) return;

        // Calculate Bounds
        let maxX = 0, maxY = 0;
        trajectory.forEach(p => {
            if (p.x > maxX) maxX = p.x;
            if (p.y > maxY) maxY = p.y;
        });

        // Add padding/margins
        maxX = Math.max(maxX, 10) * 1.1;
        maxY = Math.max(maxY, 10) * 1.2;

        // Update Text Results (Only if NOT practice mode)
        if (!isPracticeMode) {
            const setVal = (id, val) => {
                const el = document.getElementById(id);
                if (el) el.textContent = val.toFixed(2);
            };
            setVal('res-max-height', physicsData.max_height);
            setVal('res-distance', physicsData.range);
            setVal('res-time', physicsData.total_time);
        }

        // Animation Vars
        let startTime = null;
        const animationDuration = 3000;
        const padding = 50;

        // Scaling
        const scaleX = (canvas.width - (padding * 2)) / maxX;
        const scaleY = (canvas.height - (padding * 2)) / maxY;
        const scale = Math.min(scaleX, scaleY);

        function draw(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = (timestamp - startTime) / animationDuration;

            const p = Math.min(progress, 1);

            const currentIndex = Math.floor(p * (trajectory.length - 1));
            drawScene(currentIndex, scale, padding, trajectory, physicsData);

            if (progress < 1) {
                requestAnimationFrame(draw);
            }
        }

        function drawScene(currentIndex, scale, padding, trajectory, physicsData) {
            // Background - White
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            drawGrid(scale, padding, maxX, maxY);
            drawAxes(scale, padding, maxX, maxY);
            drawTrajectoryPath(trajectory, currentIndex, scale, padding);

            if (currentIndex < trajectory.length) {
                const point = trajectory[currentIndex];
                const nextPoint = trajectory[Math.min(currentIndex + 1, trajectory.length - 1)];
                drawSuperman(point, nextPoint, scale, padding);
                drawInfoPanel(point, physicsData);
            }
        }

        function drawGrid(scale, padding, maxX, maxY) {
            ctx.strokeStyle = '#e0e0e0';
            ctx.lineWidth = 0.5;
            ctx.font = '10px Arial';
            ctx.fillStyle = '#888';

            // X Grid
            const stepX = Math.pow(10, Math.floor(Math.log10(maxX)));
            for (let x = 0; x <= maxX; x += stepX) {
                const cx = padding + x * scale;
                ctx.beginPath();
                ctx.moveTo(cx, padding);
                ctx.lineTo(cx, canvas.height - padding);
                ctx.stroke();
                ctx.fillText(x.toFixed(0), cx - 5, canvas.height - padding + 15);
            }

            // Y Grid
            const stepY = Math.pow(10, Math.floor(Math.log10(maxY)));
            for (let y = 0; y <= maxY; y += stepY) {
                const cy = (canvas.height - padding) - y * scale;
                ctx.beginPath();
                ctx.moveTo(padding, cy);
                ctx.lineTo(canvas.width - padding, cy);
                ctx.stroke();
                ctx.fillText(y.toFixed(0), padding - 25, cy + 4);
            }
        }

        function drawAxes(scale, padding, maxX, maxY) {
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.font = 'bold 12px Arial';
            ctx.fillStyle = '#000';

            // Y Axis
            ctx.beginPath();
            ctx.moveTo(padding, padding);
            ctx.lineTo(padding, canvas.height - padding);
            ctx.stroke();
            ctx.fillText('Height (m)', padding - 10, padding - 10);

            // X Axis
            ctx.beginPath();
            ctx.moveTo(padding, canvas.height - padding);
            ctx.lineTo(canvas.width - padding, canvas.height - padding);
            ctx.stroke();
            ctx.fillText('Distance (m)', canvas.width - 80, canvas.height - padding + 30);
        }

        function drawTrajectoryPath(trajectory, currentIndex, scale, padding) {
            ctx.beginPath();
            ctx.strokeStyle = '#DC2626'; // Superman red
            ctx.lineWidth = 3;
            ctx.setLineDash([5, 3]); // Dashed line
            for (let i = 0; i <= currentIndex; i++) {
                const cx = padding + trajectory[i].x * scale;
                const cy = (canvas.height - padding) - trajectory[i].y * scale;
                if (i === 0) ctx.moveTo(cx, cy);
                else ctx.lineTo(cx, cy);
            }
            ctx.stroke();
            ctx.setLineDash([]); // Reset dash
        }

        function drawSuperman(point, nextPoint, scale, padding) {
            const cx = padding + point.x * scale;
            const cy = (canvas.height - padding) - point.y * scale;

            // Calculate rotation angle based on velocity direction
            const angle = Math.atan2(-(nextPoint.y - point.y), nextPoint.x - point.x);

            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(angle);

            if (supermanLoaded) {
                // Draw Superman sprite - LARGER SIZE
                const size = 70; // Increased from 40px
                ctx.drawImage(supermanImg, -size / 2, -size / 2, size, size);
            } else {
                // Fallback: Draw red circle with S
                ctx.fillStyle = '#DC2626';
                ctx.beginPath();
                ctx.arc(0, 0, 8, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#FBBF24';
                ctx.font = 'bold 12px Arial';
                ctx.fillText('S', -4, 4);
            }

            ctx.restore();
        }

        function drawInfoPanel(point, physicsData) {
            const panelX = 60;
            const panelY = 20;
            const width = 240;
            const height = isPracticeMode ? 100 : 180;

            // Semi-transparent bg
            ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
            ctx.fillRect(panelX, panelY, width, height);
            ctx.strokeStyle = '#DC2626'; // Superman red border
            ctx.lineWidth = 2;
            ctx.strokeRect(panelX, panelY, width, height);

            ctx.fillStyle = '#000';
            ctx.font = '11px monospace';
            let y = panelY + 20;

            let lines = [];

            if (isPracticeMode) {
                lines = [
                    `🦸 SUPERMAN TRAINING`,
                    `Time:     --- s`,
                    `Position: (---, ---) m`,
                    `Velocity: --- m/s`,
                    `-----------------`,
                    `MISSION: CALCULATE`,
                    `VALUES HIDDEN`
                ];
            } else {
                lines = [
                    `Time:     ${point.time.toFixed(2)} s`,
                    `Position: (${point.x.toFixed(1)}, ${point.y.toFixed(1)}) m`,
                    `Velocity: ${point.v.toFixed(2)} m/s`,
                    `Energy:   ${point.e_total.toFixed(0)} J/kg`,
                    `-----------------`,
                    `Max H:    ${physicsData.max_height.toFixed(2)} m`,
                    `Range:    ${physicsData.range.toFixed(2)} m`,
                    `Impact V: ${physicsData.impact_velocity.toFixed(2)} m/s`
                ];
            }

            lines.forEach(line => {
                ctx.fillText(line, panelX + 10, y);
                y += 15;
            });
        }

        requestAnimationFrame(draw);
    }
});