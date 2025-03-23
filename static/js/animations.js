/**
 * Table Football Tracker - Custom Animations and Interactions
 * Enhances the user experience with smooth animations and interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations for elements that are visible on page load
    initializeAnimations();
    
    // Add animation classes to elements when they come into view
    initializeScrollAnimations();
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Initialize match form dynamic behavior
    initializeMatchForm();
    
    // Initialize profile color picker preview
    initializeProfileColorPicker();
    
    // Add football bounce effect to icons
    addFootballBounceEffect();
});

/**
 * Initialize animations for elements that are visible on page load
 */
function initializeAnimations() {
    // Add animation classes to headings
    document.querySelectorAll('h1, h2, h3').forEach(function(element, index) {
        element.classList.add('animate__animated');
        element.classList.add('animate__fadeInDown');
        element.style.animationDelay = (0.1 * index) + 's';
    });
    
    // Add animation classes to cards
    document.querySelectorAll('.card').forEach(function(element, index) {
        element.classList.add('animate__animated');
        element.classList.add('animate__fadeIn');
        element.style.animationDelay = (0.2 * index) + 's';
    });
    
    // Add animation classes to buttons
    document.querySelectorAll('.btn-primary').forEach(function(element) {
        element.classList.add('custom-pulse');
    });
    
    // Add animation to score displays
    document.querySelectorAll('.score-display').forEach(function(element) {
        element.classList.add('count-up');
    });
}

/**
 * Initialize scroll-triggered animations
 */
function initializeScrollAnimations() {
    // Create an Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated');
                
                // Add different animations based on element type
                if (entry.target.classList.contains('card')) {
                    entry.target.classList.add('animate__fadeIn');
                } else if (entry.target.classList.contains('player-avatar')) {
                    entry.target.classList.add('animate__zoomIn');
                } else if (entry.target.classList.contains('btn')) {
                    entry.target.classList.add('animate__bounceIn');
                } else {
                    entry.target.classList.add('animate__fadeIn');
                }
                
                // Stop observing after animation is added
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // Observe elements that should be animated
    const elementsToAnimate = document.querySelectorAll('.card, .player-avatar, .btn, .list-group-item');
    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Initialize interactive elements
 */
function initializeInteractiveElements() {
    // Add hover effects to player avatars
    document.querySelectorAll('.player-avatar').forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            this.classList.add('animate__pulse');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('animate__pulse');
        });
    });
    
    // Add click effects to score displays
    document.querySelectorAll('.score-display').forEach(function(element) {
        element.addEventListener('click', function() {
            this.classList.add('animate__rubberBand');
            
            // Remove animation class after it completes
            setTimeout(() => {
                this.classList.remove('animate__rubberBand');
            }, 1000);
        });
    });
    
    // Add hover effects to match cards
    document.querySelectorAll('.match-card').forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.2)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
        });
    });
}

/**
 * Initialize match form dynamic behavior
 */
function initializeMatchForm() {
    const matchTypeSelect = document.getElementById('id_match_type');
    
    if (matchTypeSelect) {
        const team1Player2Field = document.getElementById('id_team1_player2')?.parentNode.parentNode;
        const team2Player2Field = document.getElementById('id_team2_player2')?.parentNode.parentNode;
        
        function updatePlayerFields() {
            const matchType = matchTypeSelect.value;
            
            if (matchType === '1v1') {
                if (team1Player2Field) team1Player2Field.style.display = 'none';
                if (team2Player2Field) team2Player2Field.style.display = 'none';
            } else if (matchType === '2v1') {
                if (team1Player2Field) team1Player2Field.style.display = 'block';
                if (team2Player2Field) team2Player2Field.style.display = 'block';
            } else if (matchType === '2v2') {
                if (team1Player2Field) team1Player2Field.style.display = 'block';
                if (team2Player2Field) team2Player2Field.style.display = 'block';
            }
        }
        
        // Initial update
        updatePlayerFields();
        
        // Update on change
        matchTypeSelect.addEventListener('change', updatePlayerFields);
    }
}

/**
 * Initialize profile color picker preview
 */
function initializeProfileColorPicker() {
    const colorInput = document.getElementById('id_profile_color');
    const colorPreview = document.getElementById('color-preview');
    
    if (colorInput && colorPreview) {
        // Update preview on color change
        colorInput.addEventListener('input', function() {
            colorPreview.style.backgroundColor = this.value;
        });
    }
}

/**
 * Add football bounce effect to icons
 */
function addFootballBounceEffect() {
    document.querySelectorAll('.fa-futbol').forEach(function(element) {
        element.classList.add('bounce');
    });
}

/**
 * Add confetti effect for wins
 * @param {HTMLElement} element - The element to attach the confetti effect to
 */
function addConfettiEffect(element) {
    element.addEventListener('click', function(e) {
        // Create and append canvas for confetti
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);
        
        // Configure confetti
        const confetti = {
            canvas: canvas,
            ctx: canvas.getContext('2d'),
            particles: [],
            colors: ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6'],
            
            start: function() {
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
                this.createParticles();
                this.loop();
                
                // Remove canvas after animation completes
                setTimeout(() => {
                    document.body.removeChild(canvas);
                }, 3000);
            },
            
            createParticles: function() {
                for (let i = 0; i < 100; i++) {
                    this.particles.push({
                        x: e.clientX,
                        y: e.clientY,
                        size: Math.random() * 10 + 5,
                        color: this.colors[Math.floor(Math.random() * this.colors.length)],
                        vx: Math.random() * 10 - 5,
                        vy: Math.random() * -10 - 10,
                        gravity: 0.5,
                        rotation: Math.random() * 360,
                        rotationSpeed: Math.random() * 10 - 5
                    });
                }
            },
            
            loop: function() {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                for (let i = 0; i < this.particles.length; i++) {
                    const p = this.particles[i];
                    
                    p.vy += p.gravity;
                    p.x += p.vx;
                    p.y += p.vy;
                    p.rotation += p.rotationSpeed;
                    
                    this.ctx.save();
                    this.ctx.translate(p.x, p.y);
                    this.ctx.rotate(p.rotation * Math.PI / 180);
                    this.ctx.fillStyle = p.color;
                    this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
                    this.ctx.restore();
                    
                    if (p.y > this.canvas.height) {
                        this.particles.splice(i, 1);
                        i--;
                    }
                }
                
                if (this.particles.length > 0) {
                    requestAnimationFrame(this.loop.bind(this));
                }
            }
        };
        
        confetti.start();
    });
}

// Apply confetti effect to win badges
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.alert-success').forEach(function(element) {
        addConfettiEffect(element);
    });
});
