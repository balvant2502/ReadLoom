const profileBtn = document.getElementById('profile-btn');
const profileSlider = document.getElementById('profile-slider');
const closeSlider = document.getElementById('close-slider');

// Open Slider
profileBtn.addEventListener('click', () => {
    profileSlider.classList.add('active');
});

// Close Slider
closeSlider.addEventListener('click', () => {
    profileSlider.classList.remove('active');
});

// Close Slider if clicking outside
document.addEventListener('click', (e) => {
    if (!profileSlider.contains(e.target) && !profileBtn.contains(e.target)) {
        profileSlider.classList.remove('active');
    }
});