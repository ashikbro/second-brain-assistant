import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { graphService } from '../services/api';

const GRAPH_WIDTH = 800;
const GRAPH_HEIGHT = 600;
const MIN_STROKE_WIDTH = 2;
const MAX_STROKE_WIDTH = 5;

const KnowledgeGraph = () => {
  const svgRef = useRef();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadGraph();
  }, []);

  const loadGraph = async () => {
    setLoading(true);
    setError('');
    try {
      // Build the graph first
      await graphService.buildGraph();
      // Then fetch and display it
      const response = await graphService.getGraph();
      renderGraph(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load graph');
    } finally {
      setLoading(false);
    }
  };

  const renderGraph = (data) => {
    const svg = d3.select(svgRef.current);

    svg.selectAll('*').remove();

    if (!data.nodes || data.nodes.length === 0) {
      svg.append('text')
        .attr('x', GRAPH_WIDTH / 2)
        .attr('y', GRAPH_HEIGHT / 2)
        .attr('text-anchor', 'middle')
        .style('font-size', '16px')
        .style('fill', '#666')
        .text('No notes yet. Create some notes to see the knowledge graph!');
      return;
    }

    svg.attr('width', GRAPH_WIDTH).attr('height', GRAPH_HEIGHT);

    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.relationships)
        .id(d => d.id)
        .distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(GRAPH_WIDTH / 2, GRAPH_HEIGHT / 2));

    const link = svg.append('g')
      .selectAll('line')
      .data(data.relationships)
      .enter().append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', d => Math.min(d.weight * MIN_STROKE_WIDTH, MAX_STROKE_WIDTH));

    const node = svg.append('g')
      .selectAll('g')
      .data(data.nodes)
      .enter().append('g')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    node.append('circle')
      .attr('r', 10)
      .attr('fill', '#667eea');

    node.append('text')
      .text(d => d.title)
      .attr('x', 15)
      .attr('y', 5)
      .style('font-size', '12px')
      .style('fill', '#333');

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
  };

  return (
    <div className="graph-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2>Knowledge Graph</h2>
        <button className="btn btn-primary" onClick={loadGraph} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh Graph'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      {loading ? (
        <div className="loading">Loading graph...</div>
      ) : (
        <svg ref={svgRef}></svg>
      )}
    </div>
  );
};

export default KnowledgeGraph;
