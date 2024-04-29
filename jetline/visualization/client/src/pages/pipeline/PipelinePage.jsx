import { useState, useEffect, useMemo } from "react";
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
import DefaultEdge from "../../components/pipe/edge/default";

const proOptions = { hideAttribution: true };

const minimapStyle = {
  height: 120,
};

const PipelinePage = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [data, setData] = useState({ name: '', links: [] });
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/pipe_data');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const responseData = await response.json();
        setNodes(responseData.nodes);
        setEdges(responseData.edges);
      } catch (error) {
        console.log(error)
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

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

  const edgeTypes = useMemo(() => ({
    default: DefaultEdge,
  }), []);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      fitView
      proOptions={proOptions}
      onNodeClick={handleNodeClick}
      nodeTypes={nodeTypes}
      edgeTypes={edgeTypes}
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
