import { useState } from 'react';
import { AlertTriangle, Loader, CheckCircle } from 'lucide-react';
import { rca } from '../api/client';

interface RCAResult {
  failure_description: string;
  five_why_analysis: Record<string, string>;
  fishbone_diagram: Record<string, string[]>;
  recommendations: string[];
  evidence_summary: string;
  confidence_score: number;
}

export function RCADisplay() {
  const [failureDescription, setFailureDescription] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<RCAResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!failureDescription.trim() || isAnalyzing) return;

    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const response = await rca.analyze(failureDescription.trim());
      setResult(normalizeRCAResult(response.data, failureDescription.trim()));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const normalizeRCAResult = (data: any, fallbackDescription: string): RCAResult => {
    const fiveWhy = Array.isArray(data.five_why_analysis)
      ? Object.fromEntries(
          data.five_why_analysis.slice(0, 5).map((item: any, index: number) => [
            `why_${index + 1}`,
            item.answer || item.question || String(item),
          ])
        )
      : data.five_why_analysis || {};

    const fishbone = Object.fromEntries(
      Object.entries(data.fishbone_diagram || {}).map(([category, factors]) => [
        category.toLowerCase(),
        Array.isArray(factors)
          ? factors.map((factor: any) =>
              typeof factor === 'string'
                ? factor
                : factor.factor || factor.description || JSON.stringify(factor)
            )
          : [],
      ])
    );

    const recommendations = Array.isArray(data.recommendations)
      ? data.recommendations.map((rec: any) =>
          typeof rec === 'string'
            ? rec
            : [rec.title, rec.description].filter(Boolean).join(': ') || JSON.stringify(rec)
        )
      : [];

    return {
      failure_description: data.failure_description || fallbackDescription,
      five_why_analysis: fiveWhy,
      fishbone_diagram: fishbone,
      recommendations,
      evidence_summary:
        data.evidence_summary ||
        data.ai_analysis ||
        `Evidence collected from ${data.evidence?.document_chunks ?? 0} document chunks and ${data.evidence?.graph_entities ?? 0} graph entities.`,
      confidence_score: data.confidence_score ?? data.confidence ?? 0,
    };
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Root Cause Analysis
        </h1>
        <p className="text-gray-600">
          Describe a failure or incident for AI-powered RCA
        </p>
      </div>

      {/* Input Form */}
      <form onSubmit={handleAnalyze} className="mb-8">
        <textarea
          value={failureDescription}
          onChange={(e) => setFailureDescription(e.target.value)}
          placeholder="Describe the failure or incident in detail..."
          rows={6}
          disabled={isAnalyzing}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-industrial-500 disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={!failureDescription.trim() || isAnalyzing}
          className="mt-4 px-6 py-3 bg-industrial-500 text-white rounded-lg hover:bg-industrial-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isAnalyzing ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <AlertTriangle className="w-5 h-5" />
              <span>Analyze Root Cause</span>
            </>
          )}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Confidence Score */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center space-x-3">
            <CheckCircle className="w-6 h-6 text-green-600" />
            <div>
              <p className="font-semibold text-green-900">Analysis Complete</p>
              <p className="text-sm text-green-700">
                Confidence: {(result.confidence_score * 100).toFixed(1)}%
              </p>
            </div>
          </div>

          {/* 5-Why Analysis */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              5-Why Analysis
            </h2>
            <div className="space-y-3">
              {Object.entries(result.five_why_analysis).map(([key, value], index) => (
                <div key={key} className="flex space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-industrial-100 rounded-full flex items-center justify-center font-semibold text-industrial-700">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-800">{value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Fishbone Diagram */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Fishbone Diagram (Contributing Factors)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(result.fishbone_diagram).map(([category, factors]) => (
                <div key={category} className="border border-gray-200 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-800 mb-2 capitalize">
                    {category}
                  </h3>
                  <ul className="space-y-1">
                    {factors.map((factor, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <span className="mr-2">•</span>
                        <span>{factor}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Recommendations
            </h2>
            <ul className="space-y-3">
              {result.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-industrial-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {idx + 1}
                  </div>
                  <p className="text-gray-700 flex-1">{rec}</p>
                </li>
              ))}
            </ul>
          </div>

          {/* Evidence Summary */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Evidence Summary
            </h2>
            <p className="text-gray-700 whitespace-pre-wrap">
              {result.evidence_summary}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
