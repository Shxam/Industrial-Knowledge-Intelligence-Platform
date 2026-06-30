import { Loader } from 'lucide-react';

export function LoadingScreen() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gradient-to-br from-industrial-50 to-white">
      <div className="text-center">
        <div className="mb-6">
          <Loader className="w-16 h-16 text-industrial-600 animate-spin mx-auto" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">IKIP</h1>
        <p className="text-gray-600">Industrial Knowledge Intelligence Platform</p>
        <p className="text-sm text-gray-500 mt-4">Loading application...</p>
      </div>
    </div>
  );
}
