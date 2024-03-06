export function createContainer(id) {
  
    const container = document.createElement('div');
    container.setAttribute('id', id);
    container.className = 'pipe-container';

    const infoTitleElement = document.createElement('h2');
    infoTitleElement.textContent = id;
    infoTitleElement.classList.add('pipe-title');

    container.appendChild(infoTitleElement);

    const nodesDiv = document.createElement('div');
    nodesDiv.classList.add('nodes');

    container.appendChild(nodesDiv);

    return container;
}

export function appendToNodesContainer(container, element) {
    const nodesContainer = container.querySelector('.nodes');
    nodesContainer.appendChild(element);
}
