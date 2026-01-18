// ==========================================
// PARTICLE SYSTEM
// ==========================================

class ParticleSystem {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;

    this.ctx = this.canvas.getContext("2d");
    this.particles = [];
    this.particleCount = 50;
    this.mouse = { x: null, y: null, radius: 150 };

    this.init();
    this.animate();
    this.setupEventListeners();
  }

  init() {
    this.resizeCanvas();
    this.createParticles();
  }

  resizeCanvas() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.particleCount; i++) {
      const size = Math.random() * 3 + 1;
      const x = Math.random() * this.canvas.width;
      const y = Math.random() * this.canvas.height;
      const speedX = (Math.random() - 0.5) * 0.5;
      const speedY = (Math.random() - 0.5) * 0.5;
      const color = this.getRandomColor();

      this.particles.push({
        x,
        y,
        size,
        speedX,
        speedY,
        color,
        opacity: Math.random() * 0.5 + 0.2,
      });
    }
  }

  getRandomColor() {
    const colors = [
      "rgba(102, 126, 234, ",
      "rgba(118, 75, 162, ",
      "rgba(79, 172, 254, ",
      "rgba(0, 242, 254, ",
      "rgba(67, 233, 123, ",
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  drawParticle(particle) {
    this.ctx.beginPath();
    this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
    this.ctx.fillStyle = particle.color + particle.opacity + ")";
    this.ctx.fill();

    // Add glow effect
    this.ctx.shadowBlur = 10;
    this.ctx.shadowColor = particle.color + "0.8)";
  }

  drawConnections() {
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(102, 126, 234, ${
            0.2 * (1 - distance / 100)
          })`;
          this.ctx.lineWidth = 1;
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.stroke();
        }
      }
    }
  }

  updateParticle(particle) {
    // Move particle
    particle.x += particle.speedX;
    particle.y += particle.speedY;

    // Bounce off edges
    if (particle.x < 0 || particle.x > this.canvas.width) {
      particle.speedX *= -1;
    }
    if (particle.y < 0 || particle.y > this.canvas.height) {
      particle.speedY *= -1;
    }

    // Mouse interaction
    if (this.mouse.x != null && this.mouse.y != null) {
      const dx = particle.x - this.mouse.x;
      const dy = particle.y - this.mouse.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < this.mouse.radius) {
        const force = (this.mouse.radius - distance) / this.mouse.radius;
        const angle = Math.atan2(dy, dx);
        particle.x += Math.cos(angle) * force * 2;
        particle.y += Math.sin(angle) * force * 2;
      }
    }

    // Pulse opacity
    particle.opacity += Math.sin(Date.now() * 0.001) * 0.001;
    particle.opacity = Math.max(0.2, Math.min(0.7, particle.opacity));
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Update and draw particles
    this.particles.forEach((particle) => {
      this.updateParticle(particle);
      this.drawParticle(particle);
    });

    // Draw connections
    this.drawConnections();

    requestAnimationFrame(() => this.animate());
  }

  setupEventListeners() {
    window.addEventListener("resize", () => {
      this.resizeCanvas();
      this.createParticles();
    });

    window.addEventListener("mousemove", (event) => {
      this.mouse.x = event.x;
      this.mouse.y = event.y;
    });

    window.addEventListener("mouseout", () => {
      this.mouse.x = null;
      this.mouse.y = null;
    });
  }
}

// Initialize particle system when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new ParticleSystem("particleCanvas");
  });
} else {
  new ParticleSystem("particleCanvas");
}
