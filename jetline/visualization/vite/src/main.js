import './assets/css/style.css';
import { createBlock } from './components/block.js';
import { createContainer,appendToNodesContainer } from './components/container.js';
import { createArrow } from './components/arrow';


const appContainer = document.querySelector('#app');

var json = {
  "ProjectName": "project",
  "DataClasses": [
      {
          "name": "Name",
          "description": "",
          "code": "class YourDataClass(Data):\n\n    def __init__(self):\n        super().__init__(name='Name', data=self.get_data())\n\n    @staticmethod\n    def get_data():\n        file = choose_file()\n        return file"
      }
  ],
  "Pipelines": {
      "example_pipeline": {
          "RegisterFunction": {
              "Function": "def register(data_manager) -> Pipeline:\n    return Pipeline(nodes=[\n        Node(name='node1', function=func.node_function_1, inputs=[\"Name\"], outputs=[\"Name\"]),\n        Node(name='node2', function=func.node_function_2,inputs=[\"Name\"]),",
              "Description": null
          },
          "Nodes": [
              {
                  "name": "node_function_1",
                  "function": "def node_function_1(data):\n    \"\"\"\n    An example function that processes data and returns a modified version.\n\n    Args:\n        data: The input data to be processed.\n\n    Returns:\n        str: The processed data.\n    \"\"\"\n    print('Input Data:', data)\n    processed_data = data + 'asasdasdd'\n    print('Processed Data:', processed_data)\n    return processed_data",
                  "description": "An example function that processes data and returns a modified version.\n\nArgs:\n    data: The input data to be processed.\n\nReturns:\n    str: The processed data.",
                  "inputs": [
                      "Name"
                  ],
                  "outputs": [
                      "Name"
                  ]
              },
              {
                  "name": "node_function_2",
                  "function": "def node_function_2(data):\n    \"\"\"\n    An example function that returns the input data unchanged.\n\n    Args:\n        data: The input data.\n\n    Returns:\n        str: The input data.\n    \"\"\"\n    print('Input Data:', data)\n    return data",
                  "description": "An example function that returns the input data unchanged.\n\nArgs:\n    data: The input data.\n\nReturns:\n    str: The input data.",
                  "inputs": [
                      "Name"
                  ],
                  "outputs": ""
              }
          ]
      },
      "second": {
          "RegisterFunction": {
              "Function": "def register(data_manager) -> Pipeline:\n    return Pipeline(nodes=[\n        Node(name='node1', function=func.node_function_3, inputs=[\"Name\"], outputs=[\"Name\"]),",
              "Description": null
          },
          "Nodes": [
              {
                  "name": "node_function_3",
                  "function": "def node_function_3(data):\n    \"\"\"\n    An example function that processes data and returns a modified version.\n\n    Args:\n        data: The input data to be processed.\n\n    Returns:\n        str: The processed data.\n    \"\"\"\n    print('Input Data:', data)\n    processed_data = data + 'asasdasdd'\n    print('Processed Data:', processed_data)\n    return processed_data",
                  "description": "An example function that processes data and returns a modified version.\n\nArgs:\n    data: The input data to be processed.\n\nReturns:\n    str: The processed data.",
                 
                 
              },
              {
                "name": "node_function_3",
                "function": "def node_function_3(data):\n    \"\"\"\n    An example function that processes data and returns a modified version.\n\n    Args:\n        data: The input data to be processed.\n\n    Returns:\n        str: The processed data.\n    \"\"\"\n    print('Input Data:', data)\n    processed_data = data + 'asasdasdd'\n    print('Processed Data:', processed_data)\n    return processed_data",
                "description": "An example function that processes data and returns a modified version.\n\nArgs:\n    data: The input data to be processed.\n\nReturns:\n    str: The processed data.",
                "inputs": [
                    "Name"
                ],
                "outputs": [
                    "Name"
                ]
            }
          ]
      },
      "third": {
          "RegisterFunction": {
              "Function": "def register(data_manager) -> Pipeline:\n    return Pipeline(nodes=[\n        Node(name='node1', function=func.node_function_4, inputs=[\"Name\"], outputs=[\"Name\"]),\n        Node(name='node2', function=func.node_function_5,inputs=[\"Name\"],outputs=[\"Name\"]),",
              "Description": null
          },
          "Nodes": [
              {
                  "name": "node_function_4",
                  "function": "def node_function_4(data):\n    \"\"\"\n    An example function that processes data and returns a modified version.\n\n    Args:\n        data: The input data to be processed.\n\n    Returns:\n        str: The processed data.\n    \"\"\"\n    print('Input Data:', data)\n    processed_data = data + 'asasdasdd'\n    print('Processed Data:', processed_data)\n    return processed_data",
                  "description": "An example function that processes data and returns a modified version.\n\nArgs:\n    data: The input data to be processed.\n\nReturns:\n    str: The processed data.",
                  "inputs": [
                      "Name"
                  ],
                  "outputs": [
                      "Name"
                  ]
              },
              {
                  "name": "node_function_5",
                  "function": "def node_function_5(data):\n    \"\"\"\n    An example function that returns the input data unchanged.\n\n    Args:\n        data: The input data.\n\n    Returns:\n        str: The input data.\n    \"\"\"\n    print('Input Data:', data)\n    return data",
                  "description": "An example function that returns the input data unchanged.\n\nArgs:\n    data: The input data.\n\nReturns:\n    str: The input data.",
                  "inputs": [
                      "Name"
                  ],
                  "outputs": [
                      "Name"
                  ]
              }
          ]
      }
  }
}


