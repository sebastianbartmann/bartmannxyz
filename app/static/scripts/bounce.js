/* Home page background: a pixel-art head that bounces off the viewport edges like a ball.
   Each bounce swaps in the next beard stage; after the longest beard it starts over.
   The head is the ball (a circle around the face); the beard hangs outside it and may
   leave the screen. No motion for visitors who ask for reduced motion. */
(() => {
    const FRAMES = 8;
    const SPEED = 130; // px per second
    const SPIN = 45; // degrees per second
    const host = document.querySelector("[data-bounce]");
    if (!host || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const version = new URL(document.currentScript.src).search;
    const ball = document.createElement("div");
    ball.className = "bounce__ball";
    const frames = [];
    for (let i = 0; i < FRAMES; i++) {
        const img = new Image();
        img.src = `/static/images/bartmann/beard-${i}.png${version}`;
        img.alt = "";
        img.className = "bounce__frame";
        img.hidden = i !== 0;
        ball.appendChild(img);
        frames.push(img);
    }
    host.appendChild(ball);

    let frame = 0;
    let radius = 0;
    let x = 0;
    let y = 0;
    let dx = 0.78;
    let dy = 0.62;
    let angle = 0;
    let spin = SPIN;
    let last = null;

    const measure = () => {
        // The head is 80% of the image width; the ball is a little larger than half of that.
        radius = frames[0].getBoundingClientRect().width * 0.47 || radius;
    };

    const step = (now) => {
        requestAnimationFrame(step);
        if (last === null) {
            last = now;
            measure();
            x = radius + Math.random() * Math.max(0, window.innerWidth - 2 * radius);
            y = radius + Math.random() * Math.max(0, window.innerHeight - 2 * radius);
        }
        const dt = Math.min(now - last, 50) / 1000;
        last = now;
        const maxX = window.innerWidth - radius;
        const maxY = window.innerHeight - radius;
        x += dx * SPEED * dt;
        y += dy * SPEED * dt;
        let bounced = false;
        if (x < radius || x > maxX) {
            dx = x < radius ? Math.abs(dx) : -Math.abs(dx);
            x = Math.min(Math.max(x, radius), Math.max(maxX, radius));
            bounced = true;
        }
        if (y < radius || y > maxY) {
            dy = y < radius ? Math.abs(dy) : -Math.abs(dy);
            y = Math.min(Math.max(y, radius), Math.max(maxY, radius));
            bounced = true;
        }
        if (bounced) {
            frames[frame].hidden = true;
            frame = (frame + 1) % FRAMES;
            frames[frame].hidden = false;
            spin = -spin;
        }
        angle = (angle + spin * dt) % 360;
        ball.style.transform = `translate3d(${x}px, ${y}px, 0) rotate(${angle}deg)`;
    };

    window.addEventListener("resize", measure);
    frames[0].decode().catch(() => {}).then(() => requestAnimationFrame(step));
})();
