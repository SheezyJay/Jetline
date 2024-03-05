import './assets/css/style.css'

import { createBlock } from './components/block.js';

const appContainer = document.querySelector('#app');
  const myBlock = createBlock('customBlock', '<i>🌟 Mein Icon</i>', '8px');
  appContainer.appendChild(myBlock);

  const myBlock2 = createBlock('customBlock2', '<i>✨ Mein Icon 2</i>', '8px');
appContainer.appendChild(myBlock2);
  