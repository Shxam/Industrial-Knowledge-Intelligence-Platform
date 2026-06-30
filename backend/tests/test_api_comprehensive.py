"""
Comprehensive API Testing Suite for IKIP
Tests all major endpoints and user flows
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, Any, List

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = 30

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}! {msg}{Colors.ENDC}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.ENDC}")

def print_section(msg: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.tests = []
    
    def add_pass(self, test_name: str, details: str = ""):
        self.passed += 1
        self.tests.append({"name": test_name, "status": "PASS", "details": details})
        print_success(f"{test_name}: {details}")
    
    def add_fail(self, test_name: str, details: str = ""):
        self.failed += 1
        self.tests.append({"name": test_name, "status": "FAIL", "details": details})
        print_error(f"{test_name}: {details}")
    
    def add_warning(self, test_name: str, details: str = ""):
        self.warnings += 1
        self.tests.append({"name": test_name, "status": "WARNING", "details": details})
        print_warning(f"{test_name}: {details}")
    
    def summary(self):
        print_section("TEST SUMMARY")
        total = self.passed + self.failed + self.warnings
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed} ({self.passed/total*100:.1f}%){Colors.ENDC}")
        print(f"{Colors.RED}Failed: {self.failed} ({self.failed/total*100:.1f}%){Colors.ENDC}")
        print(f"{Colors.YELLOW}Warnings: {self.warnings} ({self.warnings/total*100:.1f}%){Colors.ENDC}")
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.ENDC}\n")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️  SOME TESTS FAILED ⚠️{Colors.ENDC}\n")
            print("Failed tests:")
            for test in self.tests:
                if test["status"] == "FAIL":
                    print(f"  - {test['name']}: {test['details']}")


results = TestResults()


def test_health_endpoint():
    """Test health check endpoint"""
    print_section("1. HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results.add_pass("Health endpoint", f"Status: {data.get('status')}")
            
            # Check services
            services = data.get('services', {})
            for service, status in services.items():
                if status == 'healthy':
                    results.add_pass(f"Service: {service}", "Healthy")
                else:
                    results.add_warning(f"Service: {service}", f"Status: {status}")
        else:
            results.add_fail("Health endpoint", f"Status code: {response.status_code}")
    
    except Exception as e:
        results.add_fail("Health endpoint", str(e))


def test_document_upload(test_file_path: str = None) -> str:
    """Test document upload endpoint"""
    print_section("2. DOCUMENT UPLOAD")
    
    # Create a test file if none provided
    if test_file_path is None or not os.path.exists(test_file_path):
        print_info("Creating test document...")
        test_file_path = "test_document.txt"
        with open(test_file_path, "w") as f:
            f.write("""
# Test Industrial Document

## Equipment: Pump P-101

### Specifications
- Type: Centrifugal Pump
- Model: XYZ-500
- Flow Rate: 500 GPM
- Pressure: 150 PSI
- Temperature: 80°C

### Maintenance Procedure
1. Shut down pump and lock out power
2. Drain pump casing
3. Remove impeller
4. Inspect for wear
5. Replace seals if needed
6. Reassemble and test

### Common Failures
- Seal leakage due to wear
- Bearing failure from overload
- Impeller erosion from contamination

