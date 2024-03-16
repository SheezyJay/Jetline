import React from 'react';
import { Handle, Position } from 'reactflow';
import './nodes.css';
import FunctionsIcon from '@mui/icons-material/Functions';
import StorageIcon from '@mui/icons-material/Storage';
import CodeIcon from '@mui/icons-material/Code';
import CircularProgress from '@mui/material/CircularProgress'; // Importieren des Ladesymbols

const handleStyle = {
  background: 'var(--nodes-background)',
  width: '12px',
  height: '3px',
  borderRadius: '2px',
  border: '0.75px solid var(--nodes-border)',
};

function DefaultNode({ data, onNodeClick, running, isLoading }) { 
  let icon = null;
  let inputHandle = <Handle className="react_flow_dot"  type="target" position={Position.Top} style={handleStyle} />;
  let outputHandle = <Handle className="react_flow_dot" type="source" position={Position.Bottom} style={handleStyle} />;

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
    <div
      key={data.id}
      className="node-default"
      style={{ display: 'flex', alignItems: 'center' }}
      onClick={handleClick}
    >
       {inputHandle}
      {icon}
      <div style={{ marginLeft: '0.5rem' }}>{data.title}</div>
      {outputHandle}
    </div>
  );
}

// Standardwertzuweisung für onNodeClick, falls nicht übergeben
DefaultNode.defaultProps = {
  onNodeClick: () => {}, 
  running: false, // Standardmäßig ist `running` false
  isLoading: false, // Standardmäßig ist `isLoading` false
};

export default DefaultNode;
