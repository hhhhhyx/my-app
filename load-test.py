import requests
import time
import random
from datetime import datetime
import json

hosts = ['http://localhost/foo', 'http://localhost/bar']

def single_request_test():
    url = random.choice(hosts)
    start_time = time.time()

    try:
        response = requests.get(url, timeout=10) 
        response_time = round((time.time() - start_time) * 1000, 2)

        return {
            'url': url,
            'status_code': response.status_code,
            'response_time_ms': response_time,
            'success': response.status_code == 200,
            'timestamp': datetime.now()
        }
    
    except Exception as e: 
        return {
            'url': url,
            'status_code': 'ERROR',
            'response_time_ms': -1,
            'success': False,
            'error': str(e),
            'timestamp': datetime.now()
        }

def multi_request_test():
    total_requests = 10
    results = []

    for i in range(total_requests):
        result = single_request_test()
        results.append(result)

        time.sleep(random.uniform(0.1, 0.5))
    
    success_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]


    avg_time = 0
    p90 = p95 = p99 = 0
    failed_rate = 0

    if success_requests:
        response_times = [r['response_time_ms'] for r in success_requests]
        response_times.sort()
        n = len(response_times)
        
        response_times.sort()
        
        avg_time = sum(response_times) / n
        p90 = response_times[int(n * 0.9)] if n > 0 else 0
        p95 = response_times[int(n * 0.95)] if n > 0 else 0
        p99 = response_times[int(n * 0.99)] if n > 0 else 0

    total_success = len(success_requests)
    total_failed = len(failed_requests)
    success_rate = (total_success / total_requests) * 100
    failed_rate = (total_failed / total_requests) * 100

    # req/s
    total_time = max(r['timestamp'] for r in results) - min(r['timestamp'] for r in results)  
    total_seconds = total_time.total_seconds() if total_time.total_seconds() > 0 else 1
    requests_per_second = total_success / total_seconds
    
    report = {
        'total_requests': total_requests,
        'successful_requests': total_success,
        'failed_requests': total_failed,
        'success_rate': round(success_rate, 2),
        'failed_rate': round(failed_rate, 2),
        'throughput': round(requests_per_second, 2),
        'response_times': {
            'avg': round(avg_time, 2),
            'p90': round(p90, 2),
            'p95': round(p95, 2),
            'p99': round(p99, 2)
        }
    }

    with open('load_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
    
    return report

def print_report(report):
    print("\n" + "="*30)
    print("REPORT")
    print("="*30)
    
    print(f"Total Requests: {report['total_requests']}")
    print(f"Successful: {report['successful_requests']}")
    print(f"Failed: {report['failed_requests']}")
    print(f"Success Rate: {report['success_rate']}%")
    print(f"Error Rate: {report['failed_rate']}%")
    print(f"Throughput: {report['throughput']} req/s")
    
    print("\nRESPONSE TIMES (ms):")
    print(f"  Average: {report['response_times']['avg']}")
    print(f"  P90: {report['response_times']['p90']}")
    print(f"  P95: {report['response_times']['p95']}")
    print(f"  P99: {report['response_times']['p99']}")
    print("="*60)

if __name__ == "__main__":
    print("===Start load test===")
    report = multi_request_test()
    print_report(report)
