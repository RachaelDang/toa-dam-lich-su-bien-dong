var typed = new Typed(".text", {
    strings: ["Frontend Developer", "YouTuber", "Web Developer"],
    typeSpeed: 100,
    backSpeed: 100,
    backDelay: 1000,
    loop: true
});

const sections = document.querySelectorAll('.context, .delegates, .debate, .statement');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animationPlayState = 'running';
        }
    });
}, { threshold: 0.1 });

sections.forEach(section => {
    section.style.animationPlayState = 'paused';
    observer.observe(section);
});

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const home = document.querySelector('.home');
    const imageFrame = document.querySelector('.image-frame');

    if (home) {
        home.style.backgroundPosition = `center ${scrolled * 0.3}px`;
    }

    if (imageFrame) {
        imageFrame.style.transform = `translateY(${scrolled * 0.2}px)`;
    }

    document.querySelectorAll('.context, .delegates, .debate, .statement').forEach((section, i) => {
        const rect = section.getBoundingClientRect();
        const speed = 0.1 + (i * 0.05);
        if (rect.top < window.innerHeight) {
            section.style.transform = `translateY(${scrolled * speed}px)`;
        }
    });
});