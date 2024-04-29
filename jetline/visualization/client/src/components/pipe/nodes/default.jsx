import { Handle, Position } from 'reactflow';
import './nodes.css';
import FunctionsIcon from '@mui/icons-material/Functions';
import StorageIcon from '@mui/icons-material/Storage';
import CodeIcon from '@mui/icons-material/Code';

const handleStyle = {
  background: 'var(--nodes-background)',
  width: '12px',
  height: '3px',
  borderRadius: '2px',
  border: '0.75px solid var(--nodes-border)',
};

function DefaultNode({ data, onNodeClick }) {
  console.log(data)
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

  if (!data.inputs) {
    inputHandle = null;
  }

  if (!data.outputs) {
    outputHandle = null;
  }

  const handleClick = () => {
    onNodeClick(data);
  };

  const truncatedTitle = data.title.length > 15 ? data.title.substring(0, 15)  : data.title;

  return (
    <div
      key={data.id}
      style={{ display: 'flex', alignItems: 'center' }}
      onClick={handleClick}
    >
      {inputHandle}
      {icon}
      <div style={{ marginLeft: '0.5rem' }}>{truncatedTitle}</div>
      {outputHandle}
    </div>
  );
}

// Standardwertzuweisung für onNodeClick, falls nicht übergeben
DefaultNode.defaultProps = {
  onNodeClick: () => {},
};

export default DefaultNode;
