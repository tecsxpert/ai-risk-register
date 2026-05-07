import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[60vh] flex items-center justify-center p-6">
          <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md w-full text-center">

            {/* Icon */}
            <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-5">
              <span className="text-4xl">⚠️</span>
            </div>

            {/* Title */}
            <h2 className="text-xl font-bold text-gray-800 mb-2">
              Something went wrong
            </h2>
            <p className="text-gray-500 text-sm mb-6">
              This page encountered an unexpected error. Try refreshing or
              going back to the dashboard.
            </p>

            {/* Error detail — dev mode */}
            {this.state.error && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-5 text-left">
                <p className="text-xs font-semibold text-gray-500 mb-1">
                  Error details:
                </p>
                <p className="text-xs text-red-600 font-mono break-all">
                  {this.state.error.toString()}
                </p>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-3 justify-center">
              <button
                onClick={this.handleReset}
                className="bg-blue-900 text-white px-5 py-2 rounded-lg hover:bg-blue-800 transition text-sm"
              >
                Try Again
              </button>
              <button
                onClick={() => (window.location.href = "/dashboard")}
                className="border border-gray-300 text-gray-700 px-5 py-2 rounded-lg hover:bg-gray-50 transition text-sm"
              >
                Go to Dashboard
              </button>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;