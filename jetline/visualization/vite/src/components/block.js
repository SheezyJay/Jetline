import '../assets/css/style.css'

/**
 * Erstellt ein klickbares Div-Element mit gegebenen Optionen und exportiert es als Modul.
 * @param {string} id Die ID für das Div-Element.
 * @param {string} icon HTML-String oder Text für das Icon.
 * @param {string} borderRadius CSS-Wert für die Border-Rundung.
 * @returns {HTMLElement} Das erstellte Block-Element.
 */
export function createBlock(id, icon, borderRadius) {
  const block = document.createElement('div');
  block.setAttribute('id', id);
  block.className = 'block';
  block.style.borderRadius = borderRadius;
  block.innerHTML = `${icon}`;
  block.tabIndex = 0; // Macht es fokussierbar

  block.addEventListener('click', () => {
    console.log(`Block ${id} geklickt`);
  });

  // Optional: Hinzufügen einer Keyboard-Interaktion
  block.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      console.log(`Block ${id} geklickt (via Keyboard)`);
    }
  });

  return block;
}
