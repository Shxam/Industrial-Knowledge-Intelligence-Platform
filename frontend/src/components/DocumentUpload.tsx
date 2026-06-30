import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, XCircle, Loader } from 'lucide-react';
import { documents } from '../api/client';
import { toast } from 'react-toastify';

interface UploadStatus {
  fileName: string;
  status: 'uploading' | 'success' | 'error';
  message?: string;
  documentId?: string;
}

export function DocumentUpload() {
  const [uploads, setUploads] = useState<UploadStatus[]>([]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      // Add to uploads list with uploading status
      setUploads((prev) => [
        ...prev,
        { fileName: file.name, status: 'uploading' },
      ]);

      try {
        const response = await documents.upload(file);
        const documentId = response.data.document_id;
        
        // Update status to success
        setUploads((prev) =>
          prev.map((upload) =>
            upload.fileName === file.name && upload.status === 'uploading'
              ? { ...upload, status: 'success', documentId, message: 'Upload successful' }
              : upload
          )
        );
        
        toast.success(`"${file.name}" uploaded successfully!`);
      } catch (error: any) {
        // Update status to error
        const errorMsg = error.response?.data?.detail || 'Upload failed';
        setUploads((prev) =>
          prev.map((upload) =>
            upload.fileName === file.name && upload.status === 'uploading'
              ? {
                  ...upload,
                  status: 'error',
                  message: errorMsg,
                }
              : upload
          )
        );
        
        toast.error(`Failed to upload "${file.name}": ${errorMsg}`);
      }
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/markdown': ['.md'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    onDropRejected: (fileRejections) => {
      fileRejections.forEach((rejection) => {
        const errors = rejection.errors.map((e) => e.message).join(', ');
        toast.error(`"${rejection.file.name}": ${errors}`);
      });
    },
  });

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Documents</h2>
        <p className="text-gray-600">
          Upload your industrial documents for AI-powered analysis
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-industrial-500 bg-industrial-50 scale-105'
            : 'border-gray-300 hover:border-industrial-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />
        <Upload
          className={`w-16 h-16 mx-auto mb-4 transition-colors ${
            isDragActive ? 'text-industrial-500' : 'text-gray-400'
          }`}
        />
        {isDragActive ? (
          <p className="text-lg text-industrial-600 font-medium">
            Drop the files here...
          </p>
        ) : (
          <>
            <p className="text-lg text-gray-700 font-medium mb-2">
              Drag & drop files here, or click to select
            </p>
            <p className="text-sm text-gray-500 mb-4">
              Supported formats: PDF, TXT, DOCX, MD
            </p>
            <p className="text-xs text-gray-400">
              Maximum file size: 50MB
            </p>
          </>
        )}
      </div>

      {uploads.length > 0 && (
        <div className="mt-8 space-y-3">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Upload Status</h3>
            {uploads.filter((u) => u.status === 'success').length > 0 && (
              <button
                onClick={() => setUploads([])}
                className="text-sm text-gray-600 hover:text-gray-900"
              >
                Clear completed
              </button>
            )}
          </div>
          {uploads.map((upload, index) => (
            <div
              key={index}
              className={`flex items-center justify-between p-4 bg-white border rounded-lg shadow-sm transition-all ${
                upload.status === 'success'
                  ? 'border-green-200 bg-green-50'
                  : upload.status === 'error'
                  ? 'border-red-200 bg-red-50'
                  : 'border-gray-200'
              }`}
            >
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <FileText className="w-5 h-5 text-gray-500 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-800 truncate">{upload.fileName}</p>
                  {upload.message && (
                    <p
                      className={`text-sm ${
                        upload.status === 'success'
                          ? 'text-green-600'
                          : upload.status === 'error'
                          ? 'text-red-600'
                          : 'text-gray-500'
                      }`}
                    >
                      {upload.message}
                    </p>
                  )}
                </div>
              </div>
              <div className="ml-4 flex-shrink-0">
                {upload.status === 'uploading' && (
                  <Loader className="w-5 h-5 text-industrial-500 animate-spin" />
                )}
                {upload.status === 'success' && (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                )}
                {upload.status === 'error' && (
                  <XCircle className="w-5 h-5 text-red-500" />
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