// add raw data

json.DataClasses.forEach(dataClass => {

  var container = createContainer(`${dataClass.name}`);
  console.log(container)
  var blockOptions = {
    content: 'Raw Data', 
    type: 'data'
  };
  var block = createBlock(dataClass.name, blockOptions);
  appendToNodesContainer(container, block);
  appContainer.appendChild(container);
});



function shouldStackNodes(nodes) {
  for (let i = 0; i < nodes.length - 1; i++) {
    const currentNode = nodes[i];
    const nextNode = nodes[i + 1];
    
    // Überprüfen, ob die Ausgaben der aktuellen Node mit den Eingaben der nächsten Node übereinstimmen
    if (currentNode.outputs && nextNode.inputs) {
      const commonOutputs = currentNode.outputs.filter(output => nextNode.inputs.includes(output));
      if (commonOutputs.length > 0) {
        return true; // Wenn es gemeinsame Ausgaben und Eingaben gibt, untereinander anordnen
      }
    }
  }
  return false; // Ansonsten nebeneinander anordnen
}


// add Pipeline data
Object.keys(json.Pipelines).forEach(pipelineName => {
  const pipeline = json.Pipelines[pipelineName];

  // Für jede Pipeline erstellen Sie einen neuen Container
  const pipelineContainer = createContainer(`${pipelineName}`);

  // Überprüfen, ob die Nodes nebeneinander oder untereinander angeordnet werden sollen
  const shouldStack = shouldStackNodes(pipeline.Nodes);

  // Verarbeiten der Nodes innerhalb der Pipeline
  pipeline.Nodes.forEach(node => {
    const nodeOptions = {
      content: node.name, // Verwenden Sie den Namen der Node als Inhalt
      type: 'function' // Annahme: 'function' für Nodes
    };
    const nodeBlock = createBlock(node.name, nodeOptions);

    // Hinzufügen von Klassen basierend auf dem Layout
    if (shouldStack) {
      nodeBlock.classList.add('stacked'); // Hinzufügen einer Klasse für Nodes, die untereinander angeordnet werden sollen
    } else {
      nodeBlock.classList.add('inline'); // Hinzufügen einer Klasse für Nodes, die nebeneinander angeordnet werden sollen
    }

    appendToNodesContainer(pipelineContainer, nodeBlock);

    // Überprüfen, ob die Node Outputs hat
    if (node.outputs && node.outputs.length > 0) {
      // Für jedes Element in den Outputs eine zusätzliche Node erstellen und direkt dem Pipeline-Container hinzufügen
      node.outputs.forEach(output => {
        const outputNodeOptions = {
          content: output, // Verwenden Sie den Namen des Outputs als Inhalt
          type: 'data' // Annahme: 'data' für Outputs
        };
        const outputNodeBlock = createBlock(output, outputNodeOptions);
        outputNodeBlock.classList.add('stacked');
        appendToNodesContainer(pipelineContainer, outputNodeBlock); // Fügen Sie den Output-Block direkt dem Pipeline-Container hinzu
      });
    }
  });

  // Fügen Sie den Pipeline-Container dem Haupt-App-Container hinzu
  appContainer.appendChild(pipelineContainer);
});
