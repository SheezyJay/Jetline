import '../assets/css/style.css';

/**
 * Erstellt ein klickbares Div-Element mit gegebenen Optionen und exportiert es als Modul.
 * @param {string} id Die ID für das Div-Element.
 * @param {Object} options Die Optionen für das Block-Element.
 * @param {string} options.content Der Inhalt für das Div-Element.
 * @param {string} options.type Der Typ des Icons ('function' oder 'data').
 * @returns {HTMLElement} Das erstellte Block-Element.
 */
export function createBlock(id, options) {
  const block = document.createElement('div');
  block.setAttribute('id', id);
  block.className = 'block';
 
   

  switch (options.type) {
    case 'function':
      block.innerHTML = `<i class="bi bi-braces"></i> ${options.content}`;
      block.style.borderRadius =  '08px';
      break;
    case 'data':
      block.innerHTML = `<i class="bi bi-database"></i> ${options.content}`;
      block.style.borderRadius =  '20px';
      break;
    default:
      throw new Error('Ungültiger Icon-Typ');
  }

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
