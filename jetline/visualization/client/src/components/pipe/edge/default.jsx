import React from 'react';
import { BezierEdge } from 'react-flow-renderer';

/**
 * DefaultEdge component represents a default edge in a flow chart.
 * @param {string} id - The unique identifier for the edge.
 * @param {number} sourceX - The x-coordinate of the edge's source.
 * @param {number} sourceY - The y-coordinate of the edge's source.
 * @param {number} targetX - The x-coordinate of the edge's target.
 * @param {number} targetY - The y-coordinate of the edge's target.
 * @param {string} strokeColor - The color of the edge stroke.
 * @param {boolean} animated - Whether the edge should be animated.
 * @param {number} strokeWidth - The width of the edge stroke.
 * @returns {JSX.Element} - React component rendering the edge.
 */
function DefaultEdge({ id, sourceX, sourceY, targetX, targetY, strokeColor, animated, strokeWidth }) {
  // Define styles for the edge
  const edgeStyle = {
    stroke: strokeColor || '#464646', // Default to a dark gray color if strokeColor is not provided
    animated: animated !== undefined ? animated : true, // Enable animation for the edge if not specified
    strokeWidth: strokeWidth !== undefined ? strokeWidth : 2, // Set the stroke width to 2 if not specified
  };

  // Render the edge component
  return (
    <BezierEdge
      id={id}
      sourceX={sourceX}
      sourceY={sourceY}
      targetX={targetX}
      targetY={targetY}
      style={edgeStyle}
    />
  );
}

export default DefaultEdge;
