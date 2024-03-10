import React from 'react';
import { Handle, Position } from 'reactflow';
import './nodes.css';
import FunctionsIcon from '@mui/icons-material/Functions';
import StorageIcon from '@mui/icons-material/Storage';
import CodeIcon from '@mui/icons-material/Code';

function DefaultNode({ data }) {
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
    alert('Hallo');
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

export default DefaultNode;
