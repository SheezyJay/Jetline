import Panzoom from '@panzoom/panzoom'
var elem = document.getElementById("app");
console.log(elem)
const panzoom = Panzoom(elem, {
  maxScale: 5
})

elem.addEventListener('panzoomstart', function(event) {
  
});

elem.addEventListener('panzoomchange', function(event) {
  
});

elem.addEventListener('panzoomend', function(event) {
  
});
// Maus- und Touchpad-Zoom
elem.addEventListener('wheel', function(event) {
  panzoom.zoomWithWheel(event, {
      step: 0.1, // Anpassen der Zoomgeschwindigkeit
  });
});

// Touchpad-Zoom
elem.addEventListener('touchstart', function(event) {
  if (event.touches.length === 2) {
      panzoom.startZoom(event);
  }
});

elem.addEventListener('touchmove', function(event) {
  if (event.touches.length === 2) {
      panzoom.moveZoom(event);
  }
});

elem.addEventListener('touchend', function(event) {
  if (event.touches.length === 0) {
      panzoom.endZoom(event);
  }
});



// Panning and pinch zooming are bound automatically (unless disablePan is true).
// There are several available methods for zooming
// that can be bound on button clicks or mousewheel.
//button.addEventListener('click', panzoom.zoomIn)
//elem.parentElement.addEventListener('wheel', panzoom.zoomWithWheel)