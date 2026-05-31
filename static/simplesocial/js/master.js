// STAR SOCIAL — galaxy starfield background.
// Layered twinkling stars with parallax drift + occasional shooting stars.
// Pure vanilla, lightweight, and respects prefers-reduced-motion.
(function () {
    const canvas = document.getElementById('canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let width = 0;
    let height = 0;
    let dpr = 1;
    let stars = [];
    let shootingStars = [];

    // Three depth layers: far (small/dim/slow) → near (big/bright/fast).
    const LAYERS = [
        { count: 0.00018, size: [0.4, 0.9], speed: 0.04, alpha: [0.25, 0.55] },
        { count: 0.00012, size: [0.7, 1.4], speed: 0.09, alpha: [0.45, 0.8] },
        { count: 0.00006, size: [1.1, 2.1], speed: 0.16, alpha: [0.6, 1.0] },
    ];

    const rand = (min, max) => Math.random() * (max - min) + min;

    function buildStars() {
        stars = [];
        const area = width * height;
        for (const layer of LAYERS) {
            const n = Math.round(area * layer.count);
            for (let i = 0; i < n; i++) {
                stars.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    r: rand(layer.size[0], layer.size[1]),
                    speed: layer.speed,
                    baseAlpha: rand(layer.alpha[0], layer.alpha[1]),
                    twinkle: rand(0, Math.PI * 2),
                    twinkleSpeed: rand(0.005, 0.02),
                });
            }
        }
    }

    function resize() {
        dpr = Math.min(window.devicePixelRatio || 1, 2);
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        buildStars();
    }

    function spawnShootingStar() {
        const fromLeft = Math.random() > 0.5;
        shootingStars.push({
            x: fromLeft ? rand(0, width * 0.3) : rand(width * 0.7, width),
            y: rand(0, height * 0.4),
            len: rand(120, 240),
            speed: rand(6, 11),
            angle: fromLeft ? rand(0.35, 0.6) : Math.PI - rand(0.35, 0.6),
            life: 1,
        });
    }

    function drawStar(s) {
        s.twinkle += s.twinkleSpeed;
        const alpha = s.baseAlpha * (0.6 + 0.4 * Math.sin(s.twinkle));
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
        ctx.fill();
        // subtle cyan glow on the brightest stars
        if (s.r > 1.4) {
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r * 2.4, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(0, 242, 254, ${alpha * 0.08})`;
            ctx.fill();
        }
    }

    function updateStar(s) {
        s.y += s.speed;
        if (s.y - s.r > height) {
            s.y = -s.r;
            s.x = Math.random() * width;
        }
    }

    function drawShootingStar(ss) {
        const dx = Math.cos(ss.angle) * ss.len;
        const dy = Math.sin(ss.angle) * ss.len;
        const grad = ctx.createLinearGradient(ss.x, ss.y, ss.x - dx, ss.y - dy);
        grad.addColorStop(0, `rgba(255, 255, 255, ${ss.life})`);
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.strokeStyle = grad;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(ss.x, ss.y);
        ctx.lineTo(ss.x - dx, ss.y - dy);
        ctx.stroke();

        ss.x += Math.cos(ss.angle) * ss.speed;
        ss.y += Math.sin(ss.angle) * ss.speed;
        ss.life -= 0.012;
    }

    function frame() {
        ctx.clearRect(0, 0, width, height);
        for (const s of stars) {
            updateStar(s);
            drawStar(s);
        }
        for (let i = shootingStars.length - 1; i >= 0; i--) {
            drawShootingStar(shootingStars[i]);
            if (shootingStars[i].life <= 0) shootingStars.splice(i, 1);
        }
        if (Math.random() < 0.004 && shootingStars.length < 2) spawnShootingStar();
        requestAnimationFrame(frame);
    }

    function renderStatic() {
        ctx.clearRect(0, 0, width, height);
        for (const s of stars) {
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${s.baseAlpha})`;
            ctx.fill();
        }
    }

    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            resize();
            if (reduceMotion) renderStatic();
        }, 150);
    });

    resize();
    if (reduceMotion) {
        renderStatic();
    } else {
        frame();
    }
})();