### Safety Notes
- Always use PPE
- Follow LOTO procedures
- Check for residual pressure
            """)
    
    doc_id = None
    
    try:
        # Upload document
        with open(test_file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{BASE_URL}/documents/upload",
                files=files,
                timeout=TIMEOUT
            )
        
        if response.status_code == 200:
            data = response.json()
            doc_id = data.get("document_id")
            results.add_pass("Document upload", f"ID: {doc_id}")
        else:
            results.add_fail("Document upload", f"Status: {response.status_code}")
            return None
    
    except Exception as e:
        results.add_fail("Document upload", str(e))
        return None
    
    # Check status
    if doc_id:
        try:
            # Wait a bit for processing
            time.sleep(2)
            
            response = requests.get(
                f"{BASE_URL}/documents/{doc_id}/status",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                chunks = data.get("chunks", 0)
                results.add_pass("Document status", f"Status: {status}, Chunks: {chunks}")
            else:
                results.add_warning("Document status", f"Status code: {response.status_code}")
        
        except Exception as e:
            results.add_warning("Document status", str(e))
    
    return doc_id


def test_query_endpoint(doc_id: str = None):
    """Test query endpoint"""
    print_section("3. QUERY & RAG")
    
    test_queries = [
        "What is the flow rate of Pump P-101?",
        "What are the common failures of the pump?",
        "What safety procedures should be followed?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        try:
            print_info(f"Query {i}: {query}")
            
            payload = {
                "question": query,
                "strategy": "hybrid",
                "top_k": 5
            }
            
            response = requests.post(
                f"{BASE_URL}/query",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "")
                citations = data.get("citations", [])
                confidence = data.get("confidence", 0)
                
                results.add_pass(
                    f"Query {i}",
                    f"Answer length: {len(answer)} chars, Citations: {len(citations)}, Confidence: {confidence:.2f}"
                )
                
                # Print answer snippet
                answer_snippet = answer[:150] + "..." if len(answer) > 150 else answer
                print(f"  Answer: {answer_snippet}")
            else:
                results.add_fail(f"Query {i}", f"Status: {response.status_code}")
        
        except Exception as e:
            results.add_fail(f"Query {i}", str(e))


def test_rca_endpoint():
    """Test RCA analysis endpoint"""
    print_section("4. RCA AGENT")
    
    failure_description = """
    Pump P-101 experienced seal failure on June 25, 2026.
    Operator noticed leakage during routine inspection.
    Pump had been running continuously for 6 months without maintenance.
    Recent changes include higher throughput demand and increased operating temperature.
    Previous seal failures occurred in March and April 2026.
    """
    
    try:
        print_info("Running RCA analysis...")
        
        payload = {
            "failure_description": failure_description
        }
        
        response = requests.post(
            f"{BASE_URL}/rca/analyze",
            json=payload,
            timeout=60  # RCA can take longer
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            why_analysis = data.get("why_analysis", [])
            fishbone = data.get("fishbone_diagram", {})
            recommendations = data.get("recommendations", [])
            confidence = data.get("confidence_score", 0)
            
            results.add_pass(
                "RCA analysis",
                f"5-Why: {len(why_analysis)} levels, Recommendations: {len(recommendations)}, Confidence: {confidence:.2f}"
            )
            
            # Print summary
            print(f"\n  Root Causes Found: {len(why_analysis)}")
            print(f"  Recommendations: {len(recommendations)}")
            if recommendations:
                print(f"  Top Recommendation: {recommendations[0].get('action', 'N/A')[:80]}...")
        
        else:
            results.add_fail("RCA analysis", f"Status: {response.status_code}")
    
    except Exception as e:
        results.add_fail("RCA analysis", str(e))


def test_graph_endpoints():
    """Test knowledge graph endpoints"""
    print_section("5. KNOWLEDGE GRAPH")
    
    # Test graph stats
    try:
        response = requests.get(f"{BASE_URL}/graph/stats", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            nodes = data.get("total_nodes", 0)
            edges = data.get("total_relationships", 0)
            results.add_pass("Graph stats", f"Nodes: {nodes}, Edges: {edges}")
        else:
            results.add_warning("Graph stats", f"Status: {response.status_code}")
    
    except Exception as e:
        results.add_warning("Graph stats", str(e))
    
    # Test graph visualization
    try:
        response = requests.get(f"{BASE_URL}/graph/visualize", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            nodes = len(data.get("nodes", []))
            edges = len(data.get("edges", []))
            results.add_pass("Graph visualize", f"Nodes: {nodes}, Edges: {edges}")
        else:
            results.add_warning("Graph visualize", f"Status: {response.status_code}")
    
    except Exception as e:
        results.add_warning("Graph visualize", str(e))
    
    # Test entity search
    try:
        response = requests.get(
            f"{BASE_URL}/graph/search",
            params={"query": "pump"},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            entities = len(data.get("entities", []))
            results.add_pass("Graph search", f"Found {entities} entities")
        else:
            results.add_warning("Graph search", f"Status: {response.status_code}")
    
    except Exception as e:
        results.add_warning("Graph search", str(e))


def test_document_deletion(doc_id: str):
    """Test document deletion"""
    print_section("6. DOCUMENT DELETION")
    
    if not doc_id:
        results.add_warning("Document deletion", "No document ID to delete")
        return
    
    try:
        response = requests.delete(
            f"{BASE_URL}/documents/{doc_id}",
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            results.add_pass("Document deletion", f"Deleted doc: {doc_id}")
        else:
            results.add_warning("Document deletion", f"Status: {response.status_code}")
    
    except Exception as e:
        results.add_warning("Document deletion", str(e))


def test_error_handling():
    """Test error handling"""
    print_section("7. ERROR HANDLING")
    
    # Test invalid document ID
    try:
        response = requests.get(f"{BASE_URL}/documents/invalid-id/status", timeout=5)
        if response.status_code == 404:
            results.add_pass("Error handling", "Invalid ID returns 404")
        else:
            results.add_warning("Error handling", f"Expected 404, got {response.status_code}")
    except Exception as e:
        results.add_warning("Error handling", str(e))
    
    # Test empty query
    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": ""},
            timeout=5
        )
        if response.status_code == 422:
            results.add_pass("Error handling", "Empty query returns 422")
        else:
            results.add_warning("Error handling", f"Expected 422, got {response.status_code}")
    except Exception as e:
        results.add_warning("Error handling", str(e))


def test_performance():
    """Test performance metrics"""
    print_section("8. PERFORMANCE")
    
    # Test query response time
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": "What is the pump flow rate?", "strategy": "hybrid"},
            timeout=TIMEOUT
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            if elapsed < 5:
                results.add_pass("Query performance", f"{elapsed:.2f}s (Target: <5s)")
            elif elapsed < 10:
                results.add_warning("Query performance", f"{elapsed:.2f}s (Slow but acceptable)")
            else:
                results.add_fail("Query performance", f"{elapsed:.2f}s (Too slow!)")
        else:
            results.add_warning("Query performance", "Query failed")
    
    except Exception as e:
        results.add_warning("Query performance", str(e))


def run_all_tests(test_file: str = None):
    """Run all tests in sequence"""
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"IKIP - Comprehensive API Test Suite")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    print_info(f"API Base URL: {BASE_URL}")
    print_info(f"Timeout: {TIMEOUT}s\n")
    
    # Run tests
    test_health_endpoint()
    doc_id = test_document_upload(test_file)
    
    # Wait for document processing
    if doc_id:
        print_info("Waiting for document processing (10s)...")
        time.sleep(10)
    
    test_query_endpoint(doc_id)
    test_rca_endpoint()
    test_graph_endpoints()
    test_error_handling()
    test_performance()
    
    if doc_id:
        test_document_deletion(doc_id)
    
    # Print summary
    results.summary()
    
    # Return exit code
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    # Check if test file provided
    test_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Run tests
    exit_code = run_all_tests(test_file)
    
    # Exit with appropriate code
    sys.exit(exit_code)
