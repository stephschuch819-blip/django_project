#!/usr/bin/env python
"""
Test script to verify IDOR protection is working correctly.
This script tests the security fixes implemented in the portal views.
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delegacy_portal.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from portal.models import BeneficiaryCase
from portal.views import get_beneficiary_case
from django.core.exceptions import PermissionDenied
from django.http import Http404


def add_session_to_request(request):
    """Helper to add session to request object"""
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    return request


def test_valid_case_access():
    """Test 1: Valid case access should work"""
    print("\n[TEST 1] Testing valid case access...")
    
    # Create a test case
    case = BeneficiaryCase.objects.filter(is_active=True).first()
    if not case:
        print("  [SKIP] No active cases found in database")
        return
    
    # Create request with valid session
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request = add_session_to_request(request)
    request.session['beneficiary_case_id'] = case.id
    
    try:
        retrieved_case = get_beneficiary_case(request)
        if retrieved_case.id == case.id:
            print("  [PASS] Valid case access successful")
        else:
            print("  [FAIL] Retrieved wrong case")
    except Exception as e:
        print(f"  [FAIL] Unexpected error: {e}")


def test_no_session():
    """Test 2: No session should raise PermissionDenied"""
    print("\n[TEST 2] Testing access without session...")
    
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request = add_session_to_request(request)
    # Don't set case_id in session
    
    try:
        get_beneficiary_case(request)
        print("  [FAIL] Should have raised PermissionDenied")
    except PermissionDenied as e:
        print(f"  [PASS] Correctly raised PermissionDenied: {e}")
    except Exception as e:
        print(f"  [FAIL] Wrong exception type: {e}")


def test_invalid_case_id():
    """Test 3: Invalid case_id should raise Http404"""
    print("\n[TEST 3] Testing access with invalid case_id...")
    
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request = add_session_to_request(request)
    request.session['beneficiary_case_id'] = 99999  # Non-existent ID
    
    try:
        get_beneficiary_case(request)
        print("  [FAIL] Should have raised Http404")
    except Http404 as e:
        print(f"  [PASS] Correctly raised Http404: {e}")
        # Check if session was cleared
        if 'beneficiary_case_id' not in request.session:
            print("  [PASS] Session was correctly cleared")
        else:
            print("  [FAIL] Session was not cleared")
    except Exception as e:
        print(f"  [FAIL] Wrong exception type: {e}")


def test_inactive_case():
    """Test 4: Inactive case should raise Http404"""
    print("\n[TEST 4] Testing access to inactive case...")
    
    # Find or create an inactive case
    inactive_case = BeneficiaryCase.objects.filter(is_active=False).first()
    if not inactive_case:
        # Create a temporary inactive case
        active_case = BeneficiaryCase.objects.filter(is_active=True).first()
        if not active_case:
            print("  [SKIP] No cases found in database")
            return
        # Temporarily deactivate
        active_case.is_active = False
        active_case.save()
        inactive_case = active_case
        should_reactivate = True
    else:
        should_reactivate = False
    
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request = add_session_to_request(request)
    request.session['beneficiary_case_id'] = inactive_case.id
    
    try:
        get_beneficiary_case(request)
        print("  [FAIL] Should have raised Http404 for inactive case")
    except Http404 as e:
        print(f"  [PASS] Correctly raised Http404: {e}")
    except Exception as e:
        print(f"  [FAIL] Wrong exception type: {e}")
    finally:
        # Reactivate if we deactivated it
        if should_reactivate:
            inactive_case.is_active = True
            inactive_case.save()


def test_view_decorator():
    """Test 5: Test the beneficiary_required decorator"""
    print("\n[TEST 5] Testing @beneficiary_required decorator...")
    
    client = Client()
    
    # Try to access protected view without login
    response = client.get('/dashboard/')
    
    if response.status_code == 302:  # Redirect
        if '/login/' in response.url or response.url == '/':
            print("  [PASS] Correctly redirected to login")
        else:
            print(f"  [FAIL] Redirected to wrong URL: {response.url}")
    else:
        print(f"  [FAIL] Should have redirected, got status: {response.status_code}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("IDOR PROTECTION TEST SUITE")
    print("=" * 60)
    
    try:
        test_valid_case_access()
        test_no_session()
        test_invalid_case_id()
        test_inactive_case()
        test_view_decorator()
        
        print("\n" + "=" * 60)
        print("TEST SUITE COMPLETED")
        print("=" * 60)
        print("\nReview the results above to ensure all tests passed.")
        print("Any [FAIL] results indicate a security issue that needs attention.")
        
    except Exception as e:
        print(f"\n[ERROR] Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
