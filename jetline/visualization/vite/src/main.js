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
              "Function": "def register(data_manager) -> Pipeline:\n    return Pipeline(nodes=[\n        Node(name='node1', function=func.node_function_1, inputs=[\"Name\",\"asd\"], outputs=[\"Name\"]),\n        Node(name='node2', function=func.node_function_2,inputs=[\"Name\"]),",
              "Description": null
          },
          "Nodes": [
              {
                  "name": "node_function_1",
                  "function": "def node_function_1(data):\n    \"\"\"\n    An example function that processes data and returns a modified version.\n\n    Args:\n        data: The input data to be processed.\n\n    Returns:\n        str: The processed data.\n    \"\"\"\n    print('Input Data:', data)\n    processed_data = data + 'asasdasdd'\n    print('Processed Data:', processed_data)\n    return processed_data",
                  "description": "An example function that processes data and returns a modified version.\n\nArgs:\n    data: The input data to be processed.\n\nReturns:\n    str: The processed data.",
                  "inputs": [
                      "Name",
                      "asd"
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
      "aa": {
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
      "n": {
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


Object.keys(json.Pipelines).forEach(pipelineName => {
  const pipeline = json.Pipelines[pipelineName];


  const pipelineContainer = createContainer(`${pipelineName}`);
  pipeline.Nodes.forEach(node => {
    const nodeOptions = {
      content: node.name,
      type: 'function' 
    };
    const nodeBlock = createBlock(node.name, nodeOptions);
    appendToNodesContainer(pipelineContainer, nodeBlock);
  });

  
  appContainer.appendChild(pipelineContainer);
});



