import { useState, useEffect } from 'react';
import { FileText, Trash2, CheckCircle, Clock, XCircle, Loader, RefreshCw } from 'lucide-react';
import { documents } from '../api/client';
import { toast } from 'react-toastify';

interface Document {
  id: string;
  filename: string;
  upload_date: string;
  status: 'processing' | 'completed' | 'failed';
  size?: number;
  chunks?: number;
}

export function DocumentList() {
  const [documentList, setDocumentList] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeleting, setIsDeleting] = useState<string | null>(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setIsLoading(true);
    try {
      const response = await documents.list();
      setDocumentList(response.data.documents || []);
    } catch (error: any) {
      console.error('Failed to fetch documents:', error);
      toast.error('Failed to load documents');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (documentId: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }

    setIsDeleting(documentId);
    try {
      await documents.delete(documentId);
      setDocumentList(documentList.filter((doc) => doc.id !== documentId));
      toast.success(`Deleted "${filename}"`);
    } catch (error: any) {
      console.error('Failed to delete document:', error);
      toast.error('Failed to delete document');
    } finally {
      setIsDeleting(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatSize = (bytes?: number) => {
    if (!bytes) return 'Unknown';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'processing':
        return <Clock className="w-5 h-5 text-yellow-500 animate-pulse" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'processing':
        return 'Processing';
      case 'failed':
        return 'Failed';
      default:
        return 'Unknown';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-700 bg-green-50';
      case 'processing':
        return 'text-yellow-700 bg-yellow-50';
      case 'failed':
        return 'text-red-700 bg-red-50';
      default:
        return 'text-gray-700 bg-gray-50';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader className="w-8 h-8 text-industrial-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Document Library</h2>
          <p className="text-gray-600 mt-1">
            {documentList.length} document{documentList.length !== 1 ? 's' : ''} uploaded
          </p>
        </div>
        <button
          onClick={fetchDocuments}
          className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center space-x-2"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Refresh</span>
        </button>
      </div>

      {documentList.length === 0 ? (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-gray-600 text-lg mb-2">No documents uploaded yet</p>
          <p className="text-gray-500 text-sm">
            Upload documents from the "Upload Documents" tab to get started
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {documentList.map((doc) => (
            <div
              key={doc.id}
              className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  <FileText className="w-10 h-10 text-gray-400 flex-shrink-0" />
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 truncate">
                      {doc.filename}
                    </h3>
                    <div className="flex items-center space-x-4 mt-1 text-sm text-gray-500">
                      <span>Uploaded: {formatDate(doc.upload_date)}</span>
                      {doc.size && <span>Size: {formatSize(doc.size)}</span>}
                      {doc.chunks && <span>Chunks: {doc.chunks}</span>}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-4">
                  <div
                    className={`flex items-center space-x-2 px-3 py-1 rounded-full ${getStatusColor(
                      doc.status
                    )}`}
                  >
                    {getStatusIcon(doc.status)}
                    <span className="text-sm font-medium">
                      {getStatusText(doc.status)}
                    </span>
                  </div>

                  <button
                    onClick={() => handleDelete(doc.id, doc.filename)}
                    disabled={isDeleting === doc.id}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Delete document"
                  >
                    {isDeleting === doc.id ? (
                      <Loader className="w-5 h-5 animate-spin" />
                    ) : (
                      <Trash2 className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
