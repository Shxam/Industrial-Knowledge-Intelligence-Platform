"""
Test script for IKIP API
Run this after implementing the core RAG pipeline
"""
import requests
import json
import time
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 30


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_detailed_health():
    """Test detailed health endpoint"""
    print("\n" + "="*60)
    print("Testing Detailed Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health/detailed", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_document_upload(file_path: str):
    """Test document upload"""
    print("\n" + "="*60)
    print("Testing Document Upload")
    print("="*60)
    
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f, 'application/pdf')}
            response = requests.post(
                f"{API_BASE_URL}/documents/upload",
                files=files,
                timeout=TIMEOUT
            )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            return response.json().get('document_id')
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_document_status(document_id: str):
    """Test document status check"""
    print("\n" + "="*60)
    print("Testing Document Status")
    print("="*60)
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/documents/{document_id}/status",
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_query(query_text: str, stream: bool = False):
    """Test query endpoint"""
    print("\n" + "="*60)
    print(f"Testing Query: '{query_text}'")
    print("="*60)
    
    try:
        payload = {
            "query": query_text,
            "stream": stream,
            "top_k": 5,
            "confidence_threshold": 0.5
        }
        
        response = requests.post(
            f"{API_BASE_URL}/query",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"Status: {response.status_code}")
        
        if stream:
            print("Streaming response:")
            for line in response.iter_lines():
                if line:
                    print(line.decode('utf-8'))
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_graph_entities():
    """Test graph entities endpoint"""
    print("\n" + "="*60)
    print("Testing Knowledge Graph - List Entities")
    print("="*60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/graph/entities", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_rca():
    """Test RCA endpoint"""
    print("\n" + "="*60)
    print("Testing Root Cause Analysis")
    print("="*60)
    
    try:
        payload = {
            "equipment_tag": "P-101",
            "failure_mode": "Seal Leak"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/query/rca",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_compliance():
    """Test compliance endpoint"""
    print("\n" + "="*60)
    print("Testing Compliance Check")
    print("="*60)
    
    try:
        payload = {
            "regulation": "OISD-STD-105",
            "scope": "Emergency Shutdown Systems"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/query/compliance/check",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests(test_pdf_path: str = None):
    """Run all tests"""
    print("\n" + "="*60)
    print("  IKIP API Test Suite")
    print("="*60)
    
    results = {}
    
    # Basic health checks
    results['health'] = test_health()
    results['detailed_health'] = test_detailed_health()
    
    # Document upload (if PDF provided)
    doc_id = None
    if test_pdf_path:
        doc_id = test_document_upload(test_pdf_path)
        results['upload'] = doc_id is not None
        
        if doc_id:
            time.sleep(2)  # Wait for processing
            results['status'] = test_document_status(doc_id)
    
    # Query tests
    results['query_basic'] = test_query("What is this document about?", stream=False)
    results['query_stream'] = test_query("Explain the main topic", stream=True)
    
    # Advanced features
    results['graph'] = test_graph_entities()
    results['rca'] = test_rca()
    results['compliance'] = test_compliance()
    
    # Summary
    print("\n" + "="*60)
    print("  Test Results Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20s} : {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    return passed == total


if __name__ == "__main__":
    import sys
    
    # Check if PDF path provided
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if pdf_path:
        print(f"Using test PDF: {pdf_path}")
    else:
        print("No PDF provided - skipping document upload tests")
        print("Usage: python test_api.py <path-to-test-pdf>")
    
    # Run tests
    success = run_all_tests(pdf_path)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
