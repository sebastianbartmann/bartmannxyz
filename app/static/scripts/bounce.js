/* Home page background: a pixel-art head that bounces off the viewport edges like a ball.
   The head is the ball (a circle around the face); the beard hangs outside it and may
   leave the screen. Every bounce shows the next beard stage. After the last stage the
   beard floods the whole page, stays for a few bounces, then falls off and the head
   starts over clean-shaven. It bounces for everyone, also with prefers-reduced-motion
   set (Sebastian's decision, 2026-11-15: the head is the point of the page). */
(() => {
    const FRAMES = 12;
    const FLOOD_BOUNCES = 4; // bounces the page stays covered in beard
    const MAX_SPEED = 130; // px per second; slower on small screens, where edges are close
    const SPIN = 45; // degrees per second
    const HAIR = ["#3b2219", "#5a3324", "#7a4a35", "#9a6247"];
    const host = document.querySelector("[data-bounce]");
    if (!host) return;

    const version = new URL(document.currentScript.src).search;
    const base = "/static/images/bartmann/";

    const flood = document.createElement("div");
    flood.className = "bounce__flood";
    new Image().src = `${base}beard-texture.png${version}`; // preload for the finale
    host.appendChild(flood);

    const ball = document.createElement("div");
    ball.className = "bounce__ball";
    const frames = [];
    for (let i = 0; i < FRAMES; i++) {
        const img = new Image();
        img.src = `${base}beard-${i}.png${version}`;
        img.alt = "";
        img.className = "bounce__frame";
        img.hidden = i !== 0;
        ball.appendChild(img);
        frames.push(img);
    }
    host.appendChild(ball);

    let frame = 0;
    let flooded = -1; // bounces since the flood began, -1 while the beard still grows
    let radius = 0;
    let x = 0;
    let y = 0;
    let dx = 0.78;
    let dy = 0.62;
    let angle = 0;
    let spin = SPIN;
    let squash = 0;
    let last = null;
    const hairs = [];

    const measure = () => {
        // The head is 50.8% of the image width; the ball is a little larger than half of that.
        radius = frames[frame].offsetWidth * 0.3 || radius;
    };

    const show = (next) => {
        frames[frame].hidden = true;
        frame = next;
        frames[frame].hidden = false;
    };

    // Loose hairs fly off where the head hit the edge; more of them the longer the beard.
    const shed = (px, py, count) => {
        for (let i = 0; i < count; i++) {
            const el = document.createElement("i");
            el.className = "bounce__hair";
            el.style.background = HAIR[i % HAIR.length];
            host.appendChild(el);
            const a = Math.random() * Math.PI * 2;
            const v = 60 + Math.random() * 160;
            hairs.push({ el, x: px, y: py, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 80, life: 1 });
        }
    };

    const startFlood = () => {
        flooded = 0;
        flood.classList.remove("is-falling");
        flood.style.transition = "none";
        flood.style.clipPath = `circle(0px at ${x}px ${y}px)`;
        flood.hidden = false;
        flood.getBoundingClientRect(); // commit the start state before the transition
        flood.style.transition = "";
        flood.style.clipPath = `circle(${Math.hypot(window.innerWidth, window.innerHeight)}px at ${x}px ${y}px)`;
    };

    const shave = () => {
        flooded = -1;
        flood.classList.add("is-falling");
        show(0);
    };

    flood.hidden = true;
    flood.addEventListener("transitionend", (event) => {
        if (event.propertyName === "transform" && flood.classList.contains("is-falling")) {
            flood.hidden = true;
            flood.classList.remove("is-falling");
        }
    });

    const bounce = (px, py) => {
        spin = -spin;
        squash = 1;
        if (flooded >= 0) {
            flooded += 1;
            if (flooded > FLOOD_BOUNCES) shave();
        } else if (frame < FRAMES - 1) {
            show(frame + 1);
        } else {
            startFlood();
        }
        shed(px, py, frame === 0 ? 14 : 2 + frame);
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
        const speed = Math.min(MAX_SPEED, 40 + Math.hypot(window.innerWidth, window.innerHeight) * 0.06);
        const maxX = Math.max(window.innerWidth - radius, radius);
        const maxY = Math.max(window.innerHeight - radius, radius);
        x += dx * speed * dt;
        y += dy * speed * dt;
        let hitX = null;
        let hitY = null;
        if (x < radius || x > maxX) {
            dx = x < radius ? Math.abs(dx) : -Math.abs(dx);
            x = Math.min(Math.max(x, radius), maxX);
            hitX = dx > 0 ? 0 : window.innerWidth;
        }
        if (y < radius || y > maxY) {
            dy = y < radius ? Math.abs(dy) : -Math.abs(dy);
            y = Math.min(Math.max(y, radius), maxY);
            hitY = dy > 0 ? 0 : window.innerHeight;
        }
        if (hitX !== null || hitY !== null) bounce(hitX ?? x, hitY ?? y);

        angle = (angle + spin * dt) % 360;
        squash *= Math.exp(-7 * dt);
        ball.style.transform =
            `translate3d(${x}px, ${y}px, 0) rotate(${angle}deg) scale(${1 + 0.16 * squash})`;

        for (let i = hairs.length - 1; i >= 0; i--) {
            const h = hairs[i];
            h.life -= dt * 1.1;
            if (h.life <= 0) {
                h.el.remove();
                hairs.splice(i, 1);
                continue;
            }
            h.vy += 520 * dt;
            h.x += h.vx * dt;
            h.y += h.vy * dt;
            h.el.style.transform = `translate3d(${h.x}px, ${h.y}px, 0)`;
            h.el.style.opacity = Math.min(1, h.life * 2);
        }
    };

    window.addEventListener("resize", measure);
    frames[0].decode().catch(() => {}).then(() => requestAnimationFrame(step));
})();
