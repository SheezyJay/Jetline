import React, { useState } from "react";
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


import { nodes, edges } from "../../data/initialElements";

const proOptions = { hideAttribution: true };

const minimapStyle = {
  height: 120,
};

const nodeTypes = {
  default: DefaultNode,
};

const PipelinePage = () => {

  return (
    <ReactFlow
      defaultNodes={nodes}
      defaultEdges={edges}
      fitView
      proOptions={proOptions}
      nodeTypes={nodeTypes}
      nodesDraggable
    >
      <Layout>
        <MiniMap style={minimapStyle} zoomable pannable maskColor="#222" maskStrokeColor="#333" />
        <Background variant='' />
      </Layout>
      <Controls className="react-flow__controls" />
    </ReactFlow>
  );
};

export default PipelinePage;
