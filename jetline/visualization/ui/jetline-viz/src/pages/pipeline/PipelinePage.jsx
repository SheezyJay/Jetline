import React, { useState, useMemo } from "react";
import Layout from "../../layout/Layout";
import "../../assets/css/layout/content.css";
import "../../assets/css/components/react-flow.css";
import "reactflow/dist/style.css";
import DefaultNode from '../../components/pipe/nodes/default';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
} from "reactflow";
import InfoSidebar from '../../components/content/InfoSidebar';

import { nodes, edges } from "../../data/initialElements";

const proOptions = { hideAttribution: true };

const minimapStyle = {
  height: 120,
};

const PipelinePage = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [data, setData] = useState({ name: '', links: [] });

  const closeSidebar = () => {
    setIsOpen(false);
  };
  const handleNodeClick = (_, node) => {
    setData(node.data);
    setIsOpen(true);
  };
  
  const nodeTypes = useMemo(() => ({
    default: DefaultNode,
  }), []);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      fitView
      proOptions={proOptions}
      onNodeClick={handleNodeClick}
      nodeTypes={nodeTypes}
   
    >
      <Layout>
        <MiniMap style={minimapStyle} zoomable pannable maskColor="#222" maskStrokeColor="#333" />
        <Background variant='' />
      </Layout>
      <Controls />
      <InfoSidebar isOpen={isOpen} data={data} onClose={closeSidebar} />
    </ReactFlow>
  );
};

export default PipelinePage;
