const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

                
const audio = new Audio(); // Create a new Audio object

const playTune = (keyCode) => {
    const soundUrl = sound[keyCode]; // Get the sound URL based on the key code
    if (soundUrl) {
        audio.src = soundUrl; // Set the source of the audio element
        audio.play(); // Play the audio
        // Gradually decrease the volume
    }
    const clickedKey = document.querySelector(`[data-key="${keyCode}"]`)
    clickedKey.classList.add("active");
    setTimeout(() => {
        clickedKey.classList.remove("active");
    }, 150);
};

const pressedKey = (e) => {
    if (document.activeElement.tagName === "INPUT" || document.activeElement.tagName === "TEXTAREA") {
        return; // Exit early if an input field is focused
    }

    const keyCode = e.keyCode || e.which;
    playTune(keyCode);
}

document.addEventListener("keydown", pressedKey);

const sequence = 'weseeyou';
let currentSequence = '';

document.addEventListener('keydown', (event) => {
    // Get the key pressed
    const key = event.key.toLowerCase();

    // Check if the key pressed matches the next character in the sequence
    if (key === sequence[currentSequence.length]) {
        currentSequence += key;

        // If the current sequence matches the full sequence, add the 'active' class to the wrapper
        if (currentSequence === sequence) {
            const wrapper = document.querySelector('.wrapper');
            wrapper.classList.add('active');
            // Play the creepy piano sound effect
            const creepyAudio = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
            creepyAudio.play();
            // Remove piano key listener
            document.removeEventListener('keydown', pressedKey);
        }
    } else {
        // Reset the sequence if a wrong key is pressed
        currentSequence = '';
    }
});