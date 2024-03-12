import React from 'react';
import { Handle, Position } from 'reactflow';
import './nodes.css';
import FunctionsIcon from '@mui/icons-material/Functions';
import StorageIcon from '@mui/icons-material/Storage';
import CodeIcon from '@mui/icons-material/Code';

function DefaultNode({ data, onNodeClick }) {
  let icon = null;
  let inputHandle = <Handle type="target" position={Position.Top} />;
  let outputHandle = <Handle type="source" position={Position.Bottom} />;

  if (data.type === 'function') {
    icon = <CodeIcon />;
  } else if (data.type === 'data') {
    icon = <StorageIcon />;
  } else {
    icon = <FunctionsIcon />;
  }

  if (data.stream && !data.stream.includes('input')) {
    inputHandle = null;
  }

  if (data.stream && !data.stream.includes('output')) {
    outputHandle = null;
  }

  const handleClick = () => {
    onNodeClick(data);
  };

  return (
    <div key={data.id} style={{ display: 'flex', alignItems: 'center' }} onClick={handleClick}>
      {inputHandle}
      {icon}
      <div style={{ marginLeft: '0.5rem' }}>{data.title}</div>
      {outputHandle}
    </div>
  );
}

// Standardwertzuweisung für onNodeClick, falls nicht übergeben
DefaultNode.defaultProps = {
  onNodeClick: () => {} // Standard-Handler, der keine Aktion ausführt
};

export default DefaultNode;
