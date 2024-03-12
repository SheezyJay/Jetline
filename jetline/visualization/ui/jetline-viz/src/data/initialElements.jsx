
import { ArrowForward, ArrowBack, Check } from '@mui/icons-material';


export const nodes = [

    {
      type: 'default',
      id: '1',
      data:  { "icon": "<Check />", "title": "readFile", "subline": "api.ts", "stream": ["output"], "code": "def node_function_1(data):\n    \"\"\"\n    An example function that processes data and returns a modified version.\n\n    Args:\n        data: The input data to be processed.\n\n    Returns:\n        str: The processed data.\n    \"\"\"\n    print('Input Data:', data)\n    processed_data = data + 'asasdasdd'\n    print('Processed Data:', processed_data)\n    return processed_data", "type":"data", "input": "Name", "output": "OutputName"},
      position: { x: 100, y: 0 },

    },
    {
      type: 'default',
      id: '2',
      data: { title: 'for' },
      position: { x: 0, y: 100 },
    
    },
    {
      type: 'default',
      id: '3',
      data: { title: 'using' },
      position: { x: 200, y: 100 },
    
    },
    {
      type: 'output',
      id: '4',
      data: { label: 'React Flow Pro!' },
      position: { x: 100, y: 200 },
    
    },
  ];
  
  export const edges = [
    {
      id: '1->2',
      source: '1',
      target: '2',
      animated: true,
    },
    {
      id: '1->3',
      source: '1',
      target: '3',
      animated: true,
    },
    {
      id: '2->4',
      source: '2',
      target: '4',
      animated: true,
    },
    {
      id: '3->4',
      source: '3',
      target: '4',
      animated: true,
    },
  ];
  