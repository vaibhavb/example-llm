console.log("Hello, World! ChatGPT Text Completion extension is running.");

function onInputEvent(event) {
    console.log("Listening to typing")
    const inputElement = event.target;
    if (inputElement.matches('input[type="text"], input[type="search"], textarea')) {
      console.log('User is typing:', inputElement.value);
    }
  }
  
  document.body.addEventListener('input', onInputEvent);
  
  