#!/usr/bin/env python3
"""
Test script for the kernel evaluation tool
"""

import json
import os
import sys
import subprocess

def test_rubric_structure():
    """Test that rubric.json has the correct structure."""
    print("Testing rubric structure...")
    
    with open('rubric.json', 'r') as f:
        rubric = json.load(f)
    
    # Check top-level keys
    assert 'kernel_primitives' in rubric, "Missing kernel_primitives"
    assert 'os_platform_services' in rubric, "Missing os_platform_services"
    assert 'metadata' in rubric, "Missing metadata"
    
    # Check kernel primitives count
    assert len(rubric['kernel_primitives']) == 10, f"Expected 10 kernel primitives, got {len(rubric['kernel_primitives'])}"
    
    # Check OS services count
    assert len(rubric['os_platform_services']) == 8, f"Expected 8 OS services, got {len(rubric['os_platform_services'])}"
    
    # Verify each kernel primitive has required fields
    required_fields = ['weight', 'criticality', 'description', 'evidence_cues', 'target_functions', 'target_sloc']
    for name, spec in rubric['kernel_primitives'].items():
        for field in required_fields:
            assert field in spec, f"Kernel primitive '{name}' missing field '{field}'"
        assert isinstance(spec['evidence_cues'], list), f"evidence_cues for '{name}' must be a list"
        assert len(spec['evidence_cues']) > 0, f"evidence_cues for '{name}' must not be empty"
    
    # Verify each OS service has required fields
    for name, spec in rubric['os_platform_services'].items():
        for field in required_fields:
            assert field in spec, f"OS service '{name}' missing field '{field}'"
        assert isinstance(spec['evidence_cues'], list), f"evidence_cues for '{name}' must be a list"
        assert len(spec['evidence_cues']) > 0, f"evidence_cues for '{name}' must not be empty"
    
    print("✓ Rubric structure is valid")
    return True

def test_evaluator():
    """Test that the evaluator runs successfully."""
    print("\nTesting evaluator on example kernel...")
    
    # Run the evaluator
    result = subprocess.run(
        ['python3', 'evaluate.py', 'examples/simple_kernel/'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Evaluator failed with return code {result.returncode}"
    
    # Check that output file was created
    assert os.path.exists('evaluation_results.json'), "evaluation_results.json was not created"
    
    # Load and validate results
    with open('evaluation_results.json', 'r') as f:
        results = json.load(f)
    
    assert 'kernel_primitives' in results, "Results missing kernel_primitives"
    assert 'os_services' in results, "Results missing os_services"
    assert 'summary' in results, "Results missing summary"
    
    # Check summary has required fields
    summary = results['summary']
    assert 'kernel_primitives_score' in summary, "Summary missing kernel_primitives_score"
    assert 'os_services_score' in summary, "Summary missing os_services_score"
    assert 'overall_score' in summary, "Summary missing overall_score"
    assert 'total_files_scanned' in summary, "Summary missing total_files_scanned"
    
    # Verify scores are within valid range
    assert 0 <= summary['kernel_primitives_score'] <= 100, "kernel_primitives_score out of range"
    assert 0 <= summary['os_services_score'] <= 100, "os_services_score out of range"
    assert 0 <= summary['overall_score'] <= 100, "overall_score out of range"
    
    print(f"✓ Evaluator ran successfully")
    print(f"  - Files scanned: {summary['total_files_scanned']}")
    print(f"  - Kernel score: {summary['kernel_primitives_score']:.1f}%")
    print(f"  - OS services score: {summary['os_services_score']:.1f}%")
    print(f"  - Overall score: {summary['overall_score']:.1f}%")
    
    return True

def test_kernel_primitives_list():
    """Test that all 10 kernel primitives are defined."""
    print("\nTesting kernel primitives list...")
    
    with open('rubric.json', 'r') as f:
        rubric = json.load(f)
    
    expected_primitives = [
        'boot',
        'scheduling',
        'process_thread_management',
        'memory',
        'interrupt_handling',
        'system_call_interface',
        'basic_io',
        'synchronisation',
        'timers_clock',
        'protection'
    ]
    
    for primitive in expected_primitives:
        assert primitive in rubric['kernel_primitives'], f"Missing kernel primitive: {primitive}"
    
    print("✓ All 10 kernel primitives are defined")
    return True

def test_os_services_list():
    """Test that all 8 OS services are defined."""
    print("\nTesting OS services list...")
    
    with open('rubric.json', 'r') as f:
        rubric = json.load(f)
    
    expected_services = [
        'virtual_memory',
        'driver_framework',
        'filesystem',
        'networking',
        'ipc',
        'security',
        'power_management',
        'profiling'
    ]
    
    for service in expected_services:
        assert service in rubric['os_platform_services'], f"Missing OS service: {service}"
    
    print("✓ All 8 OS services are defined")
    return True

def main():
    """Run all tests."""
    print("Running tests for kernel evaluation system\n")
    print("="*70)
    
    try:
        test_rubric_structure()
        test_kernel_primitives_list()
        test_os_services_list()
        test_evaluator()
        
        print("\n" + "="*70)
        print("All tests passed! ✓")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
