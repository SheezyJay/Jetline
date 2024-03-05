import './assets/css/style.css';
import { createBlock } from './components/block.js';
import { createContainer,appendToNodesContainer } from './components/container.js';
import { createArrow } from './components/arrow';


const appContainer = document.querySelector('#app');

// Erstelle den ersten Container für die Blöcke
const container1 = createContainer('blockContainer1');

// Erstelle den zweiten Container für die Blöcke
const container2 = createContainer('blockContainer2');

// Erstelle die Blöcke und füge sie dem ersten Container hinzu
const options1 = {
  content: 'Inhalt für Daten',
  type: 'data'
};
const myBlock1 = createBlock('customBlock1', options1);
const myBlock3 = createBlock('customBlock3', options1);
appendToNodesContainer(container1,myBlock1);
appendToNodesContainer(container1,myBlock3);

// Erstelle die Blöcke und füge sie dem zweiten Container hinzu
const options2 = {
  content: 'Inhalt für Funktion',
  type: 'function'
};
const myBlock2 = createBlock('customBlock2', options2);
container2.appendChild(myBlock2);

// Füge den ersten Container dem App-Container hinzu
appContainer.appendChild(container1);


// Füge den zweiten Container dem App-Container hinzu
appContainer.appendChild(container2);
createArrow("#customBlock1","#customBlock2")

createArrow("#customBlock3","#customBlock2")


// Wähle das Sidebar-Element aus
const sidebar = document.getElementById('sidebar');

// Wähle das Hauptinhaltselement aus
const mainContent = document.getElementById('app');

// Füge einen Event-Listener hinzu, um die Sidebar zu öffnen, wenn auf ein bestimmtes Element geklickt wird
const openSidebarButton = document.getElementById('button');
openSidebarButton.addEventListener('click', function() {
    sidebar.classList.toggle('open');
    mainContent.classList.toggle('open');
});

