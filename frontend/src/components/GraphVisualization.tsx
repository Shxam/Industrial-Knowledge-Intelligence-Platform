import { useState, useEffect, useRef } from 'react';
import { Network, Loader, Search, RefreshCw, ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';
import { graph } from '../api/client';
import cytoscape from 'cytoscape';

interface GraphStats {
  nodes: number;
  relationships: number;
  node_types: Record<string, number>;
  relationship_types: Record<string, number>;
}

interface GraphData {
  nodes: Array<{
    id: string;
    label: string;
    type: string;
    properties?: Record<string, any>;
  }>;
  edges: Array<{
    source: string;
    target: string;
    relationship: string;
  }>;
}

export function GraphVisualization() {
  const [stats, setStats] = useState<GraphStats | null>(null);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [isLoadingStats, setIsLoadingStats] = useState(true);
  const [isLoadingGraph, setIsLoadingGraph] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showGraph, setShowGraph] = useState(false);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  useEffect(() => {
    if (showGraph && graphData && containerRef.current && !cyRef.current) {
      initializeCytoscape();
    }
  }, [showGraph, graphData]);

  const fetchStats = async () => {
    setIsLoadingStats(true);
    setError(null);
    try {
      const response = await graph.stats();
      setStats(normalizeStats(response.data));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch graph stats');
    } finally {
      setIsLoadingStats(false);
    }
  };

  const fetchGraphData = async () => {
    setIsLoadingGraph(true);
    setError(null);
    try {
      const response = await graph.visualize(100);
      setGraphData(normalizeGraphData(response.data));
      setShowGraph(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch graph data');
    } finally {
      setIsLoadingGraph(false);
    }
  };

  const normalizeStats = (data: any): GraphStats => {
    const normalizeCountMap = (value: any): Record<string, number> => {
      if (Array.isArray(value)) {
        return Object.fromEntries(value.map((item) => [String(item), 0]));
      }
      return value || {};
    };

    return {
      nodes: data.nodes ?? data.node_count ?? 0,
      relationships: data.relationships ?? data.relationship_count ?? 0,
      node_types: normalizeCountMap(data.node_types),
      relationship_types: normalizeCountMap(data.relationship_types),
    };
  };

  const normalizeGraphData = (data: any): GraphData => ({
    nodes: (data.nodes || []).map((node: any) => {
      const source = node.data || node;
      return {
        id: source.id,
        label: source.label || source.text || source.id,
        type: source.type || 'entity',
        properties: source,
      };
    }),
    edges: (data.edges || []).map((edge: any, index: number) => {
      const source = edge.data || edge;
      return {
        source: source.source,
        target: source.target,
        relationship: source.relationship || source.label || source.type || `REL_${index + 1}`,
      };
    }),
  });

  const initializeCytoscape = () => {
    if (!containerRef.current || !graphData) return;

    // Color palette for different node types
    const nodeColors: Record<string, string> = {
      equipment: '#0ea5e9',
      process: '#10b981',
      material: '#f59e0b',
      person: '#8b5cf6',
      location: '#ef4444',
      document: '#6b7280',
      default: '#64748b',
    };

    const elements = [
      ...graphData.nodes.map((node) => ({
        data: {
          id: node.id,
          label: node.label,
          type: node.type,
          color: nodeColors[node.type.toLowerCase()] || nodeColors.default,
        },
      })),
      ...graphData.edges.map((edge, idx) => ({
        data: {
          id: `edge-${idx}`,
          source: edge.source,
          target: edge.target,
          label: edge.relationship,
        },
      })),
    ];

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(color)',
            label: 'data(label)',
            color: '#fff',
            'text-outline-color': 'data(color)',
            'text-outline-width': 2,
            'font-size': 12,
            width: 40,
            height: 40,
          },
        },
        {
          selector: 'edge',
          style: {
            width: 2,
            'line-color': '#cbd5e1',
            'target-arrow-color': '#cbd5e1',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            label: 'data(label)',
            'font-size': 10,
            color: '#64748b',
            'text-rotation': 'autorotate',
            'text-margin-y': -10,
          },
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 3,
            'border-color': '#0f172a',
          },
        },
      ],
      layout: {
        name: 'cose',
        animate: true,
        animationDuration: 1000,
        nodeRepulsion: 8000,
        idealEdgeLength: 100,
        edgeElasticity: 100,
      },
      minZoom: 0.3,
      maxZoom: 3,
      wheelSensitivity: 0.2,
    });

    // Add click handler for nodes
    cyRef.current.on('tap', 'node', (evt) => {
      const node = evt.target;
      console.log('Selected node:', node.data());
    });
  };

  const handleZoomIn = () => {
    if (cyRef.current) {
      cyRef.current.zoom(cyRef.current.zoom() * 1.2);
      cyRef.current.center();
    }
  };

  const handleZoomOut = () => {
    if (cyRef.current) {
      cyRef.current.zoom(cyRef.current.zoom() * 0.8);
      cyRef.current.center();
    }
  };

  const handleFit = () => {
    if (cyRef.current) {
      cyRef.current.fit();
    }
  };

  const handleReset = () => {
    if (cyRef.current) {
      cyRef.current.layout({ name: 'cose', animate: true }).run();
    }
  };

  const handleSearch = () => {
    if (!cyRef.current || !searchTerm) return;

    cyRef.current.nodes().removeClass('highlighted');
    const matchedNodes = cyRef.current.nodes().filter((node) =>
      node.data('label').toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (matchedNodes.length > 0) {
      matchedNodes.addClass('highlighted');
      cyRef.current.animate({
        fit: { eles: matchedNodes, padding: 50 },
        duration: 500,
      });
    }
  };

  if (isLoadingStats) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader className="w-8 h-8 text-industrial-500 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
        {error}
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div className="w-full max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Knowledge Graph
        </h1>
        <p className="text-gray-600">
          Explore entities and relationships extracted from your documents
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Network className="w-8 h-8 text-industrial-500" />
            <h2 className="text-xl font-bold text-gray-900">
              Graph Statistics
            </h2>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total Nodes:</span>
              <span className="text-2xl font-bold text-industrial-600">
                {stats.nodes}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total Relationships:</span>
              <span className="text-2xl font-bold text-industrial-600">
                {stats.relationships}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Node Types
          </h2>
          <div className="space-y-2">
            {Object.entries(stats.node_types).map(([type, count]) => (
              <div key={type} className="flex justify-between items-center">
                <span className="text-gray-700 capitalize">{type}:</span>
                <span className="font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Relationship Types */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Relationship Types
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {Object.entries(stats.relationship_types).map(([type, count]) => (
            <div
              key={type}
              className="bg-gray-50 border border-gray-200 rounded-lg p-4"
            >
              <p className="text-sm text-gray-600 mb-1">{type}</p>
              <p className="text-2xl font-bold text-industrial-600">{count}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive Visualization */}
      {!showGraph ? (
        <div className="bg-white border border-gray-200 rounded-lg p-12 text-center">
          <Network className="w-16 h-16 mx-auto mb-4 text-industrial-500" />
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Interactive Graph Visualization
          </h3>
          <p className="text-gray-600 mb-6">
            Explore your knowledge graph visually with interactive nodes and relationships
          </p>
          <button
            onClick={fetchGraphData}
            disabled={isLoadingGraph || stats.nodes === 0}
            className="px-6 py-3 bg-industrial-500 text-white rounded-lg hover:bg-industrial-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2 mx-auto"
          >
            {isLoadingGraph ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Loading Graph...</span>
              </>
            ) : (
              <>
                <Network className="w-5 h-5" />
                <span>Visualize Graph</span>
              </>
            )}
          </button>
          {stats.nodes === 0 && (
            <p className="text-sm text-gray-500 mt-4">
              Upload and process documents first to see the knowledge graph
            </p>
          )}
        </div>
      ) : (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          {/* Controls */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2 flex-1">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search nodes..."
                className="flex-1 max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-industrial-500"
              />
              <button
                onClick={handleSearch}
                className="px-4 py-2 bg-industrial-500 text-white rounded-lg hover:bg-industrial-600 transition-colors"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleZoomIn}
                className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title="Zoom In"
              >
                <ZoomIn className="w-5 h-5" />
              </button>
              <button
                onClick={handleZoomOut}
                className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title="Zoom Out"
              >
                <ZoomOut className="w-5 h-5" />
              </button>
              <button
                onClick={handleFit}
                className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title="Fit to Screen"
              >
                <Maximize2 className="w-5 h-5" />
              </button>
              <button
                onClick={handleReset}
                className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title="Reset Layout"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Graph Container */}
          <div
            ref={containerRef}
            className="w-full h-[600px] border border-gray-200 rounded-lg bg-gray-50"
          />

          {/* Legend */}
          <div className="mt-4 flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-[#0ea5e9]"></div>
              <span>Equipment</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-[#10b981]"></div>
              <span>Process</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-[#f59e0b]"></div>
              <span>Material</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-[#8b5cf6]"></div>
              <span>Person</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 rounded-full bg-[#ef4444]"></div>
              <span>Location</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
